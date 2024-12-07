FROM python:3.10-slim

# Install make and other necessary tools
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY ./docs/requirements.txt /app/docs/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/docs/requirements.txt

# Set working directory
WORKDIR /app

# Copy Sphinx project and source code
COPY ./docs /app/docs
COPY ./src /app/src

# Generate HTML on container start
CMD ["sh", "-c", "cd docs && make html && python3 -m http.server --directory build/html 8081"]
