from app.schemes.customers import GetCustomerRequest
from app.utils.path_handler import path_handler as ph
from app.utils.request_builder import builder


def test_request_builder() -> None:
    test_data = GetCustomerRequest(
        email="email.example@gmail.com",
    )
    processed_data = builder.process_scheme(test_data)

    assert processed_data.get("email", None) == test_data.email
    assert processed_data.get("name", None) is None

    filters = builder.build_filter_params(processed_data)

    assert isinstance(filters, dict)
    assert filters.get("page") == 1
    assert filters.get("filter[email]") == test_data.email

    body = builder.build_body(processed_data, field_name="test")

    assert isinstance(body, dict)
    assert body.get("apiKey", None) is not None
    assert body.get("test", None) is not None


def test_path_handler() -> None:
    assert ph.create_cust == "customers/create"
    assert ph.get_cust == "customers"
    assert ph.create_ord == "orders/create"
    assert ph.get_ord == "orders"
    assert ph.create_ord_pay == "orders/payments/create"
