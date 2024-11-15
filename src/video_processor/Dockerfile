# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set noninteractive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies in a single RUN command to reduce layers
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./video_processor/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./video_processor /app
COPY ./helpers /app/helpers

# Command to run your script
CMD ["python", "-u", "main.py"]