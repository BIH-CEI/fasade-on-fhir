import unittest

from erkeronfhir.config import config
from erkeronfhir.convert.generate import create_from_single
from fhir.resources.patient import Patient


class TestGenerateFromSingle(unittest.TestCase):
    def test_simple(self):
        config.mapping = {"Patient": {"name": "PatientName"}}

        PATIENT_NAME = "TestPatient"

        record = {"PatientName": PATIENT_NAME, "record_id": 1}

        result = create_from_single("Patient", record)

        self.assertIsInstance(result, Patient)
        self.assertEqual(result.name, PATIENT_NAME)
