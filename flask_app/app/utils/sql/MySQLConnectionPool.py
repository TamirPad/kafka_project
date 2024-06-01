import mysql.connector.pooling as pooling
from mysql.connector import Error
import logging
from typing import Optional

class MySQLConnectionPool:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306, pool_name: str = 'mypool', pool_size: int = 5) -> None:
        # Todo
        pass

    def _create_connection_pool(self) -> None:
        # Todo
        pass

    def get_connection(self) -> Optional[pooling.PooledMySQLConnection]:
        # Todo
        pass
