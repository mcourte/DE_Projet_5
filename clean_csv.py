import pandas as pd

# Lecture du csv


df = pd.read_csv(
    "healthcare_dataset.csv",
    sep=",",  # séparateur entre colonnes
    skipinitialspace=True,  # ignore les espaces après le séparateur
)

# print(df.head())
# print(df.columns)
# print(df.info())


# NETTOYAGE DU CSV

## NAME

# Uniformiser les noms de patients : Prénom Nom 
# # + supprime les espaces inutiles en début ou fin de chaine de caractères
df['Name'] = df['Name'].str.title().str.strip()

# On peut voir également que certains patients ont des Mrs, Mr ou Dr devant. 
# Il faut les supprimer pour plus de cohérence
# Liste des préfixes à supprimer
prefixes = ['Dr ', 'Mr ', 'Mrs ', 'Ms ']

# Supprimer les préfixes
for prefix in prefixes:
    df['Name'] = df['Name'].str.replace(f'^{prefix}', '', regex=True, case=False)

#regex : ^Dr : ça ne supprime le prefixe que si il est en début de chaine
#case: false : insensible à la casse, supprime les prefixes qu'importe leur format DR, mRs ... 

# print(df['Name'].head())


## DOCTOR
#Uniformiser les noms des médecins
df['Doctor'] = df['Doctor'].str.title().str.strip()

# print(df['Doctor'].head())


## INSURANCE PROVIDER
#Uniformiser les noms d'assurance en enlevant les ""
df['Insurance Provider'] = df['Insurance Provider'].str.replace('"', '').str.strip()

# print(df['Insurance Provider'].head())


## BILLING AMOUNT


# Remplacer le point décimal par une virgule, et garder 2 chiffres après la virgule
# .apply(lambda x: f"{x:.2f}") : applique à chaque valeur de la colonne un format à deux chiffres après la virgule
df['Billing Amount'] = df['Billing Amount'].apply(lambda x: f"{x:.2f}".replace('.', ','))


# print(df['Billing Amount'].head())


df.to_csv("healthcare_dataset_clean.csv", index=False, sep=",", encoding="utf-8")
