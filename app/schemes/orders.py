from enum import Enum

from pydantic import (
    BaseModel,
    Field,
)

from app.schemes.customers import (
    CustomerIdentifier,
    Pagination,
)


class PaymentStatusEnum(str, Enum):
    not_paid = "not-paid"
    invoice = "invoice"
    wait_approved = "wait-approved"
    payment_start = "payment-start"
    canceled = "canceled"
    fail = "fail"
    paid = "paid"
    returned = "returned"


class PaymentTypeEnum(str, Enum):
    cash = "cash"
    bank_card = "bank-card"
    e_money = "e-money"
    bank_transfer = "bank-transfer"
    credit = "credit"


class ItemScheme(BaseModel):
    productName: str = Field(
        description="item title",
    )
    quantity: int = Field(
        description="number of items",
    )
    price: float = Field(
        description="item price",
    )


class Order(BaseModel):
    number: str = Field(
        description="order number",
    )
    site: str | None = Field(
        description="site",
        default=None,
    )
    customer: CustomerIdentifier = Field(
        description="client identification",
    )


class CreateOrderRequest(Order):
    items: list[ItemScheme] = Field(
        description="items added to the order",
    )


class CreateOrderResponse(BaseModel):
    success: bool = Field(
        description="status of order creation",
    )
    id: int = Field(
        description="created order id",
    )
    order: Order = Field(
        description="order content",
    )


class GetOrder(Pagination):
    customerId: int = Field(
        description="customer id for filtering",
    )


class GetOrderResponse(BaseModel):
    success: bool = Field(
        description="response success status",
    )
    pagination: dict = Field(
        description="pagination info",
    )
    orders: list[dict] = Field(
        description="list of orders",
    )


class OrderByID(BaseModel):
    id: int = Field(
        description="order id",
    )


class PaymentCreateRequest(BaseModel):
    amount: float = Field(
        description="order payment amount",
    )
    type: PaymentTypeEnum = Field(
        description="payment option types",
        default=PaymentTypeEnum.cash,
    )
    status: PaymentStatusEnum = Field(
        description="status of the payment",
        default=PaymentStatusEnum.not_paid,
    )
    order: OrderByID = Field(description="reference to the order")


class PaymentCreateResponse(BaseModel):
    success: bool = Field(
        description="status of payment creation",
    )
    id: int = Field(
        description="created payment id",
    )
