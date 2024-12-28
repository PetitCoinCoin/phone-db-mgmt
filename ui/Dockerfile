FROM node:23 AS build-stage

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
COPY ./src ./src
COPY ./public ./public
RUN npm ci
RUN npm run build

FROM caddy:alpine

EXPOSE 80
EXPOSE 443

COPY --from=build-stage /app/build /usr/share/caddy
