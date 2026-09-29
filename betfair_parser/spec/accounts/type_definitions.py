from typing import Annotated

from betfair_parser.spec.accounts.enums import (
    AffiliateRelationStatus,
    ItemClass,
    SubscriptionStatus,
    TokenType,
    Wallet,
    WinLose,
)
from betfair_parser.spec.common import BaseMessage, Date, EventId, EventTypeId, MarketType, SelectionId, doc


class ApplicationSubscription(BaseMessage, frozen=True):
    """Application subscription details"""

    subscription_token: Annotated[str, doc("Application key identifier")]
    expiry_date_time: Date | None = None
    expired_date_time: Date | None = None
    created_date_time: Date | None = None
    activation_date_time: Date | None = None
    cancellation_date_time: Date | None = None
    subscription_status: SubscriptionStatus | None = None
    client_reference: str | None = None
    vendor_client_id: str | None = None


class SubscriptionHistory(BaseMessage, frozen=True):
    """Application subscription history details"""

    subscription_token: Annotated[str, doc("Application key identifier")]
    expiry_date_time: Date | None = None
    expired_date_time: Date | None = None
    created_date_time: Date | None = None
    activation_date_time: Date | None = None
    cancellation_date_time: Date | None = None
    subscription_status: SubscriptionStatus | None = None
    client_reference: str | None = None


class SubscriptionTokenInfo(BaseMessage, frozen=True):
    """Subscription token information"""

    subscription_token: str
    activated_date_time: Date | None = None
    expiry_date_time: Date | None = None
    expired_date_time: Date | None = None
    cancellation_date_time: Date | None = None
    subscription_status: SubscriptionStatus | None = None


class AccountSubscription(BaseMessage, frozen=True):
    """Application subscription details"""

    subscription_tokens: list[SubscriptionTokenInfo]
    application_name: str | None = None
    application_version_id: str | None = None


class DeveloperAppVersion(BaseMessage, frozen=True):
    """Describes a version of an external application"""

    owner: Annotated[str, doc("The user who owns the specific version of the application")]
    version_id: Annotated[int, doc("The unique Id of the application version")]
    version: Annotated[str, doc("identifier string such as 1.0, 2.0. Unique for a given application.")]
    application_key: Annotated[str, doc("The unique application key associated with this application version")]

    delayData: Annotated[
        bool,
        doc(
            "Indicates whether the data exposed by platform services as seen by this application key is delayed or "
            "realtime."
        ),
    ]
    subscription_required: Annotated[bool, doc("Indicates whether the application version needs explicit subscription")]

    owner_managed: Annotated[
        bool,
        doc(
            "Indicates whether the application version needs explicit management by the software owner. A value of "
            "false indicates, this is a version meant for personal developer use."
        ),
    ]
    active: Annotated[bool, doc("Indicates whether the application version is currently active")]

    vendor_id: Annotated[
        str | None,
        doc(
            "Public unique string provided to the Vendor that they can use to pass to the Betfair API in order to "
            "identify themselves."
        ),
    ] = None
    vendor_secret: Annotated[
        str | None,
        doc(
            "Private unique string provided to the Vendor that they pass with certain calls to confirm their identity. "
            "Linked to a particular App Key."
        ),
    ] = None


class DeveloperApp(BaseMessage, frozen=True):
    """Describes developer/vendor specific application"""

    app_name: Annotated[str, doc("The unique name of the application")]
    app_id: Annotated[int, doc("A unique id of this application")]
    app_versions: Annotated[list[DeveloperAppVersion], doc("The application versions (including application keys)")]


