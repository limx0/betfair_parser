import asyncio
import io
import itertools
import pathlib
import socket
import ssl
import urllib.parse
from collections.abc import AsyncGenerator, Callable, Iterable
from typing import Any

from betfair_parser.cache import MarketSubscriptionCache, OrderSubscriptionCache
from betfair_parser.exceptions import StreamError
from betfair_parser.spec.common import encode
from betfair_parser.spec.streaming import (
    MCM,
    OCM,
    Authentication,
    ChangeMessageType,
    Connection,
    MarketSubscription,
    OrderSubscription,
    Status,
    StreamRef,
    StreamResponseType,
    SubscriptionType,
    stream_decode,
)


LINE_SEPARATOR = b"\r\n"


def _default_handler(msg: StreamResponseType) -> StreamResponseType:
    return msg


class ExchangeStream:
    """Handle the byte stream with betfair."""

    def __init__(self, app_key: str, token: str, id_generator: Callable | None = None) -> None:
        self.app_key = app_key
        self.token = token
        self.subscriptions: dict[StreamRef, SubscriptionType] = {}
        self.handlers: dict[StreamRef, Callable] = {}
        self._id_generator = id_generator if id_generator is not None else itertools.count(1000)
        self._connection_id: str | None = None
        self._connections_available: int = 0

    @property
    def connection_id(self) -> str | None:
        return self._connection_id

    @property
    def is_connected(self) -> bool:
        return bool(self.connection_id)

    @property
    def connections_available(self) -> int:
        return self._connections_available

    def unique_id(self) -> int:
        return next(self._id_generator)  # type: ignore[arg-type]

    def handle_connection(self, msg: Connection) -> Connection:
        self._connection_id = msg.connection_id
        return msg

    def handle_status(self, msg: Status) -> Status:
        if msg.is_error or msg.connection_closed:
            raise StreamError(
                f"Connection {self.connection_id} to stream {msg.id} failed: {msg.error_code}: {msg.error_message}"
            )
        if msg.connections_available is not None:
            self._connections_available = msg.connections_available
        return msg

    def handle_msg(self, msg: StreamResponseType) -> Any:
        match msg:
            case Status():
                return self.handle_status(msg)
            case Connection():
                return self.handle_connection(msg)
        try:
            return self.handlers[msg.id](msg)
        except KeyError:
            raise StreamError(f"Unexpected stream message: {msg}")
        except Exception as e:
            raise StreamError(f"Handling stream message failed: {msg}") from e

    def authenticate(self) -> bytes:
        return encode(Authentication(id=self.unique_id(), app_key=self.app_key, session=self.token)) + LINE_SEPARATOR

    def subscribe(self, subscription: SubscriptionType, handler: Callable = _default_handler) -> bytes | None:
        self.subscriptions[subscription.id] = subscription
        self.handlers[subscription.id] = handler
        if self.connection_id:
            # only write something, if the connection is already established
            return encode(subscription) + LINE_SEPARATOR
        return None

    def connect(self) -> bytes:
        auth = self.authenticate()
        if not self.subscriptions:
            return auth

        # send out subscriptions, that were registered before connecting
        subscriptions = LINE_SEPARATOR.join(encode(subscription) for subscription in self.subscriptions.values())
        return auth + subscriptions + LINE_SEPARATOR

    def receive_bytes(self, data: bytes) -> Any:
        if not data:
            return None
        return self.handle_msg(stream_decode(data))  # type: ignore[arg-type]

    def receive(self, stream: io.RawIOBase) -> Any:
        return self.receive_bytes(stream.readline())


