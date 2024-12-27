import datetime
from pathlib import Path

import msgspec


RESOURCES_DIR = Path(__file__).parent.absolute()


def id_from_path(path: Path | str) -> str:
    """Create a test case id from a file path."""
    return Path(path).stem


def _parse_json_date(datetime_str):
    return msgspec.json.decode(f'"{datetime_str}"', type=datetime.datetime)


def assert_json_equal(x, y):
    assert type(x) is type(y)
    if isinstance(x, dict):
        # can't compare the length, as None values might have been omitted
        assert sum(1 for v in x.values() if v is not None) == sum(1 for v in y.values() if v is not None)
        for key_x in x:
            assert_json_equal(x[key_x], y.get(key_x))
    elif isinstance(x, list):
        assert len(x) == len(y)
        for item_x, item_y in zip(x, y):
            assert_json_equal(item_x, item_y)
    elif isinstance(x, str) and "T" in x and x.endswith("Z"):
        # We have a time object, that might differ in the microsecond encoding
        # Betfair "2021-03-19T19:00:00.000Z" vs. msgspec "2021-03-19T19:00:00Z"
        assert _parse_json_date(x) == _parse_json_date(y)
    else:
        assert x == y
