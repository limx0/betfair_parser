"""
This module checks against the published betfair XML API definition files,
if all operations, type definitions and enums are covered within this package.
This includes checking of all parameters of operations and type definitions.
"""

import keyword
import re
import xml.etree.ElementTree as etree  # noqa

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
    return item.__name__.split(".spec.")[1]


@pytest.mark.parametrize(
    ["spec", "node"],
    [
        (spec, node)
        for xml_file, spec in zip(XML_FILES, (accounts.enums, betting.enums, heartbeat))
        for node in xml_nodes(xml_file, "simpleType")
    ],
    ids=id_check_item,
)
def test_enum(spec, node):
    xml_typename = node.get("name")
    if xml_typename in ("MarketGroupType", "LimitBreachActionType"):
        # Defined only in XML, but not in documentation
        pytest.skip("Not defined in documentation")
    if xml_typename == "MarketType":
        pytest.skip("Misplaced in XML, belongs to accounts")
    if xml_typename == "EventTypeId":
        pytest.skip("It's stated as str in the API, but actually an int")

    datatype_cls = get_definition(spec, xml_typename)
    validvalues = list(node.iter("validValues"))
    if not validvalues:
        # Type is a simple subclass
        xml_type = xml_type_format(node.get("type"))
        datatype_str = py_type_format(py_type_unpack(datatype_cls))
        if datatype_str == "Union[str,int]":
            # Some custom defined hybrid types for fields, that accept both, even if not stated in the XML
            assert xml_type == "str"
        else:
            assert py_type_format(py_type_unpack(datatype_cls)) == xml_type
    else:
        # Type is an enum of strings
        validvalues = validvalues[0]
        assert node.get("type") == "string"
        for value in validvalues.iter("value"):
            valname = value.get("name")
            assert hasattr(datatype_cls, valname), f"Enum field {xml_typename}.{valname} not set"


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
}


def check_typedef_param(param, py_cls, typedef_name):
    xml_param_name = param_name(param)
    if param_deprecated(param):
        return
    if DOCUMENTATION_ERRORS.get(typedef_name, {}).get(xml_param_name):
        # Documented exception for this parameter found, skip checks
        return

    assert py_cls is not None, f"{typedef_name} does not define parameters, but XML defines '{xml_param_name}'"
    assert param_defined(param, py_cls), f"{typedef_name}.{xml_param_name} not defined"
    param_cls = py_cls.__annotations__[xml_param_name]
    if param_mandatory(param):
        assert not param_optional(param, py_cls), f"{typedef_name} fails to require {xml_param_name}"
    else:
        assert param_optional(param, py_cls), f"{typedef_name} erroneously requires {xml_param_name}"
        param_cls = py_type_unpack(param_cls)  # unpack Optional[...]

    xml_type = xml_type_format(param.get("type"))
    param_cls_name = py_type_format(param_cls)
    assert param_cls_name == xml_type, f"{typedef_name}.{xml_param_name}:{xml_type}: Invalid type: {param_cls_name}"


@pytest.mark.parametrize(
    ["spec", "node"],
    [
        (spec, node)
        for xml_file, spec in zip(XML_FILES, (accounts.operations, betting.operations, heartbeat))
        for node in xml_nodes(xml_file, "operation")
    ],
    ids=id_check_item,
)
def test_operations(spec, node):
    operation_name = node.get("name")
    for ex in [
        "Subscription",
        "Subscribed",
        "Vendor",
        "Developer",
        "Affiliate",
        "Authorisation",
        "WebApp",
    ]:
        if ex in operation_name:
            pytest.skip("Subscription, developer and vendor operations are not covered by this API implementation")
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
    assert xml_type_format(xml_return_type) == py_type_format(py_type_unpack(operation_cls.return_type))
    xml_error_type = node.findall("parameters/exceptions/exception")[0].get("type")
    assert xml_type_format(xml_error_type) == operation_cls.throws.__name__
    try:
        params_cls = operation_cls.__annotations__["params"]
    except KeyError:
        params_cls = None
    else:
        params_cls_name = compat_type_name(params_cls)
        assert params_cls_name.endswith("Params") or params_cls_name == "ParamsType"  # ParamsType: no arguments
    params = node.findall("parameters/request/parameter")
    for param in params:
        check_typedef_param(param, params_cls, operation_name)


