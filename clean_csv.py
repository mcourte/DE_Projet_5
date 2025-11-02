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
    """
    Détecte et enregistre tous les doublons du DataFrame.

    - Les doublons (originaux + copies) sont enregistrés dans grouped_duplicates.csv
      avec l'original suivi immédiatement de ses copies.
    - Supprime les doublons du DataFrame original en gardant le premier exemplaire.
    """
    output_path = "app/grouped_duplicates.csv"

    # Clé temporaire pour identifier les doublons
    df['_dup_key'] = df.apply(tuple, axis=1)

    # Masque des doublons
    duplicate_mask = df.duplicated(subset='_dup_key', keep=False)

    # 🟢 Aucun doublon trouvé → on nettoie la clé temporaire et on continue
    if not duplicate_mask.any():
        print("✅ Aucun doublon détecté.")
        df = df.drop(columns='_dup_key')
        return df

    # 🔵 Doublons détectés → regrouper et sauvegarder
    ordered_duplicates = [
        df[df['_dup_key'] == key] for key in df.loc[duplicate_mask, '_dup_key'].unique()
    ]

    # Sécurité : vérifier qu'il y a bien des groupes avant concaténation
    if ordered_duplicates:
        duplicates_ordered = pd.concat(ordered_duplicates)
        duplicates_ordered = duplicates_ordered.drop(columns='_dup_key')
        duplicates_ordered.to_csv(output_path, index=False)
        print(f"💾 Doublons enregistrés dans le fichier : {output_path}")
        print(f"{len(duplicates_ordered)} doublon(s) supprimé(s).")
    else:
        duplicates_ordered = pd.DataFrame()
        print("⚠️ Aucun groupe de doublons à enregistrer.")

    # Supprimer les doublons dans le DataFrame original
    df = df.drop_duplicates(subset='_dup_key').drop(columns='_dup_key')
    print(f"📉 Taille du DataFrame après nettoyage : {len(df)} lignes.")

    return df




def check_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie la présence de lignes entièrement vides dans le DataFrame.

    Affiche le nombre de lignes vides.
    Retourne le DataFrame sans ces lignes.
    """
    empty_rows = df.isnull().all(axis=1).sum()
    if empty_rows > 0:
        print(f"{empty_rows} lignes vides trouvées et supprimées.")
        df = df.dropna(how="all")
    else:
        print("Aucune ligne vide trouvée.")
    return df

def check_missing_values(df: pd.DataFrame) -> None:
    """
    Vérifie si certaines colonnes contiennent des valeurs manquantes (NaN ou vides)

    - Affiche le nombre total de cellules manquantes.
    - Indique les colonnes concernées et leur pourcentage de valeurs manquantes.
    - Affiche les lignes contenant au moins une valeur manquante.
    """
    total_missing = df.isna().sum().sum()

    if total_missing == 0:
        print("Aucune valeur manquante détectée dans le DataFrame.")
        return

    print(f" {total_missing} valeur(s) manquante(s) détectée(s).")
    print("\n Détail des colonnes concernées :")
    missing_per_column = df.isna().sum()
    for col, count in missing_per_column.items():
        if count > 0:
            pct = (count / len(df)) * 100
            print(f"  - {col}: {count} valeurs manquantes ({pct:.2f}%)")

    print("\n Aperçu des lignes contenant au moins une valeur manquante :")
    rows_with_missing = df[df.isna().any(axis=1)]
    print(rows_with_missing)


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
    df = check_empty_rows(df)
    check_missing_values(df)
    save_csv(df, output_path)
    return df
