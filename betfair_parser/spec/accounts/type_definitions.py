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


class ApplicationSubscription(BaseMessage, frozen=True):
    """Application subscription details"""

    subscriptionToken: str  # Application key identifier
    expiryDateTime: Optional[Date] = None
    expiredDateTime: Optional[Date] = None
    createdDateTime: Optional[Date] = None
    activationDateTime: Optional[Date] = None
    cancellationDateTime: Optional[Date] = None
    subscriptionStatus: Optional[SubscriptionStatus] = None
    clientReference: Optional[str] = None
    vendorClientId: Optional[str] = None


class SubscriptionHistory(BaseMessage, frozen=True):
    """Application subscription history details"""

    subscriptionToken: str  # Application key identifier
    expiryDateTime: Optional[Date] = None
    expiredDateTime: Optional[Date] = None
    createdDateTime: Optional[Date] = None
    activationDateTime: Optional[Date] = None
    cancellationDateTime: Optional[Date] = None
    subscriptionStatus: Optional[SubscriptionStatus] = None
    clientReference: Optional[str] = None


class SubscriptionTokenInfo(BaseMessage, frozen=True):
    """Subscription token information"""

    subscriptionToken: str
    activatedDateTime: Optional[Date] = None
    expiryDateTime: Optional[Date] = None
    expiredDateTime: Optional[Date] = None
    cancellationDateTime: Optional[Date] = None
    subscriptionStatus: Optional[SubscriptionStatus] = None


class AccountSubscription(BaseMessage, frozen=True):
    """Application subscription details"""

    subscriptionTokens: list[SubscriptionTokenInfo]
    applicationName: Optional[str] = None
    applicationVersionId: Optional[str] = None


class DeveloperAppVersion(BaseMessage, frozen=True):
    """Describes a version of an external application"""

    owner: str  # The user who owns the specific version of the application
    versionId: int  # The unique Id of the application version
    version: str  # identifier string such as 1.0, 2.0. Unique for a given application.
    applicationKey: str  # The unique application key associated with this application version

    # Indicates whether the data exposed by platform services as seen by this
    # application key is delayed or realtime.
    delayData: bool
    subscriptionRequired: bool  # Indicates whether the application version needs explicit subscription

    # Indicates whether the application version needs explicit management by the software owner.
    # A value of false indicates, this is a version meant for personal developer use.
    ownerManaged: bool
    active: bool  # Indicates whether the application version is currently active

    # Public unique string provided to the Vendor that they can use to pass to the
    # Betfair API in order to identify themselves.
    vendorId: Optional[str] = None
    # Private unique string provided to the Vendor that they pass with certain calls
    # to confirm their identity. Linked to a particular App Key.
    vendorSecret: Optional[str] = None


class DeveloperApp(BaseMessage, frozen=True):
    """Describes developer/vendor specific application"""

    appName: str  # The unique name of the application
    appId: int  # A unique id of this application
    appVersions: list[DeveloperAppVersion]  # The application versions (including application keys)


class AccountFundsResponse(BaseMessage, frozen=True):
    """Response for retrieving available to bet."""

    availableToBetBalance: Optional[float] = None
    exposure: Optional[float] = None
    retainedCommission: Optional[float] = None  # Sum of retained commission.
    exposureLimit: Optional[float] = None

    # User Discount Rate. Please note: Betfair AUS/NZ customers should not rely on this to determine
    # their discount rates which are now applied at the account level.
    discountRate: Optional[float] = None
    pointsBalance: Optional[int] = None

    # This is NOT documented in the API description, but seems to be present at least int recorded data
    wallet: Optional[Wallet] = None


class AccountDetailsResponse(BaseMessage, frozen=True):
    """Response for Account details."""

    # Default user currency Code. See Currency Parameters for minimum bet sizes relating to each currency.
    currencyCode: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    localeCode: Optional[str] = None

    # Region based on users zip/postcode (ISO 3166-1 alpha-3 format). Defaults to GBR if
    # zip/postcode cannot be identified.
    region: Optional[str] = None
    timezone: Optional[str] = None  # User Time Zone.

    # User Discount Rate.   Please note:  Betfair AUS/NZ customers should not rely on this to
    # determine their discount rates which are now applied at the account level.
    discountRate: Optional[float] = None
    pointsBalance: Optional[int] = None  # The Betfair points balance.
    countryCode: Optional[str] = None  # The customer's country of residence (ISO 2 Char format)


