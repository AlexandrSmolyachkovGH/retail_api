from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import (
    FastAPI,
    status,
)

from app.exceptions.custom_exceptions import (
    CustomerServiceError,
    OrderServiceError,
)
from app.exceptions.exception_handlers import (
    customer_service_error_handler,
    order_service_error_handler,
)
from app.routers.customers import customer_router
from app.routers.orders import order_router
from app.utils.text_samples.root import RootGroupTexts


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator:
    application.state.http_client = httpx.AsyncClient()
    try:
        yield
    finally:
        await application.state.http_client.aclose()


app = FastAPI(lifespan=lifespan)

# Include Routers
app.include_router(router=customer_router)
app.include_router(router=order_router)

# Exception Handlers
app.add_exception_handler(
    exc_class_or_status_code=CustomerServiceError,
    handler=customer_service_error_handler,
)
app.add_exception_handler(
    exc_class_or_status_code=OrderServiceError,
    handler=order_service_error_handler,
)


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["root"],
    description="API representation and common links",
)
async def get_root_page() -> dict:
    return {
        "title": RootGroupTexts.get_root_title(),
        "description": RootGroupTexts.get_root_description(),
        "paths": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "health-check": "/health",
        },
    }


@app.get(
    path="/health",
    status_code=status.HTTP_200_OK,
    tags=["root"],
    description="Router for checking service status",
)
async def check_liveness() -> dict:
    return {"status": "UP"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8086,
        reload=True,
    )
