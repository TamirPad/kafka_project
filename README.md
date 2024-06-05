# Project Name

## Description

This project comprises three main components:

- **Infrastructure Setup**: Docker Compose files for deploying Kafka, Zookeeper, MySQL, Elasticsearch, and Kibana services.
  
- **Flask Application**: An API for managing orders, interacting with MySQL, and producing Kafka messages.
  
- **Kafka Consumer Application**: Consumes messages from Kafka topics and indexes them into Elasticsearch.


## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. Start the infrastructure services using Docker Compose:

    ```bash
    docker-compose up -d
    ```

3. Configure the Flask application:
   - Navigate to the `flask_app` directory.
   - Update the `.env` file with your MySQL and Kafka settings.

4. Start the Flask application:

    ```bash
    python run.py
    ```

5. Configure the Kafka consumer application:
   - Navigate to the `consumer_app` directory.
   - Update the `main.py` file with your Kafka and Elasticsearch settings.

6. Start the Elasticsearch consumer application:

    ```bash
    python main.py
    ```

## Usage

- **Flask Application**:
  - Access the API endpoints to manage orders (e.g., create, retrieve, update, delete).
  - Example: GET http://localhost:5000/api/v1/order/<order_id>

- **Kafka Consumer Application**:
  - Consumes messages from the "orders" topic.
  - Indexes order messages into Elasticsearch for further analysis.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
