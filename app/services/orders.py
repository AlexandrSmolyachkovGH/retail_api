from httpx import (
    AsyncClient,
    HTTPStatusError,
    RequestError,
)

from app.exceptions.custom_exceptions import (
    OrderServiceError,
)
from app.schemes.orders import (
    CreateOrderRequest,
    GetOrder,
    PaymentCreateRequest,
)
from app.settings.retailcrm_settings import (
    retail_crm_settings,
)
from app.utils.path_handler import path_handler as ph
from app.utils.request_builder import builder


class OrderService:
    async def get_order(
        self,
        filter_data: GetOrder,
        httpx_client: AsyncClient,
    ) -> dict:
        scheme_data = builder.process_scheme(
            scheme=filter_data,
        )
        params = builder.build_filter_params(
            processed_scheme=scheme_data,
        )
        try:
            response = await httpx_client.get(
                f"{retail_crm_settings.api_url}/{ph.get_ord}",
                params=params,
            )
            response.raise_for_status()

        except (RequestError, HTTPStatusError) as exc:
            try:
                data = exc.response.json()
            except ValueError:
                data = {}
            exc_msg = data.get("errorMsg", "unspecified error")
            raise OrderServiceError(
                exc_msg,
                exc.response.status_code,
            ) from exc

        return response.json()

    async def create_order(
        self,
        order_data: CreateOrderRequest,
        httpx_client: AsyncClient,
    ) -> dict:
        scheme_data = builder.process_scheme(
            scheme=order_data,
        )
        request_data = builder.build_body(
            processed_scheme=scheme_data,
            field_name="order",
        )
        try:
            response = await httpx_client.post(
                f"{retail_crm_settings.api_url}/{ph.create_ord}",
                json=request_data,
            )
            response.raise_for_status()

        except (RequestError, HTTPStatusError) as exc:
            try:
                data = exc.response.json()
            except ValueError:
                data = {}
            exc_msg = data.get("errorMsg", "unspecified error")
            raise OrderServiceError(
                exc_msg,
                exc.response.status_code,
            ) from exc

        return response.json()

    async def create_payment(
        self,
        payment_data: PaymentCreateRequest,
        httpx_client: AsyncClient,
    ) -> dict:
        scheme_data = builder.process_scheme(
            scheme=payment_data,
        )
        request_data = builder.build_body(
            processed_scheme=scheme_data,
            field_name="payment",
        )
        try:
            response = await httpx_client.post(
                f"{retail_crm_settings.api_url}/{ph.create_ord_pay}",
                json=request_data,
            )
            response.raise_for_status()

        except (RequestError, HTTPStatusError) as exc:
            try:
                data = exc.response.json()
            except ValueError:
                data = {}
            exc_msg = data.get("errorMsg", "unspecified error")
            raise OrderServiceError(
                exc_msg,
                exc.response.status_code,
            ) from exc

        return response.json()


order_service = OrderService()
