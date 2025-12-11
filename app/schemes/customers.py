from datetime import date
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class ContragentEnum(str, Enum):
    enterpreneur = "enterpreneur"
    individual = "individual"
    legal_entity = "legal-entity"


class CustomerAddress(BaseModel):
    countryIso: str | None = Field(
        description="client country",
        default=None,
    )
    region: str | None = Field(
        description="client region",
        default=None,
    )
    city: str | None = Field(
        description="client city",
        default=None,
    )
    street: str | None = Field(
        description="client street name",
        default=None,
    )
    building: str | None = Field(
        description="client building number",
        default=None,
    )
    flat: str | None = Field(
        description="client flat number",
        default=None,
    )
    text: str | None = Field(
        description="text representation of address",
        default=None,
    )


class CreateCustomerRequest(BaseModel):
    firstName: str = Field(
        description="client name",
    )
    lastName: str = Field(
        description="client's last name",
    )
    email: EmailStr = Field(
        description="client email",
    )
    phone: str | None = Field(
        description="client phone number",
        default=None,
    )
    birthday: str | None = Field(
        description="client phone number",
        default=None,
    )
    vip: bool = Field(
        description="vip client status",
        default=False,
    )
    customFields: dict | None = Field(
        description="extra fields",
        default=None,
    )
    address: CustomerAddress | None = Field(
        description="client address",
        default=None,
    )


class CreateCustomerResponse(BaseModel):
    success: bool = Field(
        description="client creation success status",
    )
    id: int = Field(
        description="id of created user",
    )


class Pagination(BaseModel):
    limit: int = Field(
        description="quantity of records on the page (>=20)",
        default=20,
        examples=[20, 50, 100],
    )
    page: int = Field(
        ge=1,
        description="initial page number",
        default=1,
    )


class GetCustomerRequest(Pagination):
    name: str | None = Field(
        max_length=255,
        description="filtering by first, second name, phone fields",
        default=None,
    )
    email: EmailStr | None = Field(
        max_length=255,
        description="email for filtering",
        default=None,
    )
    dateFrom: date | None = Field(
        description="min date to filter by createdAt field",
        default=None,
    )
    dateTo: date | None = Field(
        description="max date to filter by createdAt field",
        default=None,
    )

    model_config = ConfigDict(
        json_encoders={
            date: (
                lambda v: v.strftime('%Y-%m-%d') if isinstance(v, date) else v
            )
        }
    )


class Subscription(BaseModel):
    id: int = Field(
        description="subscription id",
    )
    channel: str = Field(
        description="subscription channel",
    )
    name: str = Field(
        description="subscription title",
    )
    code: str = Field(
        description="subscription code",
    )
    active: bool = Field(
        description="subscription status",
    )
    autoSubscribe: bool = Field(
        description="auto-subscription status",
    )
    ordering: int = Field(
        description="subscription order",
    )


class CustomerSubscription(BaseModel):
    subscription: Subscription = Field(
        description="subscription scheme",
    )
    subscribed: bool = Field(
        description="status of being subscribed",
    )


class Contragent(BaseModel):
    contragentType: ContragentEnum = Field(
        description="contragent type",
        default=ContragentEnum.individual,
    )


class CustomerIdentifier(BaseModel):
    id: int = Field(
        description="client id",
    )
    contragent: Contragent = Field(
        description="contaragent info",
    )


class GetCustomerResponse(BaseModel):
    type: str = Field(
        description="client type",
    )
    id: int = Field(
        description="client id",
    )
    isContact: bool = Field(
        description="is the client a contact",
    )
    createdAt: str = Field(
        description="date and time of creation",
    )
    vip: bool = Field(
        description="vip client status",
    )
    bad: bool = Field(
        description="is the client considered bad",
    )
    site: str = Field(
        description="client website",
    )
    contragent: Contragent = Field(
        description="client contragent",
    )
    tags: list[str] = Field(
        description="client tags",
    )
    customFields: list[dict] = Field(
        description="client custom fields",
    )
    personalDiscount: float = Field(
        description="client discounts",
    )
    marginSumm: float = Field(
        description="margin amount for client orders",
    )
    totalSumm: float = Field(
        description="total amount for client orders",
    )
    averageSumm: float = Field(
        description="average amount for client orders",
    )
    ordersCount: int = Field(
        description="number of client orders",
    )
    segments: list[dict] = Field(
        description="client segments",
    )
    firstName: str | None = Field(
        default=None,
        description="client name",
    )
    lastName: str | None = Field(
        default=None,
        description="client's last name",
    )
    email: EmailStr | None = Field(
        default=None,
        description="client email",
    )
    customerSubscriptions: list[CustomerSubscription] = Field(
        description="client subscriptions",
    )
    phones: list[str] = Field(
        description="client phones",
    )
    mgCustomers: list[dict] = Field(
        description="client messages",
    )
