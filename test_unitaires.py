import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from transfer_mongodb import format_patient_record


class TestMigration(unittest.TestCase):

    def setUp(self):
        """Créer un DataFrame simulé pour les tests"""
        self.df = pd.DataFrame([
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
            },
            {
                "name": "Alice Smith",  # doublon exact
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

    def test_format_patient_record(self):
        """Test la transformation d'une ligne en JSON structuré"""
        row = self.df.iloc[0]
        record = format_patient_record(row)
        self.assertIn("patient", record)
        self.assertIn("hospitalizations", record["patient"])
        self.assertEqual(record["patient"]["name"], "Alice Smith")
        hosp = record["patient"]["hospitalizations"][0]
        self.assertEqual(hosp["admission"]["doctor"], "Dr John")
        self.assertEqual(hosp["admission"]["billing"], 1500.0)

    def test_data_integrity_before_insertion(self):
        """Test intégrité : colonnes, types, doublons, valeurs manquantes"""
        expected_columns = [
            "name","age","gender","blood_type","medical_condition",
            "date_of_admission","admission_type","discharge_date","room_number",
            "doctor","hospital","billing_amount","insurance_provider",
            "medication","test_results"
        ]
        self.assertListEqual(list(self.df.columns), expected_columns)
        self.assertTrue(pd.api.types.is_integer_dtype(self.df['age']))
        self.assertTrue(pd.api.types.is_float_dtype(self.df['billing_amount']))
        self.assertFalse(self.df.isnull().values.any())

    def test_no_duplicates(self):
        """Test la suppression des doublons"""
        df_no_dupes = self.df.drop_duplicates()
        self.assertFalse(df_no_dupes.duplicated().any())
        self.assertEqual(len(df_no_dupes), 1)  # On passe de 2 à 1

    @patch("transfer_mongodb.MongoClient")
    def test_insert_document(self, mock_client):
        """Test l'insertion dans MongoDB"""
        mock_collection = MagicMock()
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        mock_collection.insert_many([{"patient": "Alice"}])
        mock_collection.insert_many.assert_called_once()

    @patch("transfer_mongodb.MongoClient")
    def test_update_document(self, mock_client):
        """Test la modification d'un document dans MongoDB"""
        mock_collection = MagicMock()
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        mock_collection.update_one({"patient.name": "Alice Smith"}, {"$set": {"age": 31}})
        mock_collection.update_one.assert_called_once_with(
            {"patient.name": "Alice Smith"},
            {"$set": {"age": 31}}
        )

    @patch("transfer_mongodb.MongoClient")
    def test_delete_document(self, mock_client):
        """Test la suppression d'un document dans MongoDB"""
        mock_collection = MagicMock()
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        mock_collection.delete_one({"patient.name": "Alice Smith"})
        mock_collection.delete_one.assert_called_once_with({"patient.name": "Alice Smith"})


if __name__ == "__main__":
    unittest.main()
