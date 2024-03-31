from typing import Optional

from betfair_parser.spec.accounts.enums import (
    AffiliateRelationStatus,
    ItemClass,
    SubscriptionStatus,
    TokenType,
    Wallet,
    WinLose,
)
from betfair_parser.spec.common import BaseMessage, Date


class ApplicationSubscription(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Application subscription details"""

    subscription_token: str  # Application key identifier
    expiry_date_time: Optional[Date] = None
    expired_date_time: Optional[Date] = None
    created_date_time: Optional[Date] = None
    activation_date_time: Optional[Date] = None
    cancellation_date_time: Optional[Date] = None
    subscription_status: Optional[SubscriptionStatus] = None
    client_reference: Optional[str] = None
    vendor_client_id: Optional[str] = None


class SubscriptionHistory(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Application subscription history details"""

    subscription_token: str  # Application key identifier
    expiry_date_time: Optional[Date] = None
    expired_date_time: Optional[Date] = None
    created_date_time: Optional[Date] = None
    activation_date_time: Optional[Date] = None
    cancellation_date_time: Optional[Date] = None
    subscription_status: Optional[SubscriptionStatus] = None
    client_reference: Optional[str] = None


class SubscriptionTokenInfo(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Subscription token information"""

    subscription_token: str
    activated_date_time: Optional[Date] = None
    expiry_date_time: Optional[Date] = None
    expired_date_time: Optional[Date] = None
    cancellation_date_time: Optional[Date] = None
    subscription_status: Optional[SubscriptionStatus] = None


class AccountSubscription(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Application subscription details"""

    subscription_tokens: list[SubscriptionTokenInfo]
    application_name: Optional[str] = None
    application_version_id: Optional[str] = None


class DeveloperAppVersion(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Describes a version of an external application"""

    owner: str  # The user who owns the specific version of the application
    version_id: int  # The unique Id of the application version
    version: str  # identifier string such as 1.0, 2.0. Unique for a given application.
    application_key: str  # The unique application key associated with this application version

    # Indicates whether the data exposed by platform services as seen by this
    # application key is delayed or realtime.
    delayData: bool
    subscription_required: bool  # Indicates whether the application version needs explicit subscription

    # Indicates whether the application version needs explicit management by the software owner.
    # A value of false indicates, this is a version meant for personal developer use.
    owner_managed: bool
    active: bool  # Indicates whether the application version is currently active

    # Public unique string provided to the Vendor that they can use to pass to the
    # Betfair API in order to identify themselves.
    vendor_id: Optional[str] = None
    # Private unique string provided to the Vendor that they pass with certain calls
    # to confirm their identity. Linked to a particular App Key.
    vendor_secret: Optional[str] = None


class DeveloperApp(BaseMessage, frozen=True):
    """Describes developer/vendor specific application"""

    app_name: str  # The unique name of the application
    app_id: int  # A unique id of this application
    app_versions: list[DeveloperAppVersion]  # The application versions (including application keys)


class AccountFundsResponse(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Response for retrieving available to bet."""

    available_to_bet_balance: Optional[float] = None
    exposure: Optional[float] = None
    retained_commission: Optional[float] = None  # Sum of retained commission.
    exposure_limit: Optional[float] = None

    # User Discount Rate. Please note: Betfair AUS/NZ customers should not rely on this to determine
    # their discount rates which are now applied at the account level.
    discount_rate: Optional[float] = None
    points_balance: Optional[int] = None

    # This is not documented in the API description, but seems to be present anyway
    wallet: Optional[Wallet] = None


class AccountDetailsResponse(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Response for Account details."""

    # Default user currency Code. See Currency Parameters for minimum bet sizes relating to each currency.
    currency_code: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    locale_code: Optional[str] = None

    # Region based on users zip/postcode (ISO 3166-1 alpha-3 format). Defaults to GBR if
    # zip/postcode cannot be identified.
    region: Optional[str] = None
    timezone: Optional[str] = None  # User Time Zone.

    # User Discount Rate.   Please note:  Betfair AUS/NZ customers should not rely on this to
    # determine their discount rates which are now applied at the account level.
    discount_rate: Optional[float] = None
    points_balance: Optional[int] = None  # The Betfair points balance.
    country_code: Optional[str] = None  # The customer's country of residence (ISO 2 Char format)


class StatementLegacyData(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Summary of a cleared order."""

    avg_price: Optional[float]  # The average matched price of the bet (null if no part has been matched)

    # The amount of the stake of your bet. (0 for commission payments or deposit/withdrawals)
    bet_size: Optional[float] = None
    bet_type: Optional[str] = None  # Back or lay
    bet_category_type: Optional[str] = None  # Exchange, Market on Close SP bet, or Limit on Close SP bet.
    commission_rate: Optional[str] = None  # Commission rate on market
    event_id: Optional[int] = None  # Please note: this is the Id of the market without the associated exchangeId
    event_type_id: Optional[int] = None

    # Full Market Name. For card payment items, this field contains the card name
    full_market_name: Optional[str] = None
    gross_bet_amount: Optional[float] = None  # The winning amount to which commission is applied.

    # Market Name. For card transactions, this field indicates the type of card
    # transaction (deposit, deposit fee, or withdrawal).
    market_name: Optional[str] = None

    # Market type. For account deposits and withdrawals, marketType is set to NOT_APPLICABLE.
    market_type: Optional[str] = None
    placed_date: Optional[Date] = None  # Date and time of bet placement

    # Id of the selection (this will be the same for the same selection across markets)
    selection_id: Optional[int] = None
    selection_name: Optional[str] = None  # Name of the selection
    start_date: Optional[Date] = None  # Date and time at the bet portion was settled
    transaction_type: Optional[str] = None  # Debit or credit
    transaction_id: Optional[int] = None  # The unique reference Id assigned to account deposit and withdrawals.
    win_lose: Optional[WinLose] = None

    # In the instance of a dead heat, this field will indicate the number of winners
    # involved in the dead heat (null otherwise)
    dead_heat_price_divisor: Optional[float] = None

    # Currently returns same value as avgPrice. Once released will display the average matched
    # price of the bet with no rounding applied
    avg_price_raw: Optional[float] = None


class StatementItem(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Summary of a cleared order."""

    # An external reference, eg. equivalent to betId in the case of an exchange bet statement item.
    ref_id: Optional[str] = None

    # The date and time of the statement item, eg. equivalent to settledData for an exchange
    # bet statement item. (in ISO-8601 format, not translated)
    item_date: Date
    amount: Optional[float] = None  # The amount of money the balance is adjusted by
    balance: Optional[float] = None

    # Class of statement item. This value will determine which set of keys will be included in itemClassData
    item_class: Optional[ItemClass] = None
    # Key value pairs describing the current statement item. The set of keys will be
    # determined by the itemClass
    item_class_data: Optional[dict[str, str]] = None
    # Set of fields originally returned from APIv6. Provided to facilitate migration from
    # APIv6 to API-NG, and ultimately onto itemClass and itemClassData
    legacy_data: Optional[StatementLegacyData] = None


class AccountStatementReport(BaseMessage, frozen=True):
    """A container representing search results."""

    account_statement: list[StatementItem]  # The list of statement items returned by your request.
    more_available: bool  # Indicates whether there are further result items beyond this page.


class CurrencyRate(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    currency_code: Optional[str] = None  # Three-letter ISO 4217 code
    rate: Optional[float] = None  # Exchange rate for the currency specified in the request


class AuthorisationResponse(BaseMessage, frozen=True):
    """Wrapper object containing authorisation code and redirect URL for web vendors"""

    authorisation_code: str  # The authorisation code
    redirect_url: str  # URL to redirect the user to the vendor page


class SubscriptionOptions(BaseMessage, frozen=True, omit_defaults=True, repr_omit_defaults=True, rename=None):
    # No rename: SubscriptionOption fields don't use camelCase in Betfair API

    """Wrapper object containing details of how a subscription should be created"""

    # How many days should a created subscription last for. Open-ended subscription created
    # if value not provided. Relevant only if createdSubscription is true.
    subscription_length: Optional[int] = None

    # An existing subscription token that the caller wishes to be activated instead of creating a new one.
    # Ignored is createSubscription is true.
    subscription_token: Optional[str] = None
    client_reference: Optional[str] = None  # Any client reference for this subscription token request.


class VendorAccessTokenInfo(BaseMessage, frozen=True, rename=None):
    # No rename: VendorAccessTokenInfo fields don't use camelCase in Betfair API

    """
    Wrapper object containing UserVendorSessionToken, RefreshToken and
    optionally a Subscription Token if one was created
    """

    access_token: str  # Session token used by web vendors
    token_type: TokenType  # Type of the token
    expires_in: int  # How long until the token expires
    refresh_token: str  # Token used to refresh the session token in future

    # Object containing the vendor client id and optionally some subscription information
    application_subscription: ApplicationSubscription


class VendorDetails(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Wrapper object containing vendor name and redirect url"""

    app_version_id: int  # Internal id of the application
    vendor_name: str
    redirect_url: Optional[str] = None  # URL to be redirected to


class AffiliateRelation(BaseMessage, frozen=True):
    """Wrapper object containing affiliate relation details"""

    status: AffiliateRelationStatus
    vendor_client_id: str  # ID of user
