import os
import pandas as pd
from pymongo import MongoClient


def connect_mongo():
    """
    Connexion à MongoDB en local avec authentification.
    Retourne la collection 'patients' de la base 'healthcare_data'.
    """
    # Informations de connexion
    mongo_host = os.getenv("MONGO_HOST", "localhost") 
    mongo_port = int(os.getenv("MONGO_PORT", 27017))  
    mongo_db = os.getenv("MONGO_DB", "healthcare_data")
    mongo_user = os.getenv("MONGO_USER", "magali")
    mongo_password = os.getenv("MONGO_PASSWORD", "Iloomph312")
    auth_db = os.getenv("MONGO_AUTH_DB", "admin")      

    # Création du client Mongo
    client = MongoClient(
        host=mongo_host,
        port=mongo_port,
        username=mongo_user,
        password=mongo_password,
        authSource=auth_db,
        authMechanism='SCRAM-SHA-256'  
    )

    # Sélection de la collection
    collection = client[mongo_db]["patients"]
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
            "gender": row["gender"],
            "blood_type": row["blood_type"],
            "hospitalizations": [
                {
                    "admission": {
                        "age": row["age"],
                        "medical_condition": row["medical_condition"],
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
