from typing import Any

from httpx import (
    AsyncClient,
    HTTPStatusError,
    RequestError,
)

from app.exceptions.custom_exceptions import CustomerServiceError
from app.schemes.customers import (
    CreateCustomerRequest,
    GetCustomerRequest,
)
from app.settings.retailcrm_settings import (
    retail_crm_settings,
)
from app.utils.path_handler import path_handler as ph
from app.utils.request_builder import builder


class CustomerService:
    async def get_customers(
        self,
        customer_filters: GetCustomerRequest,
        httpx_client: AsyncClient,
    ) -> list[dict[str, Any]]:
        processed_scheme = builder.process_scheme(
            scheme=customer_filters,
        )
        params = builder.build_filter_params(
            processed_scheme=processed_scheme,
        )
        try:
            response = await httpx_client.get(
                f"{retail_crm_settings.api_url}/{ph.get_cust}",
                params=params,
            )
            response.raise_for_status()

        except (RequestError, HTTPStatusError) as exc:
            try:
                data = exc.response.json()
            except ValueError:
                data = {}
            exc_msg = data.get("errorMsg", "unspecified error")
            raise CustomerServiceError(
                exc_msg,
                exc.response.status_code,
            ) from exc

        return response.json().get("customers", [])

    async def create_customer(
        self,
        customer: CreateCustomerRequest,
        httpx_client: AsyncClient,
    ) -> dict:
        scheme_data = builder.process_scheme(
            scheme=customer,
        )
        request_data = builder.build_body(
            processed_scheme=scheme_data,
            field_name="customer",
        )
        try:
            response = await httpx_client.post(
                f"{retail_crm_settings.api_url}/{ph.create_cust}",
                json=request_data,
            )
            response.raise_for_status()

        except (RequestError, HTTPStatusError) as exc:
            try:
                data = exc.response.json()
            except ValueError:
                data = {}
            exc_msg = data.get("errorMsg", "unspecified error")
            raise CustomerServiceError(
                exc_msg,
                exc.response.status_code,
            ) from exc

        return response.json()


customer_service = CustomerService()
