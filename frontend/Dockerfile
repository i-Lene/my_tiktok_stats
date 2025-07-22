# Build step
FROM node:18 as build

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build

# Production server
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
