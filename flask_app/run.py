from flask import Flask
from app.api.v1.orders_api import orders_bp
from app.utils.sql.db import db
import logging


def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(orders_bp)

    try:
        # Initialize database connection and schema
        db.connect()
        
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
  
        db.execute_query(schema)
    except Exception as e:
        logging.error("[run.create_app] Error occurred while initializing database schema")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
