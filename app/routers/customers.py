from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from httpx import AsyncClient

from app.schemes.customers import (
    CreateCustomerRequest,
    CreateCustomerResponse,
    GetCustomerRequest,
)
from app.schemes.customers import GetCustomerResponse as GetCustomer
from app.services.customers import customer_service as service
from app.utils.http_client import get_http_client

customer_router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@customer_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[GetCustomer],
    description="Retrieve customers matching the filters",
)
async def get_customers(
    customer_filters: Annotated[GetCustomerRequest, Query()],
    httpx_client: AsyncClient = Depends(get_http_client),
) -> list[GetCustomer]:
    customer_data = await service.get_customers(
        customer_filters=customer_filters,
        httpx_client=httpx_client,
    )
    if not customer_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No relevant records found",
        )
    return [GetCustomer.model_validate(c) for c in customer_data]


@customer_router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateCustomerResponse,
    description="Create a new customer",
)
async def create_customer(
    customer: CreateCustomerRequest,
    httpx_client: AsyncClient = Depends(get_http_client),
) -> CreateCustomerResponse:
    customer_data = await service.create_customer(
        customer=customer,
        httpx_client=httpx_client,
    )
    return CreateCustomerResponse.model_validate(customer_data)
