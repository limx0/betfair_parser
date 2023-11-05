import msgspec
import pytest

from betfair_parser.spec.streaming import messages, type_definitions
from tests.integration.test_completeness import snake_case
from tests.resources import RESOURCES_DIR


API_DEFS = dict(type_definitions.__dict__, **messages.__dict__)
SWAGGER_FILE = RESOURCES_DIR / "documents" / "ESASwaggerSchema.json"
SWAGGER_DEFS = {
    k: v for k, v in msgspec.json.decode(SWAGGER_FILE.read_bytes())["definitions"].items() if "Example" not in k
}


def api_name(spec: str) -> str:
    if not spec.endswith("Message"):
        return spec
    if spec == "MarketChangeMessage":
        return "MCM"
    if spec == "OrderChangeMessage":
        return "OCM"
    if spec == "RequestMessage":
        return "_StreamRequest"
    if spec == "ResponseMessage":
        return "_StreamResponse"
    return spec.replace("Message", "")


@pytest.mark.parametrize("spec", sorted(SWAGGER_DEFS))
def test_typedef(spec: str):
    swagger_spec = SWAGGER_DEFS[spec]
    swagger_properties = swagger_spec.get("properties") or swagger_spec["allOf"][1].get("properties", [])

    py_name = api_name(spec)
    assert py_name in API_DEFS

    api_class = API_DEFS[py_name]
    for prop in swagger_properties:
        if prop == "op":
            # this is defined and handled by msgspec
            continue
        assert hasattr(api_class, snake_case(prop))
