# Stage 1: Build the React app
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Install dependencies
COPY ./react_frontend/package*.json ./
RUN npm install

# Copy the rest of the app source code
# COPY ./react_frontend .

CMD ["npm", "start"]