# Use an official Python runtime as a parent image
FROM python:3.12.2-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the rabbitmq_bindings directory contents into the container at /app/rabbitmq_bindings
COPY ./rabbitmq_bindings/ .

# Copy the helpers directory contents into the container at /app/helpers
COPY ./helpers/ /app/helpers/

# Copy the requirements.txt file into the container at /app/requirements.txt
# COPY requirements.txt requirements.txt

# COPY .env .env

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to start your application
CMD python example.py
