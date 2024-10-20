# producer/Dockerfile

# Use an official Python runtime as a parent image, need python 3.10 otherwise build will fail
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the multimodal_search directory contents into the container
COPY ./multimodal_search /app

# Copy the helper directory contents into the container
COPY ./helpers /app/helpers

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your script
CMD ["python", "-u", "main.py"]
