# Projet 5 – Migration des données médicales vers MongoDB
## Description du projet

Ce projet a pour objectif de migrer un dataset médical de patients vers MongoDB, tout en proposant un système scalable, portable et sécurisé.
Le projet est divisé en deux parties principales :

healthcare/app : contient le code Python pour nettoyer les données CSV et les insérer dans MongoDB.

healthcare/docker : contient les fichiers Docker pour lancer MongoDB et l’application dans des conteneurs, facilitant le déploiement et la portabilité.

Le programme principal est main.py, qui automatise la pipeline complète :

- Nettoyage du CSV (suppression des doublons et valeurs manquantes)

- Transformation des données pour MongoDB

- Insertion des documents dans MongoDB

## Etapes pour lancer le projet

### Etape 1 : Télécharger le code

Cliquer sur le bouton vert <> Code puis sur Download ZIP.

Extraire l'ensemble des fichiers dans le dossier où vous souhaitez stocker le projet et les datas.

## Etape 2 : Installer Python et ouvrir le terminal

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

Ouvrir le terminal de commande :

Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

## Etape 3 : Créer un environnement virtuel

### Créer l’environnement virtuel :
```
python3 -m venv env
```

#### Activer l’environnement :

- Linux / Mac OS :
```
source env/bin/activate
```  

- Windows :

```
env\Scripts\activate.bat
```

### Etape 4 : Installer les dépendances
```
pip install -r requirements.txt
```

### Etape 5 : Connexion à MongoDB

Créer le fichier ```.env```

Créer un fichier .env à la racine de docker ou du projet contenant les identifiants pour MongoDB :
```
# MongoDB root
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=Admin123!
MONGO_DB=healthcare_data

# User pour l'évaluateur
MONGO_URI=mongodb://evaluateur:Evaluateur123!@mongo_db:27017/healthcare_data?authSource=healthcare_data

```

#### Connexion à MongoDB avec l’utilisateur evaluateur

Commandes directes pour se connecter à MongoDB (mongosh) :

- Linux / Mac OS :
```
mongosh "mongodb://evaluateur:evaluateur123!@localhost:27017/healthcare_data"
```

- Windows (PowerShell / CMD) :

```
mongosh "mongodb://evaluateur:evaluateur123!@localhost:27017/healthcare_data"
```


### Etape 5 : Lancer le programme Python

Dans le terminal, lancer la commande :

```
python3 main.py
```

Le programme va nettoyer le CSV et générer un fichier grouped_duplicates.csv à la racine du projet  

Les données sont ensuite insérées dans MongoDB.  

#### Connexion à MongoDB

Vous pouvez vous connecter via mongosh avec les identifiants que vous avez insérés dans ```.env```.  

#### Commandes pour se connecter :

- Linux / Mac OS :
```
mongosh "mongodb://<USER>:<PASSWORD>@localhost:27017/healthcare_data"
```

- Windows :
```
mongosh "mongodb://<USER>:<PASSWORD>@localhost:27017/healthcare_data"
```

Vous pouvez les voir en utilisant les commandes suivantes :  

- Vérification des données :
```
use healthcare_data
db.patients.find().limit(5).pretty()
```

- Vérification des utilisateurs :
```
db.getUsers()
```



## Utilisation de Docker


Construire et lancer les conteneurs :

```
docker-compose up --build
```

Le conteneur MongoDB sera accessible sur le port 27017.   

Le conteneur app exécutera automatiquement ```main.py```.  

Les fichiers générés (grouped_duplicates.csv et healthcare_dataset_clean.csv) apparaissent dans app/  


Vérification :
```
use healthcare_data
db.patients.find().limit(5).pretty()
``` 
### Résumé du fonctionnement

**Collecte** : Le CSV est lu depuis main.

**Nettoyage** : Les doublons sont enregistrés dans grouped_duplicates.csv et supprimés du DataFrame.

**Transformation** : Préparation des documents pour MongoDB.

**Stockage** : Insertion sécurisée dans MongoDB avec authentification et rôles utilisateurs.

**Docker** : Conteneurisation pour portabilité et déploiement.

## Système d’authentification et rôles utilisateurs

Le projet met en place un système d’authentification sécurisé pour accéder à MongoDB et gérer les données des patients.  

### Authentification

Chaque utilisateur MongoDB possède un nom d’utilisateur et un mot de passe.

Les mots de passe sont hachés avec l’algorithme SHA-256 pour assurer la sécurité.

L’accès à la base de données nécessite de s’authentifier avant toute opération (lecture ou écriture).

### Rôles utilisateurs

Les utilisateurs ont des rôles définis pour limiter leurs permissions. Voici les rôles possibles utilisés dans le projet :  

| Rôle      | Description                                                     | Portée           |
|-----------|-----------------------------------------------------------------|-----------------|
| read      | Lecture seule des collections                                    | Base spécifique |
| readWrite | Lecture et écriture des documents                                | Base spécifique |
| dbAdmin   | Administration de la base (index, statistiques, utilisateurs, etc.) | Base spécifique |
| userAdmin | Gestion des utilisateurs et des rôles                            | Base spécifique |
| dbOwner   | Combine readWrite, dbAdmin et userAdmin sur la même base         | Base spécifique |
| root      | Accès total à toutes les bases et commandes                     | Global          |


**Pour permettre à l’évaluateur de vérifier les données et les utilisateurs, l’utilisateur evaluateur est configuré avec le rôle dbAdmin sur la base healthcare_data.**


### Branches Git et utilité
Branche	Contenu	Utilité
- healthcare/app	Code Python (main.py, clean_csv.py, transfer_mongodb.py), dataset	Développement et exécution du pipeline de données
- healthcare/docker	Dockerfile, docker-compose.yml, .env.sample	Conteneurisation de MongoDB et de l’application pour portabilité et déploiement
