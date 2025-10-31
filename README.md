# main.py – Script principal de migration des données
## Objectif

Le fichier ```main.py``` orchestre l’ensemble du processus de migration des données médicales depuis un fichier CSV vers une base MongoDB.  
Il constitue le cœur de la pipeline et exécute automatiquement toutes les étapes :  
lecture, nettoyage, transformation et insertion des données.  

### Étapes principales du script

- Chargement du dataset

Le script lit le fichier healthcare_dataset.csv présent dans le dossier app/.

Les données sont chargées dans un DataFrame Pandas pour faciliter le traitement.

- Nettoyage des données

Suppression des doublons.

Détection des doublons enregistrée dans grouped_duplicates.csv.

Suppression des lignes contenant des valeurs manquantes critiques.

Normalisation des types de données (dates, entiers, chaînes...).

- Transformation

Conversion des données nettoyées au format compatible avec MongoDB (documents JSON).

Harmonisation des clés (noms de colonnes, formats).

- Connexion sécurisée à MongoDB

Connexion via l’URI stocké dans le fichier .env :
```
MONGO_URI=mongodb://evaluateur:Evaluateur123!@mongo_db:27017/healthcare_data?authSource=healthcare_data
```

- Authentification avec l’utilisateur défini (evaluateur).

Insertion dans MongoDB

Les documents sont insérés dans la collection patients.

Si la collection existe déjà, seules les nouvelles données sont ajoutées.

- Journalisation

Chaque étape affiche des messages dans la console (succès, erreurs, nombre de lignes insérées, etc.).

Cela permet de suivre l’évolution de la migration.

- Génération de fichiers de sortie

  - grouped_duplicates.csv : contient les doublons détectés.

  - healthcare_dataset_clean.csv : dataset final prêt à être analysé.

### Structure du code

Le script s’appuie sur deux modules internes :

#### Module	Description
- clean_csv.py	Fonctions de nettoyage et de validation du CSV
- transfer_mongodb.py	Fonctions de connexion et d’insertion dans MongoDB
*Exemple d’exécution*

Dans le terminal (dans le conteneur ou en local) :  
```
python3 main.py
```

**Sortie attendue :**

[INFO] Lecture du fichier CSV...
[INFO] Nettoyage des doublons...
[INFO] Transformation pour MongoDB...
[INFO] Connexion à MongoDB établie.
[INFO] Insertion de 23500 documents terminée.
[INFO] Migration réussie !

## Résumé du fonctionnement
#### Étapes du projet

| Étape | Fichier concerné       | Action principale                                      |
|-------|-----------------------|--------------------------------------------------------|
| 1     | `main.py`             | Lance toute la pipeline                                |
| 2     | `clean_csv.py`        | Nettoie et prépare les données                        |
| 3     | `transfer_mongodb.py` | Connecte et insère les données dans MongoDB           |

---

#### Sorties générées

| Fichier                        | Description                                      |
|--------------------------------|--------------------------------------------------|
| `grouped_duplicates.csv`        | Liste des doublons détectés                       |
| `healthcare_dataset_clean.csv`  | Données nettoyées prêtes à l’analyse             |

## Conclusion

main.py est le point d’entrée du projet.
Il assure une migration automatisée, traçable et sécurisée des données médicales vers MongoDB, sans intervention manuelle.
