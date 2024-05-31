from flask import Flask
from app.api.v1.orders import orders_bp


app = Flask(__name__)
app.register_blueprint(orders_bp)

# Init db connection?



if __name__ == "__main__":
    app.run(debug=True)
