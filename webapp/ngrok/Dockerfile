# Use the latest Alpine Linux image
FROM alpine:latest

# Install required packages
RUN apk add --no-cache curl jq bash openrc

# Install Ngrok
RUN curl -sSL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-amd64.tgz | tar xz \
    && mv ngrok /usr/local/bin/ngrok

# Add the Ngrok auth token during build if provided
ARG NGROK_AUTHTOKEN
RUN if [ -n "$NGROK_AUTHTOKEN" ]; then \
    ngrok config add-authtoken "$NGROK_AUTHTOKEN"; \
    fi

# Add the fetch script
COPY fetch_ngrok_url.sh /fetch_ngrok_url.sh
RUN chmod +x /fetch_ngrok_url.sh

# Entry point to start Ngrok and fetch the URL
ENTRYPOINT ["/bin/bash", "-c", "ngrok http nginx:80 & sleep 5 && /fetch_ngrok_url.sh && tail -f /dev/null"]
