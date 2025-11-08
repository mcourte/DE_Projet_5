import sys
import os
import pytest
import pandas as pd
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.transfer_mongodb import format_patient_record, insert_records_to_mongo


@pytest.fixture
def df_sample():
    """Crée un DataFrame minimal pour le test MongoDB"""
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
            "test_results": "Normal"
        }
    ])


def test_format_patient_record(df_sample):
    """Teste la transformation d'une ligne en document MongoDB"""
    row = df_sample.iloc[0]
    record = format_patient_record(row)
    assert "patient" in record
    assert "hospitalizations" in record["patient"]
    assert record["patient"]["name"] == "Alice Smith"


def test_insert_records_to_mongo(df_sample):
    """Teste l'insertion dans MongoDB via un mock"""
    mock_collection = MagicMock()
    insert_records_to_mongo(df_sample, mock_collection)

    # Vérifie que insert_many a bien été appelé une fois
    mock_collection.insert_many.assert_called_once()

    # Vérifie que le bon nombre de documents a été transmis
    args, kwargs = mock_collection.insert_many.call_args
    assert len(args[0]) == len(df_sample)
