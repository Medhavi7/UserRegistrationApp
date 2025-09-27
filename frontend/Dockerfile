# Use Node.js
FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .
RUN npm install react-router-dom

# Build React + Tailwind
RUN npm run build

# Serve app using a simple web server
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]



