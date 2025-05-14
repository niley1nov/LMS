# frontend/Dockerfile

# 1) Build the React app
FROM node:18-alpine AS build
WORKDIR /app

# install deps
COPY package*.json ./
RUN npm install

# copy source and build
COPY . .
RUN npm run build

# 2) Serve the static build with nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 (Cloud Run default HTTP port)
EXPOSE 80

# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
