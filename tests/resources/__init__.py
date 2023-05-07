from tests.unit.conftest import RESOURCES_DIR


def read_test_file(path) -> bytes:
    full_path = RESOURCES_DIR.joinpath(path)
    if full_path.suffix == ".json":
        return full_path.read_bytes()
    else:
        raise ValueError()


def id_from_path(path) -> str:
    return str(path).rsplit("/", 1)[1].split(".", 1)[0]
