from app.utils.sql.MySQLClient import MySQLClient
from app.config import Config

def init_db():
    """
    Initialize a connection to the MySQL database.

    Returns:
        MySQLClient: An instance of MySQLClient representing the database connection.
    """
    db_config = {
        'host': Config.MYSQL_HOST,
        'user': Config.MYSQL_USER,
        'password': Config.MYSQL_PASSWORD,
        'database': Config.MYSQL_DB,
        'port': Config.MYSQL_PORT,
        'pool_name': 'mypool',
        'pool_size': 10  
    }
    db = MySQLClient(**db_config)
    return db

db = init_db()
