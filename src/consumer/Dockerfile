# consumer/Dockerfile

# Use an official Python runtime as a parent image, need python 3.10 otherwise build will fail
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the producer directory contents into the container
COPY ./consumer /app

# Copy the helper directory contents into the container
COPY ./helpers /app/helpers

# Copying the db folder
COPY ./postgresql /app/postgresql

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your script
CMD ["python", "main.py"]
