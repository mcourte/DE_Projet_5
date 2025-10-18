import pandas as pd
import os


def read_csv(file_path: str) -> pd.DataFrame:
    """Lit le CSV et retourne un DataFrame"""
    return pd.read_csv(file_path, sep=",", skipinitialspace=True)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Met les noms de colonnes en minuscules et remplace les espaces par des _"""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df


def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    """Uniformise les noms de patients et médecins"""
    prefixes = ['Dr ', 'Mr ', 'Mrs ', 'Ms ', 'Dr. ', 'Mr. ', 'Mrs. ', "Ms. "]
    df['name'] = df['name'].str.title().str.strip()
    for prefix in prefixes:
        df['name'] = df['name'].str.replace(f'^{prefix}', '', regex=True, case=False)
    df['doctor'] = df['doctor'].str.title().str.strip()
    return df


def clean_insurance_billing(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les colonnes assurance et montant"""
    df['insurance_provider'] = df['insurance_provider'].str.replace('"', '').str.strip()
    df['billing_amount'] = df['billing_amount'].apply(lambda x: f"{x:.2f}".replace('.', ','))
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les doublons dans le DataFrame"""
    df = df.drop_duplicates()
    return df


def save_csv(df: pd.DataFrame, file_path: str):
    """Sauvegarde le DataFrame nettoyé en CSV"""
    df.to_csv(file_path, index=False, sep=",", encoding="utf-8")


def clean_csv(file_path: str, output_path: str) -> pd.DataFrame:
    """Pipeline complet de nettoyage du CSV"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    
    df = read_csv(file_path)
    df = standardize_column_names(df)
    df = clean_names(df)
    df = clean_insurance_billing(df)
    df = remove_duplicates(df)
    save_csv(df, output_path)
    return df
