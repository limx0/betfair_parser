"""
This module checks against the published betfair XML API definition files,
if all operations, type definitions and enums are covered within this package.
This includes checking of all parameters of operations and type definitions.
"""

import keyword
import re
import xml.etree.ElementTree as etree  # noqa
from typing import get_type_hints

import pytest

from betfair_parser.spec import accounts, betting, common, heartbeat
from tests.resources import RESOURCES_DIR


XML_DEFINITIONS = ["AccountAPING", "SportsAPING", "HeartbeatAPING"]
XML_FILES = [RESOURCES_DIR / "documents" / f"{apidef}.xml" for apidef in XML_DEFINITIONS]


def xml_nodes(path, xml_type):
    tree = etree.parse(path)  # noqa
    return sorted(tree.findall(f".//{xml_type}"), key=lambda node: node.get("name"))


def id_check_item(item):
    if hasattr(item, "get"):
        return item.get("name")
    return item.__name__.split(".spec.")[1].split(".", 1)[0]


@pytest.mark.parametrize(
    ["spec", "node"],
    [
        (spec, node)
        for xml_file, spec in zip(XML_FILES, (accounts.enums, betting.enums, heartbeat))
        for node in xml_nodes(xml_file, "simpleType")
        if not list(node.iter("validValues"))  # exclude enums
    ],
    ids=id_check_item,
)
def test_basetype(spec, node):
    xml_typename = node.get("name")
    py_type = get_definition(spec, xml_typename)
    xml_type = xml_type_compat(node.get("type"))
    py_type_str = py_type_format(py_type_unpack(py_type))

    if xml_typename.endswith("Id") and xml_typename not in ("SelectionId", "MarketId"):
        # ID types are integer values encoded as strings
        assert xml_type == "str"
        assert py_type_str == "int"
    else:
        assert xml_type == py_type_str


@pytest.mark.parametrize(
    ["spec", "node"],
    [
        (spec, node)
        for xml_file, spec in zip(XML_FILES, (accounts.enums, betting.enums, heartbeat))
        for node in xml_nodes(xml_file, "simpleType")
        if list(node.iter("validValues"))  # enums only
    ],
    ids=id_check_item,
)
def test_enum(spec, node):
    xml_typename = node.get("name")
    if xml_typename in ("MarketGroupType", "LimitBreachActionType"):
        # Defined only in XML, but not in documentation
        pytest.skip("Not defined in documentation")

    datatype_cls = get_definition(spec, xml_typename)
    valid_values = list(node.iter("validValues"))[0]
    min_values = 1 if xml_typename in ("Status", "ItemClass", "TokenType", "TimeInForce") else 2
    assert len(valid_values) >= min_values
    assert node.get("type") == "string"
    for value_node in valid_values.iter("value"):
        value_name = value_node.get("name")
        assert hasattr(datatype_cls, value_name), f"Enum field {xml_typename}.{value_name} not set"


@pytest.mark.parametrize(
    ["spec", "node"],
    [
        (spec, node)
        for xml_file, spec in zip(XML_FILES, (accounts.type_definitions, betting.type_definitions, heartbeat))
        for node in xml_nodes(xml_file, "dataType")
    ],
    ids=id_check_item,
)
def test_typedef(spec, node):
    typedef_name = node.get("name")
    if typedef_name in ("DeveloperAppVersion",):
        pytest.skip("Subscription and vendor operations are not covered by this API implementation")
    if typedef_name == "TransferResponse":
        pytest.skip("Deprecated according to documentation")
    if typedef_name in {
        "LimitBreachAction",
        "MarketGroupExposureLimit",
        "MarketGroupId",
        "MarketGroup",
        "ExposureLimitsForMarketGroups",
        "ExposureLimit",
        "MarketState",
        "Matches",
    }:
        pytest.skip("Defined only by XML, but not in the documentation")
    typedef_cls = get_definition(spec, typedef_name)
    for param in node.iter("parameter"):
        check_typedef_param(param, typedef_cls, typedef_name)


DOCUMENTATION_ERRORS = {
    "CancelInstructionReport": {
        "size_cancelled": "Marked as mandatory, but it's skipped in case of errors",
        "cancelled_date": "Marked as mandatory, but it's skipped in case of errors",
    },
    "RunnerCatalog": {"sort_priority": "Marked as mandatory, but seems to be optional in real data"},
    "Runner": {"adjustment_factor": "Marked as mandatory in the XML, but optional according to the documentation"},
    "LimitOrder": {
        "size": "Marked as optional, but mandatory according to the documentation",
        "persistence_type": "Marked as optional in the XML, but mandatory according to the documentation",
    },
    "CurrentOrderSummary": {"matched_date": "Marked as mandatory, but is occasionally missing in real data"},
    "ClearedOrderSummary": {"profit": "Profit is not a size, it's just a float"},
    "listMarketBook": {"market_ids": "Should be set instead of list, just like all other market_ids"},
}


