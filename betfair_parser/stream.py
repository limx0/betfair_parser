import asyncio
import io
import itertools
import pathlib
import socket
import ssl
import urllib.parse
from collections.abc import AsyncGenerator, Callable, Iterable, Iterator
from typing import Any, Protocol, Self

from betfair_parser.cache import MarketSubscriptionCache, OrderSubscriptionCache
from betfair_parser.exceptions import StreamAuthenticationError, StreamError
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


class Stream(Protocol):
    """Anything the Betfair stream code accepts where it does I/O."""

    def readline(self) -> bytes: ...
    def write(self, data: bytes) -> int: ...
    def flush(self) -> None: ...
    def close(self) -> None: ...


LINE_SEPARATOR = b"\r\n"


def _default_handler(msg: StreamResponseType) -> StreamResponseType:
    return msg


class ExchangeStream:
    """Handle the byte stream with betfair."""

    def __init__(self, app_key: str, token: str, id_generator: Iterator[int] | None = None) -> None:
        self.app_key = app_key
        self.token = token
        self.subscriptions: dict[StreamRef, SubscriptionType] = {}
        self.handlers: dict[StreamRef, Callable] = {}
        self._id_generator = id_generator if id_generator is not None else itertools.count(1000)
        self._connection_id: str | None = None
        self._connections_available: int = 0
        self.authenticated = False

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
        return next(self._id_generator)

    def handle_connection(self, msg: Connection) -> Connection:
        self._connection_id = msg.connection_id
        return msg

    def handle_status(self, msg: Status) -> Status:
        if msg.is_error or msg.connection_closed:
            # a SUCCESS status with connection_closed=True (graceful shutdown) also raises: the
            # stream ends either way, callers are expected to treat this as a stream error and
            # re-establish the connection. errors before the authentication handshake completed
            # are auth errors
            error_cls = StreamError if self.authenticated else StreamAuthenticationError
            raise error_cls(
                f"Connection {self.connection_id} to stream {msg.id} failed: {msg.error_code}: {msg.error_message}",
                code=msg.error_code,
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
            raise StreamError(f"Unexpected stream message: {msg}") from None
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

    def receive(self, stream: Stream) -> Any:
        return self.receive_bytes(stream.readline())


def create_ssl_socket(hostname, timeout: float | None = None) -> ssl.SSLSocket:
    """Create ssl socket and set timeout."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        secure_sock = ssl.create_default_context().wrap_socket(s, server_hostname=hostname)
    except BaseException:  # re-raised, this only makes sure the raw socket resource gets closed
        s.close()
        raise
    secure_sock.settimeout(timeout)
    return secure_sock


class StreamIO:
    """Buffered IO over the Betfair stream. Auto-flushes writes and closes the socket on close."""

    __slots__ = ("_raw", "_stream")

    def __init__(self, raw: socket.socket, stream: io.BufferedRWPair) -> None:
        self._raw = raw
        self._stream = stream

    def readline(self) -> bytes:
        return self._stream.readline()

    def write(self, data: bytes) -> int:
        n = self._stream.write(data)
        self._stream.flush()
        return n

    def flush(self) -> None:
        self._stream.flush()

    def close(self) -> None:
        try:
            self._stream.close()
        finally:
            self._raw.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @classmethod
    def open(cls, endpoint: str, timeout: float = 15) -> Self:
        """Connect to a Betfair stream endpoint and return a buffered IO."""
        url = urllib.parse.urlparse(endpoint)
        sock = create_ssl_socket(url.hostname, timeout=timeout)
        try:
            sock.connect((url.hostname, url.port or 443))
        except OSError:
            sock.close()  # a held traceback (e.g. from logger.exception in a retry loop) would keep the fd open
            raise
        return cls(sock, sock.makefile("rwb"))


def create_stream_io(endpoint: str, timeout: float = 15) -> StreamIO:
    """Module-level alias of ``StreamIO.open``."""
    return StreamIO.open(endpoint, timeout=timeout)


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

    def subscribe(self, subscription: SubscriptionType) -> bytes | None:
        if isinstance(subscription, MarketSubscription):
            self.caches[subscription.id] = MarketSubscriptionCache()
        elif isinstance(subscription, OrderSubscription):
            self.caches[subscription.id] = OrderSubscriptionCache()
        else:
            raise TypeError("Invalid subscription type")
        return self.esm.subscribe(subscription, self.handle_change_message)

    def receive(self, stream: Stream) -> Any:
        return self.esm.receive(stream)

    def connect(self, stream: Stream) -> None:
        self.esm.receive(stream)  # read connection
        stream.write(self.esm.connect())  # send auth (StreamIO auto-flushes)
        self.esm.receive(stream)  # read auth response
        self.esm.authenticated = True

    def iter_changes(
        self,
        stream: Stream,
        path: pathlib.Path | str | None = None,
    ) -> Iterable[ChangeMessageType]:
        """Iterate over the stream, yielding market and order change messages.

        Raw messages are appended to ``path`` if given.
        """
        if not self.esm.is_connected:
            self.connect(stream)

        f = open(path, "ab") if path is not None else None  # noqa: SIM115 - file is closed in finally below
        try:
            while True:
                raw_msg = stream.readline()
                if not raw_msg:
                    return
                msg = self.esm.receive_bytes(raw_msg)
                if isinstance(msg, ChangeMessageType):
                    yield msg
                if f is not None:
                    f.write(raw_msg)
        finally:
            if f is not None:
                f.close()

    def iter_changes_and_write(
        self,
        stream: Stream,
        path: pathlib.Path | str,
    ) -> Iterable[ChangeMessageType]:
        """Iterate over the stream, yielding market and order change messages and recording raw messages to path."""
        return self.iter_changes(stream, path)


class AsyncStream:
    """Async version of io.RawIOBase over a SSL connection."""

    _reader: asyncio.StreamReader | None = None
    _writer: asyncio.StreamWriter | None = None

    def __init__(self, endpoint, timeout: float = 15) -> None:
        self._endpoint = endpoint
        self._timeout = timeout

    async def connect(self) -> None:
        url = urllib.parse.urlparse(self._endpoint)
        self._reader, self._writer = await asyncio.open_connection(
            host=url.hostname,
            port=url.port,
            ssl=ssl.create_default_context(),
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
        """Close the stream by aborting the underlying transport.

        A graceful TLS shutdown (close_notify) is deliberately not used: live streams keep sending
        application data during teardown, which would surface as `APPLICATION_DATA_AFTER_CLOSE_NOTIFY`.
        """
        self._reader = None  # does not need to be closed explicitly
        if self._writer:
            self._writer.transport.abort()  # hard close - trailing stream data must not raise SSL errors
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
        self.esm.receive_bytes(await stream.readline())  # read auth response
        self.esm.authenticated = True

    async def iter_changes_async(
        self,
        stream: AsyncStream,
        path: pathlib.Path | str | None = None,
    ) -> AsyncGenerator[ChangeMessageType, None]:
        """Iterate over the stream asynchronously, yielding market and order change messages.

        Raw messages are appended to ``path`` if given.
        """
        if not self.esm.is_connected:
            await self.connect_async(stream)

        loop = asyncio.get_running_loop()
        f = await loop.run_in_executor(None, lambda: open(path, "ab")) if path is not None else None  # noqa: SIM115 - file is sync, closed via executor below
        try:
            while True:
                raw_msg = await stream.readline()
                if not raw_msg:
                    return
                msg = self.esm.receive_bytes(raw_msg)
                if isinstance(msg, ChangeMessageType):
                    yield msg
                if f is not None:
                    await loop.run_in_executor(None, f.write, raw_msg)
        finally:
            if f is not None:
                await loop.run_in_executor(None, f.close)

    def iter_changes_and_write_async(
        self,
        stream: AsyncStream,
        path: pathlib.Path | str,
    ) -> AsyncGenerator[ChangeMessageType, None]:
        """Iterate over the stream asynchronously, yielding market and order change messages and recording raw messages to path."""
        return self.iter_changes_async(stream, path)
