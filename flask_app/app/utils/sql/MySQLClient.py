import uuid
import mysql.connector
from mysql.connector import Error
import logging
from typing import Optional, List, Dict, Any, Union


class MySQLClient:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306) -> None:
        """
        Initialize the MySQL connection parameters.

        :param host: MySQL server host
        :param user: MySQL username
        :param password: MySQL password
        :param database: MySQL database name
        :param port: MySQL server port (default is 3306)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection: Optional[mysql.connector.MySQLConnection] = None
        self._configure_logging()

    def _configure_logging(self) -> None:
        """Configure logging for the MySQL class."""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def connect(self) -> None:
        """Connect to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                logging.info("Connection to MySQL database successful")
        except Error as e:
            logging.error(f"Error occurred: {e}")
            self.connection = None

    def disconnect(self) -> None:
        """Disconnect from the MySQL database."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Disconnected from MySQL database")

    def execute_query(self, query: str, params: Optional[Union[Dict[str, Any], List[Any]]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a SQL query.

        :param query: SQL query to be executed
        :param params: Optional parameters for parameterized query
        :return: Query result for SELECT queries, None otherwise
        """
        if self.connection is None or not self.connection.is_connected():
            logging.error("Connection is not established")
            return None
        logging.info(f"Executing Query: \n{query}")

        try:
            cursor = self.connection.cursor(buffered=True, dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            if cursor.with_rows:
                result: List[Dict[str, Any]] = cursor.fetchall()
                logging.info("Query executed successfully")
                return result
            else:
                logging.info("Query executed successfully, no rows returned")
                return None
        except Error as e:
            logging.error(f"Error occurred[MySQL.execute_query]: {e}")
            return None
        finally:
            cursor.close()
