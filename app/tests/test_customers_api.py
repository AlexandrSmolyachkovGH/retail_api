import respx
from fastapi.testclient import TestClient
from httpx import Response

from app.settings.retailcrm_settings import retail_crm_settings
from app.utils.path_handler import path_handler as ph


@respx.mock
def test_create_customer_success(
    client: TestClient,
    create_customer_data: dict,
) -> None:
    url = f"{retail_crm_settings.api_url}/{ph.create_cust}"

    respx.post(url).mock(
        return_value=Response(
            status_code=200,
            json={
                "success": True,
                "id": 123,
                "customer": {"id": 123},
            },
        ),
    )

    response = client.post(
        "/customers/create",
        json=create_customer_data,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["success"] is True
    assert data["id"] == 123


@respx.mock
def test_get_customers_success(
    client: TestClient,
    get_customer_data: dict,
) -> None:
    url = f"{retail_crm_settings.api_url}/{ph.get_cust}"

    respx.get(url).mock(
        return_value=Response(
            status_code=200,
            json={
                "customers": [get_customer_data],
            },
        ),
    )
    response = client.get("/customers/?limit=20&page=1")
    data = response.json()
    item = data[0]

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert item["id"] == 1
    assert item["firstName"] == "string"
    assert item["email"] == "user@example.com"
