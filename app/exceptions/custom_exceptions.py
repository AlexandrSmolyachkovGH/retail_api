class CustomerServiceError(Exception):
    """Base class for customer-service-level errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 502,
    ) -> None:
        self.status_code = status_code
        super().__init__(message)


class OrderServiceError(Exception):
    """Base class for customer-service-level errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 502,
    ) -> None:
        self.status_code = status_code
        super().__init__(message)
