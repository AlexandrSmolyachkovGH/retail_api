import respx
from fastapi.testclient import TestClient
from httpx import Response

from app.settings.retailcrm_settings import retail_crm_settings
from app.utils.path_handler import path_handler as ph


@respx.mock
def test_get_orders_success(
    client: TestClient,
    get_order_data: dict,
) -> None:
    url = f"{retail_crm_settings.api_url}/{ph.get_ord}"

    respx.get(url).mock(
        return_value=Response(
            status_code=200,
            json=get_order_data,
        ),
    )
    response = client.get("/orders/?limit=20&page=1&customerId=1")
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["pagination"]["currentPage"] == 1
    assert len(data["orders"]) == 1


@respx.mock
def test_create_order_success(
    client: TestClient,
    create_order_data: dict,
) -> None:
    url = f"{retail_crm_settings.api_url}/{ph.create_ord}"

    respx.post(url).mock(
        return_value=Response(
            status_code=200,
            json=create_order_data.get("response_data"),
        ),
    )

    response = client.post(
        "/orders",
        json=create_order_data.get("request_data"),
    )
    data = response.json()

    assert response.status_code == 201
    assert data["success"] is True
    assert data["id"] == 1
    assert data["order"]["number"] == "number123"


@respx.mock
def test_create_payment_success(
    client: TestClient,
    create_payment_data: dict,
) -> None:
    url = f"{retail_crm_settings.api_url}/{ph.create_ord_pay}"

    respx.post(url).mock(
        return_value=Response(
            status_code=201,
            json={
                "success": True,
                "id": 123,
            },
        ),
    )
    response = client.post(
        "/orders/create-payment",
        json=create_payment_data,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["success"] is True
    assert data["id"] == 123
