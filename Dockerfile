# Utiliser une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements si tu en as
COPY requirements.txt .
COPY app/ /app
# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Variable d'environnement par défaut 
ENV MONGO_HOST=mongo_db
ENV MONGO_PORT=27017
ENV MONGO_DB=healthcare_data
ENV MONGO_USER=evaluateur
ENV MONGO_PASSWORD='Evaluateur123!'

# Commande par défaut
CMD ["python", "main.py"]