class AccountFundsResponse(BaseMessage, frozen=True):
    """Response for retrieving available to bet."""

    available_to_bet_balance: float | None = None
    exposure: float | None = None
    retained_commission: Annotated[float | None, doc("Sum of retained commission.")] = None
    exposure_limit: float | None = None

    discount_rate: Annotated[
        float | None,
        doc(
            "User Discount Rate. Please note: Betfair AUS/NZ customers should not rely on this to determine their "
            "discount rates which are now applied at the account level."
        ),
    ] = None
    points_balance: int | None = None

    wallet: Annotated[
        Wallet | None,
        doc("The Betfair wallet name"),
    ] = None


class AccountDetailsResponse(BaseMessage, frozen=True):
    """Response for Account details."""

    currency_code: Annotated[
        str | None,
        doc("Default user currency Code. See Currency Parameters for minimum bet sizes relating to each currency."),
    ] = None
    first_name: str | None = None
    last_name: str | None = None
    locale_code: str | None = None

    region: Annotated[
        str | None,
        doc(
            "Region based on users zip/postcode (ISO 3166-1 alpha-3 format). Defaults to GBR if zip/postcode cannot be "
            "identified."
        ),
    ] = None
    timezone: Annotated[str | None, doc("User Time Zone.")] = None

    discount_rate: Annotated[
        float | None,
        doc(
            "User Discount Rate. Please note: Betfair AUS/NZ customers should not rely on this to determine their "
            "discount rates which are now applied at the account level."
        ),
    ] = None
    points_balance: Annotated[int | None, doc("The Betfair points balance.")] = None
    country_code: Annotated[str | None, doc("The customer's country of residence (ISO 2 Char format)")] = None


class StatementLegacyData(BaseMessage, frozen=True):
    """Summary of a cleared order."""

    avg_price: Annotated[float | None, doc("The average matched price of the bet (null if no part has been matched)")]

    bet_size: Annotated[
        float | None,
        doc("The amount of the stake of your bet. (0 for commission payments or deposit/withdrawals)"),
    ] = None
    bet_type: Annotated[str | None, doc("Back or lay")] = None
    bet_category_type: Annotated[str | None, doc("Exchange, Market on Close SP bet, or Limit on Close SP bet.")] = None
    commission_rate: Annotated[str | None, doc("Commission rate on market")] = None
    event_id: Annotated[
        EventId | None,
        doc("Please note: this is the Id of the market without the associated exchangeId"),
    ] = None
    event_type_id: EventTypeId | None = None

    full_market_name: Annotated[
        str | None,
        doc("Full Market Name. For card payment items, this field contains the card name"),
    ] = None
    gross_bet_amount: Annotated[float | None, doc("The winning amount to which commission is applied.")] = None

    market_name: Annotated[
        str | None,
        doc(
            "Market Name. For card transactions, this field indicates the type of card transaction (deposit, deposit "
            "fee, or withdrawal)."
        ),
    ] = None

    market_type: Annotated[
        MarketType | None,
        doc("Market type. For account deposits and withdrawals, marketType is set to NOT_APPLICABLE."),
    ] = None
    placed_date: Annotated[Date | None, doc("Date and time of bet placement")] = None

    selection_id: Annotated[
        SelectionId | None,
        doc("Id of the selection (this will be the same for the same selection across markets)"),
    ] = None
    selection_name: Annotated[str | None, doc("Name of the selection")] = None
    start_date: Annotated[Date | None, doc("Date and time at the bet portion was settled")] = None
    transaction_type: Annotated[str | None, doc("Debit or credit")] = None
    transaction_id: Annotated[
        int | None,
        doc("The unique reference Id assigned to account deposit and withdrawals."),
    ] = None
    win_lose: WinLose | None = None

    dead_heat_price_divisor: Annotated[
        float | None,
        doc(
            "In the instance of a dead heat, this field will indicate the number of winners involved in the dead heat "
            "(null otherwise)"
        ),
    ] = None

    avg_price_raw: Annotated[
        float | None,
        doc(
            "Currently returns same value as avgPrice. Once released will display the average matched price of the bet "
            "with no rounding applied"
        ),
    ] = None


