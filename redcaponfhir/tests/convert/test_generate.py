import unittest

from fhir.resources.patient import Patient
from redcaponfhir.config import config
from redcaponfhir.convert.generate import create_from_single


class TestGenerateFromSingle(unittest.TestCase):
    @unittest.expectedFailure
    def test_simple(self):
        config.mapping = {"Patient": {"name": "PatientName"}}

        PATIENT_NAME = "TestPatient"

        record = {"PatientName": PATIENT_NAME, "record_id": 1}

        result = create_from_single("Patient", record)

        self.assertIsInstance(result, Patient)
        self.assertEqual(result.name, PATIENT_NAME)
