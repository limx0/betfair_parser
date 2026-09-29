import socket
import threading

import msgspec
import pytest

from betfair_parser.spec.streaming import (
    MCM,
    OCM,
    Connection,
    MarketDataFilter,
    MarketFilter,
    MarketSubscription,
    MatchedOrder,
    RunnerStatus,
    StartingPriceLay,
    Status,
    stream_decode,
)
from betfair_parser.stream import ExchangeStream, create_stream_io
from tests.resources import RESOURCES_DIR


def test_ocm():
    raw = (
        b'{"op":"ocm","id":2,"clk":"AAAAAAAAAAAAAA==","pt":1669350204489,"oc":[{"id":"1.206818134","fullImage":true,'
        b'"orc":[{"id":49914337,"fullImage":true,"uo":[],"mb":[],"ml":[[2, 100]]}]}]}'
    )
    ocm: OCM = stream_decode(raw)  # type: ignore[assignment]
    assert isinstance(ocm, OCM)
    assert ocm.oc[0].orc[0].ml[0] == MatchedOrder(price=2.0, size=100)


def test_mcm():
    raw = (
        b'{"op":"mcm","id":1,"clk":"AKO0qwIAjoPCAgCmkeIC","pt":1634070799115,"mc":[{"id":"1.189081501",'
        b'"marketDefinition":{"marketId":"1.189081501","bspMarket":false,"turnInPlayEnabled":true,'
        b'"persistenceEnabled":true,"marketBaseRate":null,"eventId":"30999984","eventTypeId":"7522",'
        b'"numberOfWinners":1,"eventName":"Detroit Pistons @ New York Knicks","countryCode":"GB",'
        b'"bettingType":"ODDS","marketType":"MATCH_ODDS","marketTime":"2021-10-13T23:40:00.000Z",'
        b'"suspendTime":"2021-10-13T23:40:00.000Z","bspReconciled":false,"complete":true,"inPlay":false,'
        b'"crossMatching":false,"runnersVoidable":false,"numberOfActiveRunners":0,"betDelay":5,"status":"CLOSED",'
        b'"runners":[{"id":237474,"name":"Detroit Pistons","hc":0.0,"sortPriority":1,"status":"LOSER"},'
        b'{"id":237482,"name":"New York Knicks","hc":0.0,"sortPriority":2,"status":"WINNER"}],"regulators":["MR_INT"],'
        b'"discountAllowed":null,"timezone":"GMT","openDate":"2021-10-13T23:40:00.000Z","version":4099822530,'
        b'"priceLadderDefinition":"CLASSIC"}}]}'
    )
    mcm: MCM = stream_decode(raw)  # type: ignore[assignment]
    assert isinstance(mcm, MCM)
    runner = mcm.mc[0].market_definition.runners[0]
    assert runner.hc == 0.0
    assert runner.id == 237474
    assert runner.name == "Detroit Pistons"
    assert runner.sort_priority == 1
    assert runner.status.value == "LOSER"


def test_mcm_no_missing_fields():
    raw = {
        "op": "mcm",
        "clk": "7977927644",
        "pt": 1541992250576,
        "mc": [
            {
                "id": "1.147666818",
                "marketDefinition": {
                    "bspMarket": False,
                    "turnInPlayEnabled": True,
                    "persistenceEnabled": True,
                    "marketBaseRate": 5.0,
                    "eventId": "28045743",
                    "eventTypeId": "4",
                    "numberOfWinners": 1,
                    "bettingType": "ODDS",
                    "marketType": "TOURNAMENT_WINNER",
                    "marketTime": "2018-11-30T23:40:00.000Z",
                    "suspendTime": "2018-11-30T23:40:00.000Z",
                    "bspReconciled": False,
                    "complete": True,
                    "inPlay": False,
                    "crossMatching": False,
                    "runnersVoidable": False,
                    "numberOfActiveRunners": 8,
                    "betDelay": 0,
                    "status": "OPEN",
                    "runners": [
                        {
                            "status": "ACTIVE",
                            "sortPriority": 1,
                            "id": 12217371,
                            "name": "Perth Scorchers WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 2,
                            "id": 12217558,
                            "name": "Sydney Sixers WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 3,
                            "id": 12215567,
                            "name": "Adelaide Strikers WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 4,
                            "id": 12217241,
                            "name": "Sydney Thunder WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 5,
                            "id": 12217559,
                            "name": "Brisbane Heat WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 6,
                            "id": 12217370,
                            "name": "Hobart Hurricanes WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 7,
                            "id": 12215569,
                            "name": "Melbourne Renegades WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 8,
                            "id": 12217242,
                            "name": "Melbourne Stars WBBL",
                        },
                    ],
                    "regulators": ["MR_INT"],
                    "countryCode": "AU",
                    "discountAllowed": False,
                    "timezone": "Australia/Sydney",
                    "openDate": "2017-12-09T02:45:00.000Z",
                    "version": 2511916192,
                    "name": "Winner 2018/19",
                    "eventName": "WBBL",
                },
                "rc": [],
                "con": True,
                "img": False,
            }
        ],
    }
    mcm: MCM = stream_decode(msgspec.json.encode(raw))  # type: ignore[assignment]
    data = msgspec.json.decode(msgspec.json.encode(mcm))
    result = set(data["mc"][0]["marketDefinition"].keys())
    expected = set(raw["mc"][0]["marketDefinition"].keys())  # type: ignore[index]
    assert expected - result == set()


