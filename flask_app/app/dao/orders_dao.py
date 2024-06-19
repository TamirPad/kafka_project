import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from flask_app.app.utils.sql.MySQLClient import MySQLClient
import logging
from flask_app.app.models.order import Order



class OrderDao:
    """
    Data Access Object for managing orders in the database.

    Attributes:
        mysql_client (MySQLClient): An instance of MySQLClient for database operations.
    """

    def __init__(self, mysql_client: MySQLClient) -> None:
        self.mysql_client = mysql_client


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
        params = (order.id, order.customer_id, json.dumps(order.product_ids), order.created_date, order.updated_date)
        try:
            self.mysql_client.execute(query, params)
            logging.info("[OrderDao.create_order] Order added successfully")
            return Order(order.id, order.customer_id, order.product_ids, order.created_date, order.updated_date)
        except Exception as e:
            logging.error(f"[OrderDao.create_order] Error occurred while adding order: {e}")
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
        logging.info(f"[OrderDao.get_order] Getting order id: {order_id}")
        query = f"SELECT * FROM orders WHERE id = '{order_id}'"
        try:
            result = self.mysql_client.execute(query)
            if result:
                row = result[0]
                return Order(row['id'], row['customerID'], row['product_ids'], row['created_date'], row['updated_date'])
            else:
                logging.info(f"[OrderDao.get_order] Order {order_id} wasn't found")
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
        params = (order.customer_id, json.dumps(order.product_ids), order.updated_date, order.id)
        try:
            logging.info(f"[OrderDao.update_order] Updating order with ID: {order.id}")
            affected_rows = self.mysql_client.execute(query, params)
            if affected_rows > 0:
                logging.info(f"[OrderDao.update_order] Order {order.id} updated successfully, Number of rows affected: {affected_rows}")
                return affected_rows
            else:
                logging.info(f"[OrderDao.update_order] Order {order.id} wasn't updated, Number of rows affected: {affected_rows}")
                return affected_rows
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
            affected_rows = self.mysql_client.execute(query, (order.id,))
            if affected_rows > 0:
                logging.info(f"[OrderDao.delete_order] Order {order.id} deleted successfully, Number of rows affected: {affected_rows}")
                return affected_rows
            else:
                logging.info(f"[OrderDao.delete_order] Order {order.id} wasn't deleted, Number of rows affected: {affected_rows}")
                return affected_rows
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
            result = self.mysql_client.execute(query)
            return [Order(row['id'], row['customerID'], row['product_ids'], row['created_date'], row['updated_date']) for row in result]
        except Exception as e:
            logging.error(f"[orders_dao.get_all_orders] Error occurred while retrieving all orders: {e}")
            raise Exception
