from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    CustomerServiceError,
    OrderServiceError,
)
from app.utils.logger_conf import logger


async def customer_service_error_handler(
    request: Request,
    exc: CustomerServiceError,
) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(
        status_code=getattr(
            exc,
            "status_code",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
        content={
            "detail": (
                f"CustomerServiceError: Exception on the RetailCRM side. "
                f"Extra: {str(exc)}"
            ),
        },
    )


async def order_service_error_handler(
    request: Request,
    exc: OrderServiceError,
) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(
        status_code=getattr(
            exc,
            "status_code",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
        content={
            "detail": (
                f"OrderServiceError: Exception on the RetailCRM side. "
                f"Extra: {str(exc)}"
            ),
        },
    )
