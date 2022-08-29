from redcaponfhir.config import config
from redcaponfhir.convert.generate import create_from_list
from redcaponfhir.redcap.provider import RedcapProvider


class Service:
    def __init__(self) -> None:
        self.provider = RedcapProvider(config.redcap.api_url, config.redcap.api_token)

    def get_patients(self):
        records = self.provider.get_records()

        patients = create_from_list("Patient", records)
        return patients