# Little helper functions


def capitalize(val):
    return f"{val[0].upper()}{val[1:]}"


def snake_case(val):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    val = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", val)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", val).lower()


def get_definition(spec, definition):
    if hasattr(spec, definition):
        return getattr(spec, definition)
    if definition in dir(common):
        return getattr(common, definition)
    raise AssertionError(f"{definition} not defined")


def param_name(xml_param):
    paramname = snake_case(xml_param.get("name"))
    if paramname in keyword.kwlist:
        return f"{paramname}_"
    return paramname


def param_deprecated(xml_param):
    desc = (xml_param.findall("description")[0].text or "").strip()
    return desc.startswith("@Deprecated")


def param_defined(xml_param, api_cls):
    paramname = param_name(xml_param)
    return paramname in api_cls.__dict__


def param_mandatory(xml_param):
    return xml_param.get("mandatory") == "true"


def param_optional(xml_param, api_cls):
    paramname = param_name(xml_param)
    type_spec_str = str(api_cls.__annotations__[paramname]).replace("typing.", "")
    return type_spec_str.startswith("Optional")


def py_type_unpack(type_def):
    return type_def.__args__[0]


def py_type_unpack_annotated(type_def):
    if compat_type_name(type_def) == "Annotated":
        return py_type_unpack(type_def)
    return type_def


def py_type_format(type_def):
    type_def_name = compat_type_name(type_def)
    if hasattr(type_def, "__metadata__"):
        return py_type_replace(type_def.__metadata__[0].title)
    if not hasattr(type_def, "__args__"):
        return py_type_replace(type_def_name)
    args = type_def.__args__ if type_def_name != "Optional" else type_def.__args__[:-1]
    args_fmt = ",".join(py_type_format(arg) for arg in args)
    return f"{py_type_replace(type_def_name)}[{args_fmt}]"


PY_TYPE_NAME_REPLACEMENTS = {
    "IntStr": "int",
    "FloatStr": "float",
    "SubscriptionStatus": "str",
    "MarketStatus": "str",
    "MarketId": "str",
    "BetId": "str",
    "SelectionId": "int",
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
}

XML_TYPE_NAME_REPLACEMENTS = {
    "string": "str",
    "i32": "int",
    "i64": "int",
    "double": "float",
    "dateTime": "datetime",
    "map": "dict",
    "SelectionId": "int",
    "MarketId": "str",
    "Date": "datetime",
    "Handicap": "float",
    "BetId": "str",
    "PersistenceType": "str",  # inconsistently used
    "CustomerOrderRef": "str",  # inconsistently used
    "CustomerStrategyRef": "str",  # inconsistently used
    "OrderType": "str",  # inconsistently used
    "OrderStatus": "str",  # inconsistently used
    "Side": "str",  # inconsistently used
    "MarketBettingType": "str",  # inconsistently used
    "Wallet": "str",  # inconsistently used
    "Matches": "list[Match]",
    "(": "[",
    ")": "]",
    ", ": ",",  # inconsistently used
}


def py_type_replace(name):
    # All the special handled types and inconsistencies need some extra care
    return PY_TYPE_NAME_REPLACEMENTS.get(name, name)


def xml_type_format(xml_type_def):
    for xml_type, py_type in XML_TYPE_NAME_REPLACEMENTS.items():
        xml_type_def = xml_type_def.replace(xml_type, py_type)

    # The following replacements need to be done carefully in order not to mess up naming
    if "MarketTypeResult" not in xml_type_def:
        xml_type_def = xml_type_def.replace("MarketType", "str")
    return xml_type_def


def compat_type_name(type_def):
    """Workaround for py3.9 which does not define a __name__ attribute for typing classes."""
    try:
        return type_def.__name__
    except AttributeError:
        # class name looks like _UnionGenericAlias, _AnnotatedAlias
        if type_def.__class__.__name__.startswith("_Annotated"):
            return "Annotated"
        name = type_def.__class__.__name__.lstrip("_").replace("Alias", "").replace("Generic", "")
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
