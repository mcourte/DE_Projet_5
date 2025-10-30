<<<<<<< HEAD
# Branche healthcare/app 

Cette branche contient le script principal ```main.py``` pour nettoyer le dataset médical, détecter et enregistrer les doublons, puis insérer les données dans MongoDB.

##  Fonctionnement et utilité du programme

Le dossier /app contient le cœur applicatif du projet.  
Il regroupe les scripts Python responsables du nettoyage, de la préparation et du transfert des données vers la base MongoDB.  

### Fonctionnement général

Nettoyage des fichiers CSV
Le script clean_csv.py supprime les doublons, ordonne les données et produit un fichier propre nommé grouped_duplicated.csv.  
Ce fichier est généré à la racine du projet après exécution.  

### Transfert vers MongoDB
Le script transfer_mongodb.py se connecte à la base MongoDB (locale ou conteneurisée) pour importer les données nettoyées.
La connexion est sécurisée grâce aux variables d’environnement (stockées dans .env, non versionné).  

### Tests unitaires
Le fichier test_unitaires.py permet de vérifier le bon fonctionnement des fonctions principales du projet (nettoyage et transfert).  

### Utilité

Automatiser la préparation des données avant leur intégration dans MongoDB.  

Garantir la qualité et la cohérence des données.  

Permettre un chargement reproductible et traçable des jeux de données dans un environnement maîtrisé.  


## Etape 1 : Télécharger le code

Cliquer sur le bouton vert "<> Code" puis sur Download ZIP.  
Extraire l'ensemble des éléments dans le dossier dans lequel vous voulez stockez les datas qui seront téléchargées.  

## Etape 2 : Installer Python et ouvrir le terminal de commande

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

Ouvrir le terminal de commande :  
Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

## Etape 3 : Création de l'environnement virtuel

Se placer dans le dossier où l'on a extrait l'ensemble des documents grâce à la commande ``cd``  
Exemple :
```
cd home/magali/OpenClassrooms/Formation_DE/Projet_5/app
```


Dans le terminal de commande, executer la commande suivante :
```
python3 -m venv env
```


Activez l'environnement virtuel
```
source env/bin/activate
```
> Pour les utilisateurs de Windows, la commande est la suivante : 
> ``` env\Scripts\activate.bat ```

## Etape 4 : Télécharger les packages nécessaires au bon fonctionnement du programme

Dans le terminal, taper la commande suivante :
```
pip install -r requierements.txt
```

## Étape 5 : Connexion à MongoDB avec mongosh

Avant de lancer le script, assurez-vous que MongoDB est démarré.

- Identifiants pour l’évaluateur

    - Utilisateur : evaluateur

    - Mot de passe : Evaluateur123!

    - Base de données : healthcare_data
 
1️ Linux

Démarrer MongoDB :  
```
sudo systemctl start mongod
```

Vérifier que le service est actif :  
```
sudo systemctl status mongod
```

Se connecter à mongosh avec les identifiants :  

```
mongosh -u evaluateur -p Evaluateur123! --authenticationDatabase healthcare_data
```

2️ MacOS (Homebrew)

Démarrer MongoDB :  

```
brew services start mongodb-community
```


Lancer le shell mongosh :  

```
mongosh -u evaluateur -p Evaluateur123! --authenticationDatabase healthcare_data
```

3️ Windows

Démarrer MongoDB :  

- Si installé en tant que service, il démarre automatiquement.  

- Sinon, ouvrir PowerShell et lancer :  

```
"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe"
```

Dans un autre terminal (PowerShell ou cmd), lancer mongosh :

```
"C:\Program Files\MongoDB\Server\7.0\bin\mongosh.exe" -u evaluateur -p Evaluateur123! --authenticationDatabase healthcare_data
```


*Le paramètre --authenticationDatabase indique la base où l’utilisateur a été créé.*

## Vérifier les utilisateurs et rôles

Votre rôle d'evaluateur dispose du rôle userAdmin sur la base healthcare_data et vous pouvez la liste des  utilisateurs :  
```
use healthcare_data
db.getUsers()
```

## Étape 6 : Lancer le script principal
```
python3 main.py
```

Le script va :

- Nettoyer le CSV healthcare_dataset.csv.

- Détecter et enregistrer les doublons dans grouped_duplicates.csv.

- Insérer les données nettoyées dans la collection MongoDB.

## Étape 4 : Vérifier les données dans MongoDB

Après exécution :

```
use healthcare_data
db.patients.find().limit(5).pretty()
```

Vous verrez les premières lignes insérées.

### Remarques importantes

Le fichier grouped_duplicates.csv contient tous les doublons détectés, avec l’original suivi de ses copies.

MongoDB doit être démarré avant d’exécuter le script.

Utilisez les identifiants fournis pour accéder à la base et vérifier les données.

## Information supplémentaires

### Système d’authentification et rôles utilisateurs
- Mécanisme d’authentification  

MongoDB utilise un système d’authentification par utilisateur avec un hachage sécurisé SHA-256 pour protéger les mots de passe.  
Lorsqu’un utilisateur est créé, MongoDB ne stocke pas le mot de passe en clair.  
Il applique la formule suivante :  
```
hash = SHA256(password + salt)
```

L’empreinte ainsi générée est enregistrée dans la collection interne system.users.  
Même avec un accès aux fichiers système, il est impossible de récupérer le mot de passe original.  

-  Liste complète des rôles MongoDB

| **Rôle** | **Description** | **Portée** |
|-----------|------------------|-------------|
| `read` | Lecture seule des collections | Base spécifique |
| `readWrite` | Lecture et écriture des documents | Base spécifique |
| `dbAdmin` | Administration de la base (index, statistiques, utilisateurs, etc.) | Base spécifique |
| `userAdmin` | Gestion des utilisateurs et des rôles | Base spécifique |
| `dbOwner` | Combine `readWrite`, `dbAdmin`, et `userAdmin` sur la même base | Base spécifique |
| `root` | Accès total à toutes les bases et commandes | Global |
=======
# Migrez des données médicales à l'aide du NoSQL

## Contexte

DataSoluTech, spécialiste des solutions de gestion et d’analyse de données, a reçu un dataset médical de patients d’un client. Ce dernier rencontre des problèmes de scalabilité pour gérer et exploiter ses données quotidiennes.

La mission consiste à proposer une solution Big Data scalable horizontalement permettant :

- une meilleure gestion des données,

- une exploitation rapide et fiable pour l’analyse,

- une portabilité et facilité de déploiement.



## Branches du projet

healthcare/app :

- Contient la version complète du programme avec main.py.

- Permet de lancer le script localement pour nettoyer et insérer les données.

healthcare/docker :

- Contient le Dockerfile et les configurations pour créer une image Docker complète.

- L’image inclut MongoDB et le script de migration, ce qui permet :

    - de déployer facilement la solution sur n’importe quelle machine,

    - de rendre le système scalable et portable,


>>>>>>> origin/main
