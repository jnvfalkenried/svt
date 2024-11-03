# fronted/Dockerfile
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the producer directory contents into the container
# COPY ./frontend /app

# Copy database_models
# COPY ./postgresql/database_models /app/postgresql/database_models

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY ./frontend/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your script
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]