class StatementLegacyData(BaseMessage, frozen=True):
    """Summary of a cleared order."""

    avgPrice: Optional[float]  # The average matched price of the bet (null if no part has been matched)

    # The amount of the stake of your bet. (0 for commission payments or deposit/withdrawals)
    betSize: Optional[float] = None
    betType: Optional[str] = None  # Back or lay
    betCategoryType: Optional[str] = None  # Exchange, Market on Close SP bet, or Limit on Close SP bet.
    commissionRate: Optional[str] = None  # Commission rate on market
    eventId: Optional[int] = None  # Please note: this is the Id of the market without the associated exchangeId
    eventTypeId: Optional[int] = None

    # Full Market Name. For card payment items, this field contains the card name
    fullMarketName: Optional[str] = None
    grossBetAmount: Optional[float] = None  # The winning amount to which commission is applied.

    # Market Name. For card transactions, this field indicates the type of card
    # transaction (deposit, deposit fee, or withdrawal).
    marketName: Optional[str] = None

    # Market type. For account deposits and withdrawals, marketType is set to NOT_APPLICABLE.
    marketType: Optional[str] = None
    placedDate: Optional[Date] = None  # Date and time of bet placement

    # Id of the selection (this will be the same for the same selection across markets)
    selectionId: Optional[int] = None
    selectionName: Optional[str] = None  # Name of the selection
    startDate: Optional[Date] = None  # Date and time at the bet portion was settled
    transactionType: Optional[str] = None  # Debit or credit
    transactionId: Optional[int] = None  # The unique reference Id assigned to account deposit and withdrawals.
    winLose: Optional[WinLose] = None

    # In the instance of a dead heat, this field will indicate the number of winners
    # involved in the dead heat (null otherwise)
    deadHeatPriceDivisor: Optional[float] = None

    # Currently returns same value as avgPrice. Once released will display the average matched
    # price of the bet with no rounding applied
    avgPriceRaw: Optional[float] = None


class StatementItem(BaseMessage, kw_only=True, frozen=True):
    """Summary of a cleared order."""

    # An external reference, eg. equivalent to betId in the case of an exchange bet statement item.
    refId: Optional[str] = None

    # The date and time of the statement item, eg. equivalent to settledData for an exchange
    # bet statement item. (in ISO-8601 format, not translated)
    itemDate: Date
    amount: Optional[float] = None  # The amount of money the balance is adjusted by
    balance: Optional[float] = None

    # Class of statement item. This value will determine which set of keys will be included in itemClassData
    itemClass: Optional[ItemClass] = None
    # Key value pairs describing the current statement item. The set of keys will be
    # determined by the itemClass
    itemClassData: Optional[dict[str, str]] = None
    # Set of fields originally returned from APIv6. Provided to facilitate migration from
    # APIv6 to API-NG, and ultimately onto itemClass and itemClassData
    legacyData: Optional[StatementLegacyData] = None


class AccountStatementReport(BaseMessage, frozen=True):
    """A container representing search results."""

    accountStatement: list[StatementItem]  # The list of statement items returned by your request.
    moreAvailable: bool  # Indicates whether there are further result items beyond this page.


class CurrencyRate(BaseMessage, frozen=True):
    currencyCode: Optional[str] = None  # Three-letter ISO 4217 code
    rate: Optional[float] = None  # Exchange rate for the currency specified in the request


class AuthorisationResponse(BaseMessage, frozen=True):
    """Wrapper object containing authorisation code and redirect URL for web vendors"""

    authorisationCode: str  # The authorisation code
    redirectUrl: str  # URL to redirect the user to the vendor page


class SubscriptionOptions(BaseMessage, frozen=True):
    """Wrapper object containing details of how a subscription should be created"""

    # How many days should a created subscription last for. Open-ended subscription created
    # if value not provided. Relevant only if createdSubscription is true.
    subscription_length: Optional[int] = None

    # An existing subscription token that the caller wishes to be activated instead of creating a new one.
    # Ignored is createSubscription is true.
    subscription_token: Optional[str] = None
    client_reference: Optional[str] = None  # Any client reference for this subscription token request.


class VendorAccessTokenInfo(BaseMessage, frozen=True):
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


class VendorDetails(BaseMessage, frozen=True):
    """Wrapper object containing vendor name and redirect url"""

    appVersionId: int  # Internal id of the application
    vendorName: str
    redirectUrl: Optional[str] = None  # URL to be redirected to


class AffiliateRelation(BaseMessage, frozen=True):
    """Wrapper object containing affiliate relation details"""

    vendorClientId: str  # ID of user
    status: AffiliateRelationStatus
