from flask import Flask
from app.api.v1.orders import orders_bp
from app.utils.sql.db import db

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(orders_bp)
    
    # Initialize database connection
    db.connect()
    
    # Add teardown handler to close the database connection
    @app.teardown_appcontext
    def close_db(exception):
        db.disconnect()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
