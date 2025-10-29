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


