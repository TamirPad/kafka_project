from flask_app.app.utils.sql.MySQLClient import MySQLClient
from flask_app.app.config import Config
import logging

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
    logging.info(f"****attempting to connect to mysql with :{db_config}")
    mysql_client = MySQLClient(**db_config)

    try:        
        # Recreate the 'orders' table 
        schema = """
                    CREATE TABLE IF NOT EXISTS orders (
                        id VARCHAR(255) PRIMARY KEY, 
                        customerID VARCHAR(255),
                        product_ids JSON,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    );
                """
  
        mysql_client.execute(schema)
    except Exception as e:
        logging.error("[db.init_db] Error occurred while initializing database schema")
    logging.info(" MySQL db Initialized successfully.")

    return mysql_client

mysql_client = init_db()
