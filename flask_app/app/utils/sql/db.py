from app.utils.sql.MySQL import MySQL
from app.config import Config

def init_db():
    db_config = {
        'host': Config.MYSQL_HOST,
        'user': Config.MYSQL_USER,
        'password': Config.MYSQL_PASSWORD,
        'database': Config.MYSQL_DB,
        'port': Config.MYSQL_PORT
    }
    db = MySQL(**db_config)
    return db

db = init_db()