class StatementItem(BaseMessage, kw_only=True, frozen=True):
    """Summary of a cleared order."""

    ref_id: Annotated[
        str | None,
        doc("An external reference, eg. equivalent to betId in the case of an exchange bet statement item."),
    ] = None

    item_date: Annotated[
        Date,
        doc(
            "The date and time of the statement item, eg. equivalent to settledData for an exchange bet statement "
            "item. (in ISO-8601 format, not translated)"
        ),
    ]
    amount: Annotated[float | None, doc("The amount of money the balance is adjusted by")] = None
    balance: float | None = None

    item_class: Annotated[
        ItemClass | None,
        doc("Class of statement item. This value will determine which set of keys will be included in itemClassData"),
    ] = None
    item_class_data: Annotated[
        dict[str, str] | None,
        doc(
            "Key value pairs describing the current statement item. The set of keys will be determined by the itemClass"
        ),
    ] = None
    legacy_data: Annotated[
        StatementLegacyData | None,
        doc(
            "Set of fields originally returned from APIv6. Provided to facilitate migration from APIv6 to API-NG, and "
            "ultimately onto itemClass and itemClassData"
        ),
    ] = None


class AccountStatementReport(BaseMessage, frozen=True):
    """A container representing search results."""

    account_statement: Annotated[list[StatementItem], doc("The list of statement items returned by your request.")]
    more_available: Annotated[bool, doc("Indicates whether there are further result items beyond this page.")]


class CurrencyRate(BaseMessage, frozen=True):
    currency_code: Annotated[str | None, doc("Three-letter ISO 4217 code")] = None
    rate: Annotated[float | None, doc("Exchange rate for the currency specified in the request")] = None


class AuthorisationResponse(BaseMessage, frozen=True):
    """Wrapper object containing authorisation code and redirect URL for web vendors"""

    authorisation_code: Annotated[str, doc("The authorisation code")]
    redirect_url: Annotated[str, doc("URL to redirect the user to the vendor page")]


class SubscriptionOptions(BaseMessage, frozen=True, rename=None):
    # No rename: SubscriptionOption fields don't use camelCase in Betfair API

    """Wrapper object containing details of how a subscription should be created"""

    subscription_length: Annotated[
        int | None,
        doc(
            "How many days should a created subscription last for. Open-ended subscription created if value not "
            "provided. Relevant only if createdSubscription is true."
        ),
    ] = None

    subscription_token: Annotated[
        str | None,
        doc(
            "An existing subscription token that the caller wishes to be activated instead of creating a new one. "
            "Ignored is createSubscription is true."
        ),
    ] = None
    client_reference: Annotated[str | None, doc("Any client reference for this subscription token request.")] = None


class VendorAccessTokenInfo(BaseMessage, frozen=True, rename=None):
    # No rename: VendorAccessTokenInfo fields don't use camelCase in Betfair API

    """
    Wrapper object containing UserVendorSessionToken, RefreshToken and
    optionally a Subscription Token if one was created
    """

    access_token: Annotated[str, doc("Session token used by web vendors")]
    token_type: Annotated[TokenType, doc("Type of the token")]
    expires_in: Annotated[int, doc("How long until the token expires")]
    refresh_token: Annotated[str, doc("Token used to refresh the session token in future")]

    application_subscription: Annotated[
        ApplicationSubscription,
        doc("Object containing the vendor client id and optionally some subscription information"),
    ]


class VendorDetails(BaseMessage, frozen=True):
    """Wrapper object containing vendor name and redirect url"""

    app_version_id: Annotated[int, doc("Internal id of the application")]
    vendor_name: str
    redirect_url: Annotated[str | None, doc("URL to be redirected to")] = None


class AffiliateRelation(BaseMessage, frozen=True):
    """Wrapper object containing affiliate relation details"""

    status: AffiliateRelationStatus
    vendor_client_id: Annotated[str, doc("ID of user")]
