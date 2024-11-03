# fronted/Dockerfile
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the producer directory contents into the container
COPY ./frontend /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your script
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]