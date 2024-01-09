FROM python:3.13-rc-alpine3.17

# Installe tzdata pour la configuration du fuseau horaire
RUN apk add --no-cache libpq-dev gcc

# Définit le fuseau horaire (remplacez par votre fuseau horaire souhaité)
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Définit le répertoire de travail dans le conteneur
WORKDIR /API/

# Copie les fichiers de dépendances Python dans le conteneur
COPY ./API/ /API/
COPY ./requirements.txt /API/

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Execute pour debug
CMD [ "tail", "-f", "/dev/null" ]

# Utiliser supervisord pour démarrer les services
# CMD []