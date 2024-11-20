# Use Playwright base image
FROM mcr.microsoft.com/playwright/python:v1.37.0-jammy

# Set the working directory
WORKDIR /app

# Install Playwright browsers
RUN pip install --no-cache-dir playwright==1.37.0 && playwright install chromium

# Copy the requirements file into the container
COPY ./producer/requirements.txt /app/requirements.txt

# Install Python dependencies including Playwright
RUN pip install --no-cache-dir -r requirements.txt

# Copy the producer directory contents into the container
COPY ./producer /app

# Copy the helper directory contents into the container
COPY ./helpers /app/helpers

# Command to run your script
CMD ["python", "-u", "main.py"]
