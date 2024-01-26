# Étape 1: Construire l'application Vue
FROM node:18.16-alpine AS build

WORKDIR /build
COPY ./front-vue /build
RUN rm -rf node_modules
RUN npm install
RUN npm run build

# Étape 2: Préparation de l'image Nginx
FROM nginx:1.15.2-alpine as release

# Installation d'OpenSSL pour générer un certificat auto-signé
RUN apk add --no-cache openssl

# Création d'un répertoire pour le certificat et la clé
RUN mkdir -p /etc/nginx/certificates

# Génération d'un certificat auto-signé et d'une clé privée
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -subj "/C=FR/ST=Some-State/L=Blagnac/O=SAE-IUT-BLAGNAC/OU=IT Department/CN=localhost" \
    -keyout /etc/nginx/certificates/localhost.key \
    -out /etc/nginx/certificates/localhost.crt

# Copie des fichiers de l'application et de la configuration Nginx
WORKDIR /usr/share/nginx/html
COPY --from=build /build/dist/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf

# Démarrage de Nginx
CMD ["nginx", "-g", "daemon off;"]
