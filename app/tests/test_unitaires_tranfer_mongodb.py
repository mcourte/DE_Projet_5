import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from app.transfer_mongodb import format_patient_record, insert_records_to_mongo

@pytest.fixture
def df_sample():
    """DataFrame simulé pour tests MongoDB"""
    return pd.DataFrame([{
        "name": "Alice Smith",
        "age": 30,
        "gender": "Female",
        "blood_type": "A+",
        "medical_condition": "Healthy",
        "date_of_admission": "2024-01-01",
        "admission_type": "Routine",
        "discharge_date": "2024-01-05",
        "room_number": 101,
        "doctor": "Dr John",
        "hospital": "City Hospital",
        "billing_amount": 1500.0,
        "insurance_provider": "Blue Cross",
        "medication": "None",
        "test_results": "Normal"
    }])

def test_format_patient_record_structure(df_sample):
    """Teste la transformation d'une ligne en document MongoDB"""
    row = df_sample.iloc[0]
    record = format_patient_record(row)
    assert "patient" in record
    assert "hospitalizations" in record["patient"]
    hosp = record["patient"]["hospitalizations"][0]
    assert hosp["admission"]["doctor"] == "Dr John"
    assert hosp["admission"]["billing"] == 1500.0

@patch("transfer_mongodb.MongoClient")
def test_insert_records(mock_client, df_sample):
    """Teste l'insertion des documents dans MongoDB via mock"""
    mock_collection = MagicMock()
    mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

    insert_records_to_mongo(df_sample, mock_collection)

    # Vérifie que insert_many a bien été appelé
    mock_collection.insert_many.assert_called_once()
