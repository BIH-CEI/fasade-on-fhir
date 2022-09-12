import unittest

from fasadeonfhir.convert.generate import Mapper
from fhir.resources.patient import Patient


class TestGenerateFromSingle(unittest.TestCase):
    @unittest.expectedFailure
    def test_simple(self):
        mapping = {"Patient": {"name": "$PatientName"}}

        PATIENT_NAME = "TestPatient"

        record = {"PatientName": PATIENT_NAME, "record_id": 1}

        mapper = Mapper(mapping, [], "", {})
        result = mapper.generate_from_record(record, resource_filter=["Patient"])

        self.assertIsInstance(result, Patient)
        self.assertEqual(result.name, PATIENT_NAME)
