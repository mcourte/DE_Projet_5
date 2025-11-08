import sys
import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.transfer_mongodb import insert_records


@pytest.fixture
def df_sample():
    """Crée un petit DataFrame de test"""
    return pd.DataFrame([
        {
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
            "test_results": "Normal",
        }
    ])


@patch("app.transfer_mongodb.MongoClient")
def test_insert_records(mock_mongo, df_sample):
    """Teste l'insertion de documents dans MongoDB avec mock"""
    mock_collection = MagicMock()
    mock_mongo.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

    inserted_count = insert_records(df_sample, "mongodb://fake_uri", "healthcare_data", "patients")

    mock_collection.insert_many.assert_called_once()
    assert inserted_count == 1
