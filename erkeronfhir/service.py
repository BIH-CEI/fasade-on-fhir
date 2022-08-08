from erkeronfhir.convert.generate import create_from_list
from erkeronfhir.convert.metadata import fill_metadata
from erkeronfhir.redcap.connector import RedcapConnector


class Service:
    def __init__(self) -> None:
        self.connector = RedcapConnector()
        self.metadata = self.connector.get_metadata()

    def get_patients(self):
        records = self.connector.get_records()
        fill_metadata(records, self.metadata)

        patients = create_from_list("Patient", records)
        return patients
