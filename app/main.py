from clean_csv import clean_csv
from transfer_mongodb import connect_mongo, insert_records_to_mongo


def main():
    """
    Fonction principale :
    - Nettoie le CSV et crée le CSV nettoyé si nécessaire
    - Transforme les données pour MongoDB
    - Insère les documents dans la collection MongoDB
    """
    input_csv = "app/healthcare_dataset.csv"
    output_csv = "data/healthcare_dataset_clean.csv"

    # Nettoyage du CSV et récupération du DataFrame nettoyé
    df_clean = clean_csv(input_csv, output_csv)

    # Connexion à MongoDB
    collection = connect_mongo()

    # Transformation + insertion dans MongoDB
    insert_records_to_mongo(df_clean, collection)

    print(f"{len(df_clean)} documents insérés dans MongoDB.")


if __name__ == "__main__":
    main()
