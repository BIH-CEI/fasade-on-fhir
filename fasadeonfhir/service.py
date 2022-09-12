from typing import List

import fhir.resources
from fhir.resources.capabilitystatement import CapabilityStatement

from fasadeonfhir.config import config
from fasadeonfhir.convert.generate import Mapper
from fasadeonfhir.redcap.provider import RedcapProvider

__app_name__ = "REDCap on FHIR"


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
        return self._get_resources(resource_filter=["Patient"])

    def get_observations(self):
        return self._get_resources(resource_filter=["Observation"])

    def _get_resources(self, resource_filter: List[str] = None):
        records = self.provider.get_records()
        return self.mapper.create_from_list(records, resource_filter=resource_filter)

    def get_capability(self):
        definition = {
            "software": {"name": __app_name__},
            "fhirVersion": fhir.resources.__fhir_version__,
            "status": "active",
            "kind": "capability",
            "date": "2022-08-30",
            "format": ["json"],
            "rest": [
                {
                    "mode": "server",
                    "resource": [
                        {"type": "Patient", "interaction": [{"code": "read"}]},
                        {"type": "Observation", "interaction": [{"code": "read"}]},
                    ],
                },
            ],
        }
        return CapabilityStatement(**definition)
