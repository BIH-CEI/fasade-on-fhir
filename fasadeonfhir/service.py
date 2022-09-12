from typing import List

from fhir.resources import __fhir_version__
from fhir.resources.capabilitystatement import CapabilityStatement

from fasadeonfhir.config import config
from fasadeonfhir.convert.generate import Mapper


class Service:
    __app_name__ = "Fasade on FHIR"
    __capabilities_rest__ = {}
    __capabilities_date__ = ""

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

    def get_capability(self):
        definition = {
            "software": {"name": self.__app_name__},
            "fhirVersion": __fhir_version__,
            "status": "active",
            "kind": "capability",
            "date": self.__capabilities_date__,
            "format": ["json"],
            "rest": [
                {
                    "mode": "server",
                },
            ],
        }

        if self.__capabilities_rest__:
            definition["rest"][0]["resource"] = []
            resources = definition["rest"][0]["resource"]

            for resource, capability in self.__capabilities_rest__.items():
                interactions = [{"code": item} for item in capability]
                resources.append({"type": resource, "interaction": interactions})

        return CapabilityStatement(**definition)
