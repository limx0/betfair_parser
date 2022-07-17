from tests.unit.streaming.test_streaming_core import RESOURCES_DIR


def read_test_file(path) -> bytes:
    full_path = RESOURCES_DIR.joinpath(path)
    if full_path.suffix == ".json":
        return full_path.read_bytes()
    else:
        raise ValueError()
