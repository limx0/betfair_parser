"""Check a broad selection of common API requests and responses for correct parsing."""
import bz2

import pytest

from betfair_parser.spec import accounts, betting
from betfair_parser.spec.common import Request, decode
from betfair_parser.util import iter_stream, stream_decode
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
    assert decode(raw, type=Request)


@pytest.mark.parametrize("path", sorted((RESOURCES_DIR / "responses").glob("*/*.json")), ids=id_from_path)
def test_read_responses(path):
    raw = path.read_bytes()
    if "streaming" in str(path):
        resp = stream_decode(raw)
    else:
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
        ("1.185781277.bz2", 7600),
        ("1.205822330.bz2", 5654),
        ("27312315.bz2", 50854),
    ],
)
def test_archive(filename, n_items):
    path = RESOURCES_DIR / "data" / filename
    results = list(iter_stream(bz2.open(path)))  # type: ignore
    assert len(results) == n_items
