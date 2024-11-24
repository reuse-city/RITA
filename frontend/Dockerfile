FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Command is specified in docker-compose.yml
CMD ["npm", "run", "dev"]
