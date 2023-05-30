from betfair_parser.spec.identity import LoginResponse


def test_login_response():
    resp = b'{"token":"","product":"","status":"FAIL","error":"INPUT_VALIDATION_ERROR"}'
    assert LoginResponse.parse(resp)
