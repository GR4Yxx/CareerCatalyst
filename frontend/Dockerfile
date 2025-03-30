FROM node:20-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Expose port
EXPOSE 3000

# Command to run the app
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"] 