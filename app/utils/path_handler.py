from dataclasses import dataclass


@dataclass
class PathHandler:
    """Class for storing information about paths"""

    get_cust: str = "customers"
    create_cust: str = "customers/create"
    get_ord: str = "orders"
    create_ord: str = "orders/create"
    create_ord_pay: str = "orders/payments/create"


path_handler = PathHandler()
