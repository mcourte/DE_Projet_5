import pandas as pd
from pymongo import MongoClient


def connect_mongo(uri="mongodb://magali:Iloomph312@localhost:27017/admin", db_name="healthcare_data", collection_name="data_patient"):
    """
    Se connecter à MongoDB et retourner l'objet collection.

    Args:
        uri (str): URI de connexion MongoDB.
        db_name (str): nom de la base de données.
        collection_name (str): nom de la collection.

    Returns:
        pymongo.collection.Collection: collection MongoDB prête à l'insertion.
    """
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection


def format_patient_record(row):
    """
    Transformer une ligne de DataFrame en dictionnaire structuré pour MongoDB.

    Args:
        row (pd.Series): ligne du DataFrame.

    Returns:
        dict: dictionnaire structuré pour insertion dans MongoDB.
    """
    return {
        "patient": {
            "name": row["name"],
            "age": row["age"],
            "gender": row["gender"],
            "blood_type": row["blood_type"],
            "medical_condition": row["medical_condition"],
            "hospitalizations": [
                {
                    "admission": {
                        "date": pd.to_datetime(row["date_of_admission"]),
                        "type": row["admission_type"],
                        "discharge_date": pd.to_datetime(row["discharge_date"]),
                        "room_number": row["room_number"],
                        "doctor": row["doctor"],
                        "hospital": row["hospital"],
                        "billing": row["billing_amount"],
                        "insurance": row["insurance_provider"]
                    },
                    "treatment": {
                        "medication": row["medication"],
                        "test_results": row["test_results"]
                    }
                }
            ]
        }
    }


def insert_records_to_mongo(df, collection):
    """
    Transformer le DataFrame et insérer les données dans MongoDB.

    Args:
        df (pd.DataFrame): DataFrame contenant les données.
        collection (pymongo.collection.Collection): collection MongoDB.
    """
    records = [format_patient_record(row) for _, row in df.iterrows()]
    collection.insert_many(records)