def check_typedef_param(param, py_cls, typedef_name):
    xml_param_name = param_name(param)
    if is_param_deprecated(param):
        return
    if DOCUMENTATION_ERRORS.get(typedef_name, {}).get(xml_param_name):
        # Documented exception for this parameter found, skip checks
        return

    assert py_cls is not None, f"{typedef_name} does not define parameters, but XML defines '{xml_param_name}'"
    assert is_param_defined(param, py_cls), f"{typedef_name}.{xml_param_name} not defined"
    param_cls = py_cls.__annotations__[xml_param_name]
    if is_param_mandatory(param):
        assert not is_param_optional(param, py_cls), f"{typedef_name} fails to require {xml_param_name}"
    else:
        assert is_param_optional(param, py_cls), f"{typedef_name} erroneously requires {xml_param_name}"
        param_cls = py_type_unpack(param_cls)  # unpack Optional[...]

    xml_type = xml_type_compat(param.get("type"), param_name=xml_param_name)
    param_cls_name = py_type_format(param_cls)
    assert xml_type == param_cls_name, f"{typedef_name}.{xml_param_name}:{xml_type}: Invalid type: {param_cls_name}"


UNCOVERED_API_KEYWORDS = [
    # Exclude operations, that are deliberately out of scope of this API
    "Subscription",
    "Subscribed",
    "Vendor",
    "Developer",
    "Affiliate",
    "AuthorisationCode",
    "WebApp",
]


@pytest.mark.parametrize(
    ["spec", "node"],
    [
        (spec, node)
        for xml_file, spec in zip(XML_FILES, (accounts.operations, betting.operations, heartbeat))
        for node in xml_nodes(xml_file, "operation")
        if not any(unhandled in node.get("name") for unhandled in UNCOVERED_API_KEYWORDS)
    ],
    ids=id_check_item,
)
def test_operations(spec, node):
    operation_name = node.get("name")
    if "MarketGroup" in operation_name:
        pytest.skip("MarketGroup is not contained in the documentation and was probably removed from the API")
    if operation_name == "transferFunds":
        pytest.skip("@Deprecated due to the removal of the AUS wallet")
    if operation_name in {
        "token",
        "addExposureReuseEnabledEvents",
        "getExposureReuseEnabledEvents",
        "removeExposureReuseEnabledEvents",
    }:
        pytest.skip("Not mentioned anywhere in the documentation")

    operation_cls = get_definition(spec, capitalize(operation_name))
    assert isinstance(operation_cls.endpoint_type.value, str), "EndpointType was not defined correctly"
    assert operation_cls.__doc__, "No documentation was provided"
    xml_return_type = node.findall("parameters/simpleResponse")[0].get("type")
    assert xml_type_compat(xml_return_type) == py_type_format(py_type_unpack(operation_cls.return_type))
    xml_error_type = node.findall("parameters/exceptions/exception")[0].get("type")
    assert xml_type_compat(xml_error_type) == operation_cls.throws.__name__
    try:
        params_cls = get_type_hints(operation_cls)["params"]
    except KeyError:
        return

    params_cls_name = compat_type_name(params_cls)
    if params_cls_name == "Optional":
        # for GetAccountDetails, GetAccountFunds
        params_cls = py_type_unpack(params_cls)
        params_cls_name = compat_type_name(params_cls)
    assert params_cls_name.endswith("Params")
    params = node.findall("parameters/request/parameter")
    for param in params:
        check_typedef_param(param, params_cls, operation_name)


# Little helper functions


def capitalize(val: str) -> str:
    return val[:1].upper() + val[1:]


def snake_case(val: str) -> str:
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    val = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", val)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", val).lower()


def get_definition(spec, definition):
    if hasattr(spec, definition):
        return getattr(spec, definition)
    if definition in dir(common):
        return getattr(common, definition)
    raise AssertionError(f"{definition} not defined")


def param_name(xml_param) -> str:
    """Translate the XML camel case names to snake case, escaping python keywords."""
    p_name = snake_case(xml_param.get("name"))
    if p_name in keyword.kwlist:
        return f"{p_name}_"
    return p_name


def is_param_deprecated(xml_param) -> bool:
    desc = (xml_param.findall("description")[0].text or "").strip()
    return desc.startswith("@Deprecated")


def is_param_defined(xml_param, api_cls) -> bool:
    p_name = param_name(xml_param)
    return p_name in api_cls.__dict__


def is_param_mandatory(xml_param) -> bool:
    return xml_param.get("mandatory") == "true"


