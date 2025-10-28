# Branche healthcare/app 

Cette branche contient le script principal ```main.py``` pour nettoyer le dataset médical, détecter et enregistrer les doublons, puis insérer les données dans MongoDB.

## Étape 1 : Se placer dans le dossier app
```
cd healthcare/app
```
## Étape 2 : Connexion à MongoDB avec mongosh

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

## Étape 3 : Lancer le script principal
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
