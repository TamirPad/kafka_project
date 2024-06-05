import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from app.utils.sql.MySQLClient import MySQLClient
import logging

class Order:
    """
    Represents an order entity.

    Attributes:
        id (str): The unique identifier for the order.
        customer_id (str): The unique identifier of the customer placing the order.
        product_ids (str): A string containing comma-separated product IDs associated with the order.
        created_date (str): The date and time when the order was created.
        updated_date (str): The date and time when the order was last updated.
    """

    def __init__(self, id: str, customer_id: str, product_ids: str, created_date: str, updated_date: str) -> None:
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


class OrderDao:
    """
    Data Access Object for managing orders in the database.

    Attributes:
        db (MySQLClient): An instance of MySQLClient for database operations.
    """

    def __init__(self, db: MySQLClient) -> None:
        self.db = db


    def create_order(self, order: Order) -> None:
        """
        Create a new order.

        Args:
            order (Order): The order object to be created.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        query = """
                INSERT INTO orders (id, customerID, product_ids, created_date, updated_date) 
                VALUES (%s, %s, %s, %s, %s)
            """
        params = (order.id, order.customer_id, order.product_ids, order.created_date, order.updated_date)
        try:
            self.db.execute_query(query, params)
            logging.info("Order added successfully")
            return Order(order.id, order.customer_id, order.product_ids, order.created_date, order.updated_date)
        except Exception as e:
            logging.error(f"[orders_dao.create] Error occurred while adding order: {e}")
            raise Exception


    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Retrieve an order by its ID.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            Optional[Order]: The retrieved Order object, or None if the order doesn't exist.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        logging.info(f"Getting order id: {order_id}")
        query = f"SELECT * FROM orders WHERE id = '{order_id}'"
        try:
            result = self.db.execute_query(query)
            if result:
                row = result[0]
                return Order(row['id'], row['customerID'], row['product_ids'], row['created_date'], row['updated_date'])
            else:
                logging.info(f"Order {order_id} wasn't found")
                return None
        except Exception as e:
            logging.error(f"[orders_dao.get_order] Error occurred while retrieving order: {e}")
            raise Exception


    def update_order(self, order: Order) -> Optional[Order]:
        """
        Update an existing order.

        Args:
            order (Order): The updated order object.

        Returns:
            Optional[Order]: The updated Order object.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        query = "UPDATE orders SET customerID = %s, product_ids = %s, updated_date = %s WHERE id = %s"
        params = (order.customer_id, order.product_ids, order.updated_date, order.id)
        try:
            self.db.execute_query(query, params)
            logging.info(f"Order {order.id} updated successfully")
            return self.get_order(order_id=order.id)
        except Exception as e:
            logging.error(f"[orders_dao.update_order] Error occurred while updating order: {e}")
            raise Exception


    def delete_order(self, order: Order) -> Optional[Order]:
        """
        Delete an order by its ID.

        Args:
            order_id (str): The ID of the order to delete.

        Returns:
            str: The ID of the deleted order.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        query = "DELETE FROM orders WHERE id = %s"
        try:
            self.db.execute_query(query, (order.id,))
            logging.info(f"Order {order.id} deleted successfully")
            return order
        except Exception as e:
            logging.error(f"Error occurred while deleting order: {e}")
            raise Exception


    def get_all_orders(self) -> List[Order]:
        """
        Retrieve all orders from the database.

        Returns:
            List[Order]: A list of all orders.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        query = "SELECT * FROM orders"
        try:
            result = self.db.execute_query(query)
            return [Order(row['id'], row['customerID'], row['product_ids'], row['created_date'], row['updated_date']) for row in result]
        except Exception as e:
            logging.error(f"[orders_dao.get_all_orders] Error occurred while retrieving all orders: {e}")
            raise Exception