def is_param_optional(xml_param, api_cls) -> bool:
    p_name = param_name(xml_param)
    type_spec_str = str(api_cls.__annotations__[p_name]).replace("typing.", "")
    return type_spec_str.startswith("Optional") or type_spec_str.endswith("| None")


def py_type_unpack(type_def):
    return type_def.__args__[0]


def py_type_unpack_annotated(type_def):
    if compat_type_name(type_def) == "Annotated":
        return py_type_unpack(type_def)
    return type_def


def py_type_format(type_def) -> str:
    type_def_name = compat_type_name(type_def)
    if hasattr(type_def, "__metadata__"):
        return py_type_replace(type_def.__metadata__[-1].title)
    if not hasattr(type_def, "__args__"):
        return py_type_replace(type_def_name)
    args = type_def.__args__ if type_def_name != "Optional" else type_def.__args__[:-1]
    args_fmt = ",".join(py_type_format(arg) for arg in args)
    return f"{py_type_replace(type_def_name)}[{args_fmt}]"


PY_TYPE_NAME_REPLACEMENTS = {
    "SubscriptionStatus": "str",
    "MarketStatus": "str",
    "MarketId": "str",
    "RunnerStatus": "str",
    "CustomerRef": "str",
    "Wallet": "str",
    "Handicap": "float",
    "Date": "datetime",
    "InstructionReportStatus": "str",
    "InstructionReportErrorCode": "str",
    "WinLose": "str",
    "PersistenceType": "str",
    "OrderType": "str",
    "OrderStatus": "str",
    "Side": "str",
    "ExecutionReportStatus": "str",
    "ExecutionReportErrorCode": "str",
    "CustomerOrderRef": "str",
    "CustomerStrategyRef": "str",
    "MarketBettingType": "str",
    "RunnerMetaData": "dict[str,str]",
    "BetId": "int",
    "CompetitionId": "int",
    "ExchangeId": "int",
    "SelectionId": "int",
    "EventId": "int",
    "MatchId": "int",
    "IDType": "int",
    "EventTypeId": "int",
    "MarketType": "str",
    "MarketTypeCode": "str",
}

XML_TYPE_NAME_REPLACEMENTS = {
    "string": "str",
    "i32": "int",
    "i64": "int",
    "double": "float",
    "dateTime": "datetime",
    "map": "dict",
    "MarketId": "str",
    "Date": "datetime",
    "Handicap": "float",
    "PersistenceType": "str",  # inconsistently used
    "CustomerOrderRef": "str",  # inconsistently used
    "CustomerStrategyRef": "str",  # inconsistently used
    "OrderType": "str",  # inconsistently used
    "OrderStatus": "str",  # inconsistently used
    "Side": "str",  # inconsistently used
    "MarketBettingType": "str",  # inconsistently used
    "MarketTypeCode": "str",
    "Wallet": "str",  # inconsistently used
    "Matches": "list[Match]",
    "(": "[",
    ")": "]",
    ", ": ",",  # inconsistently used
    "SelectionId": "int",
    "CompetitionId": "int",
    "BetId": "int",
    "ExchangeId": "int",
    "MatchId": "int",
    "EventId": "int",
    "EventTypeId": "int",
}


def py_type_replace(name: str) -> str:
    # All the special handled types and inconsistencies need some extra care
    return PY_TYPE_NAME_REPLACEMENTS.get(name, name)


def xml_type_compat(xml_type_def, param_name=None):
    """API definition switches from using base type definitions to specialized types."""
    if param_name == "bet_id" and xml_type_def == "string":
        xml_type_def = "BetId"

    for xml_type, py_type in XML_TYPE_NAME_REPLACEMENTS.items():
        xml_type_def = xml_type_def.replace(xml_type, py_type)

    # The following replacements need to be done carefully in order not to mess up naming
    if "MarketTypeResult" not in xml_type_def:
        xml_type_def = xml_type_def.replace("MarketType", "str")
    return xml_type_def


def compat_type_name(type_def) -> str:
    """Workaround for py3.9 which does not define a __name__ attribute for typing classes."""
    try:
        return type_def.__name__
    except AttributeError:
        # class name looks like _UnionGenericAlias, _AnnotatedAlias
        if type_def.__class__.__name__.startswith("_Annotated"):
            return "Annotated"
        name = type_def.__class__.__name__.lstrip("_").replace("Alias", "").replace("Generic", "").replace("Type", "")
        if name == "Union" and type_def.__args__[-1] is type(None):  # noqa
            # Optional looks just like Union, so we need to distinguish
            return "Optional"
        if not name:
            # Probably an enum
            try:
                return type_def.__origin__.__name__
            except AttributeError:
                pass
        return name
