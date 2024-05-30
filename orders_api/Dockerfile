# Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow external access
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]