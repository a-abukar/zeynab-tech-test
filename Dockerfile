# Use the official Node.js 18 image as a base
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install the application dependencies
RUN npm install --production

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 3000

# Start the Node.js application
CMD ["npm", "start"]
