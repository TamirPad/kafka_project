from app.utils.sql.MySQLClient import MySQLClient
from app.config import Config
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
    db = MySQLClient(**db_config)

    try:        
        # Recreate the 'orders' table 
        schema = """
                    CREATE TABLE IF NOT EXISTS orders (
                        id VARCHAR(255) PRIMARY KEY, 
                        customerID VARCHAR(255),
                        product_ids VARCHAR(255),
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    );
                """
  
        db.execute(schema)
    except Exception as e:
        logging.error("[db.init_db] Error occurred while initializing database schema")
    logging.info(" MySQL db Initialized successfully.")

    return db

db = init_db()
