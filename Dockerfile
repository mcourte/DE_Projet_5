# Utiliser une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements et le code source
COPY ../requirements.txt .
COPY ../app/ /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Variables d'environnement par défaut (peuvent être surchargées par docker-compose)
ENV MONGO_HOST=mongo_db
ENV MONGO_PORT=27017
ENV MONGO_DB=healthcare_data
ENV MONGO_USER=evaluateur
ENV MONGO_PASSWORD=Evaluateur123!

# Commande par défaut
CMD ["python", "main.py"]
