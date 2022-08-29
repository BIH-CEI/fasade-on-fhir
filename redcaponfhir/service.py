from redcaponfhir.config import config
from redcaponfhir.convert.generate import Mapper, create_from_list
from redcaponfhir.redcap.provider import RedcapProvider


class Service:
    def __init__(self) -> None:
        self.provider = RedcapProvider(config.redcap.api_url, config.redcap.api_token)
        self.mapper = Mapper(
            config.mapping.resources,
            config.mapping.substitutions,
            config.fhir.system_url,
            config.fhir.profiles_per_resource,
        )

    def get_patients(self):
        records = self.provider.get_records()

        patients = create_from_list("Patient", records)
        return patients

    def get_observations(self):
        records = self.provider.get_records()

        observations = create_from_list("Observations", records)
        return observations
