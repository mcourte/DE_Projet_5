import pandas as pd
from pymongo import MongoClient
# Lire le fichier CSV nettoyé
df = pd.read_csv('healthcare_dataset_clean.csv')

# Connexion à MangoDB
client = MongoClient("mongodb://magali:Iloomph312@localhost:27017/admin")
db = client["healthcare_data"]
collection = db["data_patient"]

# Conversion du DF en dictionnaire
data_dict = df.to_dict("records")


# Insertion dans MongoDB
collection.insert_many(data_dict)
print(f"{len(data_dict)} documents insérés dans MongoDB ✅")
