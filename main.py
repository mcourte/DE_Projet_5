from clean_csv import clean_data
import pandas as pd
from transfer_mongodb import connect_mongo, insert_records_to_mongo


def main():
    """
    Fonction principale : nettoie le CSV, lit les données et les insère dans MongoDB.
    """
    # Nettoyage du CSV et création si nécessaire
    csv_path = clean_data("healthcare_dataset.csv")  # renvoie le chemin du CSV nettoyé

    # Lecture du CSV nettoyé
    df = pd.read_csv(csv_path)

    # Connexion à MongoDB
    collection = connect_mongo()

    # Transformation + insertion
    insert_records_to_mongo(df, collection)


if __name__ == "__main__":
    main()
