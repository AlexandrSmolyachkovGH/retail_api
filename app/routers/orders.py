from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from httpx import AsyncClient

from app.schemes.orders import (
    CreateOrderRequest,
    CreateOrderResponse,
    GetOrder,
    GetOrderResponse,
    PaymentCreateRequest,
    PaymentCreateResponse,
)
from app.services.orders import order_service
from app.utils.http_client import get_http_client

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@order_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=GetOrderResponse,
    description="Retrieve orders matching the filters",
)
async def get_orders(
    filter_data: Annotated[GetOrder, Query()],
    httpx_client: AsyncClient = Depends(get_http_client),
) -> GetOrderResponse:
    order_data = await order_service.get_order(
        filter_data=filter_data,
        httpx_client=httpx_client,
    )
    if not order_data.get("success"):
        error_msg = order_data.get("errors", None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"errorMsg:{error_msg if error_msg else None}",
        )
    return GetOrderResponse.model_validate(order_data)


@order_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateOrderResponse,
    description="Create a new order for a customer",
)
async def create_order(
    order_data: CreateOrderRequest,
    httpx_client: AsyncClient = Depends(get_http_client),
) -> CreateOrderResponse:
    created_order = await order_service.create_order(
        order_data=order_data,
        httpx_client=httpx_client,
    )
    if not created_order.get("success"):
        error_msg = created_order.get("errors", None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"errorMsg:{error_msg if error_msg else None}",
        )
    return CreateOrderResponse.model_validate(created_order)


@order_router.post(
    path="/create-payment",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentCreateResponse,
    description="Create a new payment method for an order",
)
async def create_payment(
    payment_data: PaymentCreateRequest,
    httpx_client: AsyncClient = Depends(get_http_client),
) -> PaymentCreateResponse:
    payment = await order_service.create_payment(
        payment_data=payment_data,
        httpx_client=httpx_client,
    )
    if not payment.get("success"):
        error_msg = payment.get("errors", None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"errorMsg:{error_msg if error_msg else None}",
        )
    return PaymentCreateResponse.model_validate(payment)
