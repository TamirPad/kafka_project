from app.utils.sql.MySQLClient import MySQLClient
from app.config import Config

def init_db():
    db_config = {
        'host': Config.MYSQL_HOST,
        'user': Config.MYSQL_USER,
        'password': Config.MYSQL_PASSWORD,
        'database': Config.MYSQL_DB,
        'port': Config.MYSQL_PORT
    }
    db = MySQLClient(**db_config)

    return db

db = init_db()