"""Check a broad selection of common API requests and responses for correct parsing."""
import bz2

import pytest

from betfair_parser.spec import accounts, betting
from betfair_parser.spec.common import Request, decode
from betfair_parser.spec.streaming import (
    MCM,
    OCM,
    Authentication,
    Connection,
    MarketSubscription,
    OrderSubscription,
    Status,
    stream_decode,
)
from betfair_parser.util import iter_stream
from tests.resources import RESOURCES_DIR, id_from_path


def _name_parts(name):
    # There are some file names, that have special remarks in the end, so we can't just mangle the name:
    # list_cleared_orders_empty etc.
    if name.startswith(("get_", "list_")):
        return 3
    if name.startswith(("cancel_", "place_", "replace_")):
        return 2
    raise ValueError(f"Filename {name} not yet covered by integration tests")


def op_cls_from_path(path):
    snake_op_name = path.name.split(".")[0]
    no_parts = _name_parts(snake_op_name)
    cls_name = "".join(pt.capitalize() for pt in snake_op_name.split("_")[:no_parts])
    mod = {"betting": betting.operations, "accounts": accounts.operations}[path.parent.name]
    return getattr(mod, cls_name)


@pytest.mark.parametrize("path", sorted((RESOURCES_DIR / "requests").glob("*/*.json")), ids=id_from_path)
def test_read_requests(path):
    raw = path.read_bytes()
    if "streaming" in str(path):
        data = stream_decode(raw)
        # TODO: use isinstance(msg, STREAM_REQUEST) for py3.10+
        assert isinstance(data, (Authentication, MarketSubscription, OrderSubscription))
        return

    assert decode(raw, type=Request)


@pytest.mark.parametrize("path", sorted((RESOURCES_DIR / "responses").glob("*/*.json")), ids=id_from_path)
def test_read_responses(path):
    raw = path.read_bytes()
    if "streaming" in str(path):
        data = stream_decode(raw)
        if isinstance(data, list):
            for msg in data:
                # TODO: use isinstance(msg, STREAM_RESPONSE) for py3.10+
                assert isinstance(msg, (MCM, OCM, Status, Connection))
        else:
            # TODO: use isinstance(msg, STREAM_RESPONSE) for py3.10+
            assert isinstance(data, (MCM, OCM, Status, Connection))
        return

    parse_type = op_cls_from_path(path).return_type
    resp = decode(raw, type=parse_type)
    assert resp
    if "error" in str(path):
        assert resp.error
    else:
        assert resp.result


@pytest.mark.parametrize(
    ["filename", "n_items"],
    [
        ("1.164917629.bz2", 298),
        ("1.185781277.bz2", 7600),
        ("1.205822330.bz2", 5654),
        ("27312315.bz2", 50854),
    ],
)
def test_archive(filename, n_items):
    path = RESOURCES_DIR / "data" / filename
    for i, res in enumerate(iter_stream(bz2.open(path)), start=1):  # type: ignore
        # TODO: use isinstance(msg, STREAM_RESPONSE) for py3.10+
        assert isinstance(res, (MCM, OCM))
    assert i == n_items
