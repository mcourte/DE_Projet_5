import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import pandas as pd
from app.clean_csv import  standardize_column_names, clean_names, clean_insurance_billing, remove_duplicates, check_empty_rows, check_missing_values

@pytest.fixture
def df_raw():
    """Crée un DataFrame simulé représentant les données brutes avant migration"""
    return pd.DataFrame([
        {
            "Name": "Alice Smith",
            "Age": 30,
            "Gender": "Female",
            "Blood Type": "A+",
            "Medical Condition": "Healthy",
            "Date of Admission": "2024-01-01",
            "Admission Type": "Routine",
            "Discharge Date": "2024-01-05",
            "Room Number": 101,
            "Doctor": "Dr John",
            "Hospital": "City Hospital",
            "Billing Amount": 1500.0,
            "Insurance Provider": "Blue Cross",
            "Medication": "None",
            "Test Results": "Normal"
        },
        {
            "Name": "Alice Smith",  # doublon exact
            "Age": 30,
            "Gender": "Female",
            "Blood Type": "A+",
            "Medical Condition": "Healthy",
            "Date of Admission": "2024-01-01",
            "Admission Type": "Routine",
            "Discharge Date": "2024-01-05",
            "Room Number": 101,
            "Doctor": "Dr John",
            "Hospital": "City Hospital",
            "Billing Amount": 1500.0,
            "Insurance Provider": "Blue Cross",
            "Medication": "None",
            "Test Results": "Normal"
        }
    ])

def test_columns_integrity_before_cleaning(df_raw):
    """Vérifie la présence des colonnes attendues avant nettoyage"""
    expected_columns = [
        "Name","Age","Gender","Blood Type","Medical Condition",
        "Date of Admission","Admission Type","Discharge Date","Room Number",
        "Doctor","Hospital","Billing Amount","Insurance Provider",
        "Medication","Test Results"
    ]
    assert list(df_raw.columns) == expected_columns

def test_duplicates_detection(df_raw):
    """Vérifie la présence de doublons exacts avant nettoyage"""
    duplicates = df_raw.duplicated(keep=False)
    assert duplicates.sum() == 2

def test_cleaning_pipeline(df_raw):
    """
    Teste le pipeline complet de nettoyage :
    """
    df = df_raw.copy()

    # Applique le pipeline
    df = standardize_column_names(df)
    df = clean_names(df)
    df = clean_insurance_billing(df)
    df = remove_duplicates(df)
    df = check_empty_rows(df)

    # Vérifie la présence de valeurs manquantes et lève une erreur si nécessaire
    missing_total = df.isna().sum().sum()
    if missing_total > 0:
        check_missing_values(df)  # permet d'afficher le détail dans le test
        assert missing_total == 0, f"{missing_total} valeurs manquantes détectées après nettoyage"

    # Vérifie que les colonnes sont correctement standardisées
    expected_columns = [
        "name","age","gender","blood_type","medical_condition",
        "date_of_admission","admission_type","discharge_date","room_number",
        "doctor","hospital","billing_amount","insurance_provider",
        "medication","test_results"
    ]
    assert list(df.columns) == expected_columns, "Les colonnes ne sont pas correctement standardisées"

    # Vérifie que tous les doublons complets ont été supprimés
    duplicates_mask = df.duplicated(keep=False)
    assert duplicates_mask.sum() == 0, f"{duplicates_mask.sum()} doublons complets détectés après nettoyage"

    # Vérifie qu’il n’y a pas de lignes entièrement vides
    empty_rows_count = df.isnull().all(axis=1).sum()
    assert empty_rows_count == 0, f"{empty_rows_count} lignes vides détectées après nettoyage"
