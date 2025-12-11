import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def create_customer_data() -> dict:
    return {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "phone": "123456",
    }


@pytest.fixture(scope="session")
def get_customer_data() -> dict:
    return {
        "type": "string",
        "id": 1,
        "isContact": True,
        "createdAt": "string",
        "vip": True,
        "bad": True,
        "site": "string",
        "contragent": {"contragentType": "individual"},
        "tags": ["string"],
        "customFields": [{"additionalProp1": {}}],
        "personalDiscount": 0,
        "marginSumm": 0,
        "totalSumm": 0,
        "averageSumm": 0,
        "ordersCount": 0,
        "segments": [{"additionalProp1": {}}],
        "firstName": "string",
        "lastName": "string",
        "email": "user@example.com",
        "customerSubscriptions": [
            {
                "subscription": {
                    "id": 0,
                    "channel": "string",
                    "name": "string",
                    "code": "string",
                    "active": True,
                    "autoSubscribe": True,
                    "ordering": 0,
                },
                "subscribed": True,
            }
        ],
        "phones": ["string"],
        "mgCustomers": [{"additionalProp1": {}}],
    }


@pytest.fixture(scope="session")
def get_order_data() -> dict:
    return {
        "success": True,
        "pagination": {
            "limit": 20,
            "totalCount": 1,
            "currentPage": 1,
            "totalPageCount": 1,
        },
        "orders": [
            {
                "id": 1,
            }
        ],
    }


@pytest.fixture(scope="session")
def create_order_data() -> dict:
    return {
        "request_data": {
            "number": "number123",
            "site": "test-site",
            "customer": {
                "id": 1,
                "contragent": {
                    "contragentType": "individual",
                },
            },
            "items": [
                {
                    "productName": "Item",
                    "quantity": 1,
                    "price": 100.0,
                }
            ],
        },
        "response_data": {
            "success": True,
            "id": 1,
            "order": {
                "number": "number123",
                "site": "test-site",
                "customer": {
                    "id": 1,
                    "contragent": {
                        "contragentType": "individual",
                    },
                },
            },
        },
    }


@pytest.fixture(scope="session")
def create_payment_data() -> dict:
    return {
        "amount": 100,
        "type": "cash",
        "status": "not-paid",
        "order": {
            "id": 1,
        },
    }
