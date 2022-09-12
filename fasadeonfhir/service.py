from typing import List

from fasadeonfhir.config import config
from fasadeonfhir.convert.generate import Mapper


class Service:
    def __init__(self) -> None:
        self.mapper = Mapper(
            config.mapping.resources,
            config.mapping.substitutions,
            config.fhir.system_url,
            config.fhir.profiles_per_resource,
        )

    def get_patients(self):
        return self._get_resources(resource_filter=["Patient"])

    def get_observations(self):
        return self._get_resources(resource_filter=["Observation"])

    def _get_resources(self, resource_filter: List[str] = None):
        records = self.provider.get_records()
        return self.mapper.create_from_list(records, resource_filter=resource_filter)
