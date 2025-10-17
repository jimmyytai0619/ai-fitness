# Use Node 20
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY package*.json ./
RUN npm install

# Copy all files
COPY . .

# Build the Next.js app
RUN npm run build

# Expose port 8080 (Railway uses this)
EXPOSE 8080

# Start the app
CMD ["npm", "start"]