def test_mcm_no_clk():
    raw = b'{"op": "mcm", "clk": null, "pt": 1576840503572, "mc": []}'
    mcm: MCM = stream_decode(raw)  # type: ignore[assignment]
    assert mcm.clk is None


def test_mcm_market_definition_each_way():
    raw = (RESOURCES_DIR / "responses" / "streaming" / "mcm_market_definition_each_way.json").read_bytes()
    mcm: MCM = stream_decode(raw)  # type: ignore[assignment]
    assert mcm.mc[0].market_definition.market_type == "EACH_WAY"
    assert mcm.mc[0].market_definition.each_way_divisor == 4.0


def test_bsp_data():
    raw = (RESOURCES_DIR / "responses" / "streaming" / "mcm_bsp_data.json").read_bytes()
    mcm: MCM = stream_decode(raw)[0]  # type: ignore[assignment,index]
    rc = mcm.mc[0].rc[0]
    assert rc.spl == [StartingPriceLay(price=1.01, volume=2.8)]
    assert rc.spn == 4.5


def test_bsp_result():
    raw = (RESOURCES_DIR / "responses" / "streaming" / "mcm_market_definition_bsp.json").read_bytes()
    mcm: MCM = stream_decode(raw)  # type: ignore[assignment]
    runners = mcm.mc[0].market_definition.runners
    assert runners[0].bsp == 2.0008034621107256
    assert runners[0].status == RunnerStatus.WINNER


def test_status_error_alt():
    raw = (RESOURCES_DIR / "responses" / "streaming" / "status_error_alt.json").read_bytes()
    status: Status = stream_decode(raw)  # type: ignore[assignment]
    assert status


def test_exchange_stream_subscription_before_connect():
    """Subscribing before connecting defers the write, after connecting it returns the payload."""
    es = ExchangeStream("app_key", "token")
    subscription = MarketSubscription(market_filter=MarketFilter(), market_data_filter=MarketDataFilter())
    assert es.subscribe(subscription) is None
    es.handle_connection(Connection(connection_id="test-connection"))
    payload = es.subscribe(subscription)
    assert payload is not None
    assert b'"op":"marketSubscription"' in payload


def test_unique_id_from_custom_generator():
    es = ExchangeStream("app_key", "token", id_generator=iter([42, 43]))
    assert es.unique_id() == 42
    assert es.unique_id() == 43


def test_create_stream_io_connect_failure_closes_socket():
    """Connect failures close the underlying socket right away.

    A retry loop that logs the exception (logger.exception) keeps the traceback alive,
    which keeps the create_stream_io frame alive - without the explicit close, every
    failed connect attempt would leak one file descriptor.
    """
    failed = []
    for _ in range(3):
        try:
            create_stream_io("ndjson://127.0.0.1:1", timeout=1)
        except OSError as exc:  # simulate a retry loop holding the exception for logging
            failed.append(exc)
    assert len(failed) == 3
    for held in failed:
        tb = held.__traceback__
        while tb is not None and "sock" not in tb.tb_frame.f_locals:
            tb = tb.tb_next
        assert tb is not None, "create_stream_io frame not found in traceback"
        assert tb.tb_frame.f_locals["sock"].fileno() == -1  # closed instead of leaking the fd


def test_buffered_stream_supports_exchange_receive():
    """ExchangeStream.receive reads from a buffered stream via a socketpair."""
    peer, sock = socket.socketpair()
    try:
        es = ExchangeStream("app_key", "token")
        buffered = sock.makefile("rwb")
        peer.sendall(b'{"op":"connection","connectionId":"test"}\r\n')
        msg = es.receive(buffered)
        assert msg.connection_id == "test"
    finally:
        buffered.close()
        sock.close()
        peer.close()


def test_buffered_write_flush_reaches_peer():
    """Buffered writes must be flushed to actually be sent to the peer."""
    peer, sock = socket.socketpair()
    try:
        peer.settimeout(2)
        buffered = sock.makefile("rwb")
        buffered.write(b"hello\r\n")
        buffered.flush()
        assert peer.recv(8) == b"hello\r\n"
    finally:
        buffered.close()
        sock.close()
        peer.close()


def test_readline_across_buffer_fills():
    """BufferedReader.readline handles lines larger than the 8KB internal buffer."""
    peer, sock = socket.socketpair()
    try:
        peer.settimeout(10)
        buffered = sock.makefile("rwb")
        big = b"x" * 250_000

        def sender():
            peer.sendall(big + b"\r\n")

        threading.Thread(target=sender, daemon=True).start()
        assert buffered.readline() == big + b"\r\n"
    finally:
        buffered.close()
        sock.close()
        peer.close()


def test_create_stream_io_propagates_connect_failure():
    """create_stream_io raises on a refused endpoint instead of handing back a broken stream."""
    with pytest.raises(OSError), create_stream_io("ndjson://127.0.0.1:1", timeout=1):
        pass


def test_create_stream_io_requires_explicit_flush_after_write():
    """Buffered IO writes don't reach the peer until flushed - callers must flush()."""
    peer, sock = socket.socketpair()
    try:
        peer.settimeout(0.2)  # short timeout so a buffered write doesn't hang the test
        stream = sock.makefile("rwb")
        stream.write(b"hello\r\n")  # not flushed yet - peer recv would time out
        # confirm the write is buffered (peer cannot read it without flush)
        with pytest.raises(TimeoutError):
            peer.recv(8)
        stream.flush()
        assert peer.recv(8) == b"hello\r\n"
    finally:
        stream.close()
        sock.close()
        peer.close()
