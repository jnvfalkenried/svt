# Use an official Python runtime as a parent image
FROM python:3.12.2-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Workaround for quicker development.
# Installing required packages before copying the rest of the code avoids re-installing them on every code change.
# https://docs.docker.com/build/cache/

# Copy the requirements file into the container at /app
COPY ./rabbitmq_bindings/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rabbitmq_bindings directory contents into the container at /app/rabbitmq_bindings
COPY ./rabbitmq_bindings/ .

# Copy the helpers directory contents into the container at /app/helpers
COPY ./helpers/ /app/helpers/

# Copy the requirements.txt file into the container at /app/requirements.txt
# COPY requirements.txt requirements.txt

# COPY .env .env

# Command to start your application
CMD python bindings.py
