![betfair_parser logo](https://github.com/limx0/betfair_parser/assets/2386612/10d602a6-627c-48f1-8145-2f14232a8320)

[![GitHub Build Status](https://img.shields.io/github/actions/workflow/status/limx0/betfair_parser/build.yml?branch=main&logo=github)](https://github.com/limx0/betfair_parser/actions)
[![PyPI](https://img.shields.io/pypi/v/betfair_parser.svg?style=flat)](https://pypi.org/project/betfair_parser/)
![Python Version](https://img.shields.io/pypi/pyversions/betfair_parser)
![License](https://img.shields.io/github/license/limx0/betfair_parser)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# betfair_parser

A simple and fast betfair parser. Why you might like this library:

- Complete: All betfair (non-vendor) client API included
- Conventions: The API strictly follows pythonic naming conventions
- Consistency: All data is type checked, API requests as well as responses
- Comfort: All betfair enums and type definitions are included, to support IDE syntax completion
- Clear errors: API errors don't just throw cryptic codes, but contain documentation about that error
- Compatible: Use it with any HTTP library you like, including async libraries
- Cheetah fast: Thanks to the magic of [msgspec](https://github.com/jcrist/msgspec), megabytes of input
parse in milliseconds


## Usage

`betfair_parser` is built out of API building blocks, that can be used with any HTTP client
you like. All API operations provide `.headers()`, `.body()` and a `.parse_response()` method.

The [`client`](https://github.com/limx0/betfair_parser/blob/main/betfair_parser/client.py) module
contains a sample, minimalistic client implementation. It may be used as is with any `requests`-compatible
HTTP client or serve as an example, how to integrate `betfair_parser` with other HTTP clients.

```python
import requests
from betfair_parser import client
from betfair_parser.spec import accounts, betting

session = requests.Session()  # or anything similar like httpx.Client()
client.login(session, "username", "password", "app_key")
client.request(session, accounts.GetAccountFunds.with_params())
# AccountFundsResponse(available_to_bet_balance=10000.0, exposure=0.0,
# retained_commission=0.0, exposure_limit=-10000.0, discount_rate=0.0,
# points_balance=10, wallet=<Wallet.UK: 'UK'>)

# Request with an invalid wallet parameter:
client.request(session, accounts.GetAccountFunds.with_params(wallet="AUS"))
# >>> AccountAPINGException: INVALID_PARAMETERS: Problem parsing the parameters,
#     or a mandatory parameter was not found

client.request(session, betting.ListCurrentOrders.with_params())
# CurrentOrderSummaryReport(current_orders=[], more_available=False)

# Support for other countries
from betfair_parser.endpoints import endpoint
endpoint_cfg = endpoint("ITA")  # alpha-3 code
client.login(session, "username", "password", "app_key", endpoints=endpoint_cfg)
```

See [`test_live.py`](https://github.com/limx0/betfair_parser/blob/main/tests/integration/test_live.py)
for more API call examples.


## Releasing

Releases are published automatically when a tag is pushed to GitHub.

```bash
# Set next version number
export RELEASE=x.x.x

# Create tags
git commit --allow-empty -m "Release $RELEASE"
git tag -a $RELEASE -m "Version $RELEASE"

# Push
git push --tags
git push
```
