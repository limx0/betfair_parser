import datetime

import msgspec

from tests.unit.conftest import RESOURCES_DIR


def read_test_file(path) -> bytes:
    full_path = RESOURCES_DIR.joinpath(path)
    if full_path.suffix == ".json":
        return full_path.read_bytes()
    else:
        raise ValueError()


def id_from_path(path) -> str:
    return str(path).rsplit("/", 1)[1].split(".", 1)[0]


def parse_json_date(datetime_str):
    return msgspec.json.decode(f'"{datetime_str}"', type=datetime.datetime)


def assert_json_equal(x, y):
    assert type(x) == type(y)
    if type(x) == dict:
        assert len(x) == len(y)
        for key_x in x:
            assert key_x in y
            assert_json_equal(x[key_x], y[key_x])
    elif type(x) == list:
        assert len(x) == len(y)
        for item_x, item_y in zip(x, y):
            assert_json_equal(item_x, item_y)
    elif isinstance(x, str) and "T" in x and x.endswith("Z"):
        # We have a time object, that might differ in the microsecond encoding
        # Betfair "2021-03-19T19:00:00.000Z" vs. msgspec "2021-03-19T19:00:00Z"
        assert parse_json_date(x) == parse_json_date(y)
    else:
        assert x == y
