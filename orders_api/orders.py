import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from MySQL import MySQL
import logging

class Order:
    def __init__(self, id: str, customer_id: str, product_ids: str, created_date: str, updated_date: str) -> None:
        self.id = id
        self.customer_id = customer_id
        self.product_ids = product_ids
        self.created_date = created_date
        self.updated_date = updated_date

class OrderDao:
    def __init__(self, db: MySQL) -> None:
        self.db = db

    def create_order(self, order: Order) -> None:
        query = """
                INSERT INTO orders (id, customerID, product_ids, created_date, updated_date) 
                VALUES (%s, %s, %s, %s, %s)
            """
        params = (order.id, order.customer_id, order.product_ids, order.created_date, order.updated_date)
        try:
            self.db.execute_query(query, params)
            logging.info("Order added successfully")
        except Exception as e:
            logging.error(f"Error occurred while adding order: {e}")

    def get_order(self, order_id: str) -> Optional[Order]:
        query = "SELECT * FROM orders WHERE id = %s"
        try:
            result = self.db.execute_query(query, (order_id,))
            if result:
                row = result[0]
                return Order(row['id'], row['customerID'], row['product_ids'], row['created_date'], row['updated_date'])
            else:
                logging.info("Order not found")
                return None
        except Exception as e:
            logging.error(f"Error occurred while retrieving order: {e}")
            return None

    def update_order(self, order: Order) -> None:
        query = "UPDATE orders SET customerID = %s, product_ids = %s, updated_date = %s WHERE id = %s"
        params = (order.customer_id, order.product_ids, order.updated_date, order.id)
        try:
            self.db.execute_query(query, params)
            logging.info("Order updated successfully")
        except Exception as e:
            logging.error(f"Error occurred while updating order: {e}")

    def delete_order(self, order_id: str) -> None:
        query = "DELETE FROM orders WHERE id = %s"
        try:
            self.db.execute_query(query, (order_id,))
            logging.info("Order deleted successfully")
        except Exception as e:
            logging.error(f"Error occurred while deleting order: {e}")

    def get_all_orders(self) -> List[Order]:
        query = "SELECT * FROM orders"
        try:
            result = self.db.execute_query(query)
            return [Order(row['id'], row['customerID'], row['product_ids'], row['created_date'], row['updated_date']) for row in result]
        except Exception as e:
            logging.error(f"Error occurred while retrieving all orders: {e}")
            return []

