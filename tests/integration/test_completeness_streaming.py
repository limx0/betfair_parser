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


def get_spec_property_pairs():
    """
    Generates a list of (spec_name, property_name) tuples for test parametrization.
    This ensures each property is tested as an individual test case.
    """
    pairs = []
    for spec_name, swagger_spec in SWAGGER_DEFS.items():
        # Extract properties from standard location or within allOf hierarchy
        properties = swagger_spec.get("properties") or swagger_spec.get("allOf", [{}, {}])[1].get("properties", [])

        for prop in properties:
            if prop == "op":
                # Skip 'op' as it is handled globally by msgspec
                continue
            pairs.append((spec_name, prop))
    return sorted(pairs)


@pytest.mark.parametrize(["spec_name", "prop_name"], get_spec_property_pairs())
def test_typedef_properties(spec_name, prop_name):
    """
    Validates that each property defined in the Swagger spec
    has a corresponding attribute in the Python API class.
    """
    py_name = api_name(spec_name)
    assert py_name in API_DEFS, f"API definition for '{spec_name}' is missing in API_DEFS"

    api_class = API_DEFS[py_name]

    pythonic_prop_name = snake_case(prop_name)
    assert hasattr(api_class, pythonic_prop_name), (
        f"Class '{api_class.__name__}' is missing attribute '{pythonic_prop_name}' (Swagger source: '{prop_name}')"
    )
