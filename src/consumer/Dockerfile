# consumer/Dockerfile

# Use an official Python runtime as a parent image, need python 3.10 otherwise build will fail
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Workaround for quicker development.
# Installing required packages before copying the rest of the code avoids re-installing them on every code change.
# https://docs.docker.com/build/cache/

# Copy the requirements file into the container at /app
COPY ./consumer/requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the producer directory contents into the container
COPY ./consumer /app

# Copy the helper directory contents into the container
COPY ./helpers /app/helpers

# Copying the db folder
COPY ./postgresql /app/postgresql

# Command to run your script
CMD ["python", "-u", "main.py"]
