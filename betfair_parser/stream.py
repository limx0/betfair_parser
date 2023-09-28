import asyncio
import itertools
import socket
import ssl
import urllib.parse
from typing import Optional

from betfair_parser.exceptions import StreamAuthenticationError, StreamError
from betfair_parser.spec.common import encode
from betfair_parser.spec.streaming import (
    STREAM_REQUEST,
    STREAM_RESPONSE,
    Authentication,
    Connection,
    Heartbeat,
    Status,
    stream_decode,
)


def create_ssl_socket(hostname, timeout: int = 15) -> ssl.SSLSocket:
    """Create ssl socket and set timeout."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_default_certs()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(s, server_hostname=hostname)
    secure_sock.settimeout(timeout)
    return secure_sock


class _BaseStream:
    _connection_id: Optional[str] = None

    def __init__(self, endpoint) -> None:
        self._endpoint = endpoint
        self._id_generator = itertools.count()

    @property
    def connection_id(self) -> str:
        return self._connection_id

    def unique_id(self) -> int:
        return next(self._id_generator)


class Stream(_BaseStream):
    _sock: Optional[ssl.SSLSocket] = None
    _io: Optional[socket.SocketIO] = None

    def connect(self) -> None:
        url = urllib.parse.urlparse(self._endpoint)
        self._sock = create_ssl_socket(url.hostname)
        self._sock.connect((url.hostname, url.port))
        self._io = socket.SocketIO(self._sock, "rwb")
        msg: Connection = self.receive()  # type: ignore
        self._connection_id = msg.connection_id

    def send(self, request: STREAM_REQUEST) -> None:
        if not self._io:
            raise StreamError("Stream is not connected")
        msg = encode(request) + b"\r\n"
        written_bytes = self._io.write(msg)
        if not len(msg) == written_bytes:
            raise StreamError(f"Incomplete request transfer: {written_bytes} of {len(msg)} bytes sent")

    def receive(self) -> STREAM_RESPONSE:
        if not self._io:
            raise StreamError("Stream is not connected")
        return stream_decode(self._io.readline())

    def close(self):
        if self._io is not None:
            self._io.close()
            self._io = None
        if self._sock is not None:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self._sock.close()
            self._sock = None

    def authenticate(self, app_key: str, token: str) -> None:
        self.send(Authentication(id=self.unique_id(), app_key=app_key, session=token))
        msg: Status = self.receive()  # type: ignore
        if msg.is_error:
            raise StreamAuthenticationError(f"{msg.error_code.name}: {msg.error_message}")
        if msg.connection_closed:
            raise StreamAuthenticationError("Connection was closed by the server unexpectedly")

    def heartbeat(self) -> None:
        self.send(Heartbeat(id=self.unique_id()))

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class AsyncStream(_BaseStream):
    _reader: Optional[asyncio.StreamReader] = None
    _writer: Optional[asyncio.StreamWriter] = None

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
        msg: Connection = await self.receive()  # type: ignore
        self._connection_id = msg.connection_id

    async def send(self, request: STREAM_REQUEST) -> None:
        if not self._writer:
            raise StreamError("Stream is not connected")
        msg = encode(request) + b"\r\n"
        self._writer.write(msg)
        await self._writer.drain()

    async def receive(self) -> STREAM_RESPONSE:
        if not self._reader:
            raise StreamError("Stream is not connected")
        data = await self._reader.readline()
        return stream_decode(data)

    async def close(self):
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

    async def authenticate(self, app_key: str, token: str) -> None:
        await self.send(Authentication(id=self.unique_id(), app_key=app_key, session=token))
        msg: Status = await self.receive()  # type: ignore
        if msg.is_error:
            raise StreamAuthenticationError(f"{msg.error_code.name}: {msg.error_message}")
        if msg.connection_closed:
            raise StreamAuthenticationError("Connection was closed by the server unexpectedly")

    async def heartbeat(self) -> None:
        await self.send(Heartbeat(id=self.unique_id()))

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
