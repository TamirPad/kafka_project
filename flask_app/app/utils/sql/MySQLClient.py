import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool
import logging
from typing import Optional, List, Dict, Any, Union

class MySQLClient:
    def __init__(self, host: str, user: str, password: str, database: str, port: int , pool_name: str = 'mypool', pool_size: int = 10) -> None:
        """
        Initialize the MySQL connection parameters.

        :param host: MySQL server host
        :param user: MySQL username
        :param password: MySQL password
        :param database: MySQL database name
        :param port: MySQL server port (default is 3306)
        :param pool_name: Connection pool name
        :param pool_size: Connection pool size
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.pool: Optional[MySQLConnectionPool] = None
        self._configure_logging()
        self._initialize_pool()


    def _configure_logging(self) -> None:
        """Configure logging for the MySQL class."""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    def _initialize_pool(self) -> None:
        """Initialize the MySQL connection pool."""
        try:
            self.pool = MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                pool_reset_session=True,
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                use_pure=True,
                ssl_disabled= True
            )
            logging.info("MySQL connection pool initialized successfully")
        except Error as e:
            logging.error(f"[MySQLClient._initialize_pool] Error occurred: {e}")
            self.pool = None


    def get_connection(self):
        """Get a connection from the pool."""
        if self.pool is None:
            logging.error("[MySQLClient.get_connection] Error occurred: Connection pool is not initialized.")
            raise Exception
        return self.pool.get_connection()


    def execute(self, query: str, params: Optional[Union[Dict[str, Any], List[Any]]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a SQL query.

        :param query: SQL query to be executed
        :param params: Optional parameters for parameterized query
        :return: Query result for SELECT queries, None otherwise
        """
        connection = self.get_connection()
        if connection is None:
            logging.error("[MySQLClient.execute] Error occurred: Could not get connection from pool.")
            raise Exception

        logging.debug(f"[MySQLClient.execute] Executing Query: \n{query}")

        try:
            cursor = connection.cursor(buffered=True, dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            if cursor.with_rows:
                result: List[Dict[str, Any]] = cursor.fetchall()
                logging.info("[MySQLClient.execute]Query executed successfully")
                return result
            else:
                affected_rows = cursor.rowcount
                logging.info(f"[MySQLClient.execute]Query executed successfully, Number of rows affected: {affected_rows}")
                return affected_rows
        except Error as e:
            logging.error(f"[MySQLClient.execute_query] Error occurred: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
