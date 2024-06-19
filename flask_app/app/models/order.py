from typing import Optional, List, Dict, Any, Union

class Order():
    """
    Represents an order entity.

    Attributes:
        id (str): The unique identifier for the order.
        customer_id (str): The unique identifier of the customer placing the order.
        product_ids (str): A string containing comma-separated product IDs associated with the order.
        created_date (str): The date and time when the order was created.
        updated_date (str): The date and time when the order was last updated.
    """

    def __init__(self, id: str, customer_id: str, product_ids: List[str], created_date: str, updated_date: str) -> None:
        self.id = id
        self.customer_id = customer_id
        self.product_ids = product_ids
        self.created_date = str(created_date)
        self.updated_date = str(updated_date)


    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Order object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary containing order details.
        """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_ids": self.product_ids,
            "created_date": self.created_date,
            "updated_date": self.updated_date
        }


