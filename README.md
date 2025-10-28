# Migrez des données médicales à l'aide du NoSQL

## Contexte

DataSoluTech, spécialiste des solutions de gestion et d’analyse de données, a reçu un dataset médical de patients d’un client. Ce dernier rencontre des problèmes de scalabilité pour gérer et exploiter ses données quotidiennes.

La mission consiste à proposer une solution Big Data scalable horizontalement permettant :

- une meilleure gestion des données,

- une exploitation rapide et fiable pour l’analyse,

- une portabilité et facilité de déploiement.

## Etape 1 : Télécharger le code

Cliquer sur le bouton vert "<> Code" puis sur Download ZIP.  
Extraire l'ensemble des éléments dans le dossier dans lequel vous voulez stockez les datas qui seront téléchargées.  

## Etape 2 ; Installer Python et ouvrir le terminal de commande

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

Ouvrir le terminal de commande :  
Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

## Etape 3 : Création de l'environnement virtuel

Se placer dans le dossier où l'on a extrait l'ensemble des documents grâce à la commande ``cd``  
Exemple :
```
cd home/magali/OpenClassrooms/Formation/Projet_7
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

## Branches du projet

healthcare/app :

- Contient la version complète du programme avec main.py.

- Permet de lancer le script localement pour nettoyer et insérer les données.

healthcare/docker :

- Contient le Dockerfile et les configurations pour créer une image Docker complète.

- L’image inclut MongoDB et le script de migration, ce qui permet :

    - de déployer facilement la solution sur n’importe quelle machine,

    - de rendre le système scalable et portable,


