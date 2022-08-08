import unittest

from erkeronfhir.convert.generate import create_from_single
from fhir.resources.patient import Patient


class TestGenerateFromSingle(unittest.TestCase):
    def test_simple(self):
        mappings = {"Patient": {"name": "PatientName"}}

        PATIENT_NAME = "TestPatient"

        record = {"PatientName": PATIENT_NAME}

        result = create_from_single("Patient", record, mappings)

        self.assertIsInstance(result, Patient)
        self.assertEqual(result.name, PATIENT_NAME)