def create_ssl_socket(hostname, timeout: float | None = None) -> ssl.SSLSocket:
    """Create ssl socket and set timeout."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_default_certs()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(s, server_hostname=hostname)
    secure_sock.settimeout(timeout)
    return secure_sock


def create_stream_io(endpoint, timeout: float = 15):
    """Open an IO stream through a TLS connection to the given endpoint."""
    url = urllib.parse.urlparse(endpoint)
    sock = create_ssl_socket(url.hostname, timeout=timeout)
    sock.connect((url.hostname, url.port))
    return socket.SocketIO(sock, "rwb")


def changed_markets(msg: StreamResponseType) -> list[str]:
    """Return the market IDs of the markets affected by the given message."""
    if isinstance(msg, MCM) and msg.market_changes:
        return [m.id for m in msg.market_changes]
    if isinstance(msg, OCM) and msg.order_market_changes:
        return [m.id for m in msg.order_market_changes]
    return []


class StreamReader:
    """Read exchange stream data into a separate cache for each subscription."""

    def __init__(self, app_key, token) -> None:
        self.caches: dict[StreamRef, MarketSubscriptionCache | OrderSubscriptionCache] = {}
        self.esm = ExchangeStream(app_key, token)

    def handle_change_message(self, msg: ChangeMessageType) -> ChangeMessageType:
        self.caches[msg.id].update(msg)  # type: ignore[arg-type]
        return msg

    def subscribe(self, subscription: SubscriptionType) -> bytes:
        if isinstance(subscription, MarketSubscription):
            self.caches[subscription.id] = MarketSubscriptionCache()
        elif isinstance(subscription, OrderSubscription):
            self.caches[subscription.id] = OrderSubscriptionCache()
        else:
            raise TypeError("Invalid subscription type")
        return self.esm.subscribe(subscription, self.handle_change_message)

    def receive(self, stream: io.RawIOBase) -> Any:
        return self.esm.receive(stream)

    def connect(self, stream: io.RawIOBase) -> None:
        self.esm.receive(stream)  # read connection
        stream.write(self.esm.connect())  # send auth
        self.esm.receive(stream)

    def iter_changes(self, stream: io.RawIOBase) -> Iterable[ChangeMessageType]:
        """Iterate over the stream, yielding market and order change messages."""
        if not self.esm.is_connected:
            self.connect(stream)

        while True:
            msg = self.esm.receive(stream)
            if not msg:
                return
            if isinstance(msg, ChangeMessageType):
                yield msg

    def iter_changes_and_write(
        self,
        stream: io.RawIOBase,
        path: pathlib.Path | str,
    ) -> Iterable[ChangeMessageType]:
        if not self.esm.is_connected:
            self.connect(stream)

        with open(path, "ab") as f:
            while True:
                raw_msg = stream.readline()
                if not raw_msg:
                    return
                msg = self.esm.receive_bytes(raw_msg)
                if isinstance(msg, ChangeMessageType):
                    yield msg
                f.write(raw_msg)


class AsyncStream:
    """Async version of io.RawIOBase over a SSL connection."""

    _reader: asyncio.StreamReader | None = None
    _writer: asyncio.StreamWriter | None = None

    def __init__(self, endpoint, timeout: float = 15) -> None:
        self._endpoint = endpoint
        self._timeout = timeout

    async def connect(self) -> None:
        url = urllib.parse.urlparse(self._endpoint)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_default_certs()
        self._reader, self._writer = await asyncio.open_connection(
            host=url.hostname,
            port=url.port,
            ssl=context,
            server_hostname=url.hostname,
            limit=1_000_000,
        )

    async def write(self, data: bytes) -> None:
        if not self._writer:
            raise StreamError("Stream is not connected")
        self._writer.write(data)
        await self._writer.drain()

    async def readline(self) -> bytes:
        if not self._reader:
            raise StreamError("Stream is not connected")
        return await self._reader.readline()

    async def close(self) -> None:
        self._reader = None  # does not need to be closed explicitly
        if self._writer:
            await self._writer.drain()

            # Abort the underlying transport (equivalent to socket.shutdown())
            transport = self._writer.transport
            if transport:
                transport.abort()

            # Close the writer (which should in turn close the underlying transport)
            self._writer.close()
            await self._writer.wait_closed()
        self._writer = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


class AsyncStreamReader(StreamReader):
    async def receive_async(self, stream: AsyncStream) -> Any:
        return self.esm.receive_bytes(await stream.readline())

    async def connect_async(self, stream: AsyncStream) -> None:
        self.esm.receive_bytes(await stream.readline())  # read connection
        await stream.write(self.esm.connect())  # send auth
        self.esm.receive_bytes(await stream.readline())

    async def iter_changes_async(self, stream: AsyncStream) -> AsyncGenerator[ChangeMessageType, None]:
        if not self.esm.is_connected:
            await self.connect_async(stream)

        while True:
            msg = self.esm.receive_bytes(await stream.readline())
            if not msg:
                return
            if isinstance(msg, ChangeMessageType):
                yield msg

    async def iter_changes_and_write_async(
        self,
        stream: AsyncStream,
        path: pathlib.Path | str,
    ) -> AsyncGenerator[ChangeMessageType, None]:
        if not self.esm.is_connected:
            await self.connect_async(stream)

        loop = asyncio.get_running_loop()
        with open(path, "ab") as f:
            while True:
                raw_msg = await stream.readline()
                if not raw_msg:
                    return
                msg = self.esm.receive_bytes(raw_msg)
                if isinstance(msg, ChangeMessageType):
                    yield msg
                await loop.run_in_executor(None, f.write, raw_msg)
