#!/bin/sh

# Function to fetch the public URL from the Ngrok API
fetch_url() {
  curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url'
}

# Wait for Ngrok to start and the API to be available
echo "Waiting for Ngrok to initialize..."
for i in $(seq 1 10); do
  NGROK_URL=$(fetch_url)
  if [ -n "$NGROK_URL" ]; then
    break
  fi
  echo "Retrying... ($i/10)"
  sleep 2
done

# Check if URL is fetched
if [ -z "$NGROK_URL" ]; then
  echo "Ngrok URL could not be fetched. Is Ngrok running?"
else
  echo "Ngrok public URL: $NGROK_URL"
fi
