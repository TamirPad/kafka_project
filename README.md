# KAFKA Project

## Description

This project is a Flask application for managing orders, with integration for Apache Kafka and MySQL.

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone this repository:
    git clone <repository_url>

2. Navigate to the project directory:
    cd <project_directory>

3. Create a .env file with the following environment variables:

        * MySQL
        
                MYSQL_HOST=mysqldb.dev

                MYSQL_USER=test_user

                MYSQL_PASSWORD=test_password

                MYSQL_DB=test_db

        * Kafka

                KAFKA_BOOTSTRAP_SERVERS=localhost:9092

                KAFKA_TOPIC=my_topic

### Running the Application

1. Start the Docker containers:

        docker-compose up -d
        Access the application at http://localhost:5000.

2. Stopping the Application

        To stop the Docker containers, run:
        docker-compose down
        

*In the future, the Flask application will be containerized and included in the Docker Compose setup for easier deployment. The updated setup will be as follows: