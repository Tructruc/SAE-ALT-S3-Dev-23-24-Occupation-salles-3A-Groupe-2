FROM node:18.16-alpine AS build

WORKDIR /build

# Récupération des sources et installation des dépendances
COPY ./front-vue /build
RUN rm -rf node_modules
RUN npm install

# Build de l'application
RUN  npm run build

# Création de l'image de release
FROM nginx:1.15.2-alpine as release

# Copie des fichiers de configuration et de l'application depuis le build
WORKDIR /usr/share/nginx/html
COPY --from=build /build/dist/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]