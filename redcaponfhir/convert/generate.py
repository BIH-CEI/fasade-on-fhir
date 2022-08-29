from typing import Any, Dict, List

from fhir.resources import construct_fhir_element
from redcaponfhir.convert.constants import (
    MAPPING_RECORD_CHOICES,
    MAPPING_RECORD_NAME,
    RECORD_FIELD_ID,
)


class Mapper:
    def __init__(
        self,
        resource_mappings: Dict[str, Any],
        substitutions: Dict[str, Dict[str, str]],
        system_url: str,
        resource_profiles: Dict[str, List[str]],
    ) -> None:
        self.resource_mappings = resource_mappings
        self.substitutions = substitutions
        self.system_url = system_url
        self.resource_profiles = resource_profiles

    def create_from_list(self, resource_name: str, records: List[Dict[str, str]]) -> List[Any]:
        return [self.create_from_single(resource_name, record) for record in records]

    def create_from_single(self, resource_name: str, record: Dict[str, str]):
        # Fill substitutions
        self._apply_substitutions(record)

        # Start with meta information
        definitions = self._generate_metadata(resource_name, record[RECORD_FIELD_ID])

        for mapped_name, record_name in self.resource_mappings[resource_name].items():
            if isinstance(record_name, dict):
                record_name, choices = (
                    record_name[MAPPING_RECORD_NAME],
                    record_name[MAPPING_RECORD_CHOICES],
                )
                value = choices.get(record[record_name], None)
            else:
                value = record.get(record_name, None)

            if value:
                definitions[mapped_name] = value

        return construct_fhir_element(resource_name, definitions)

    def _generate_metadata(self, resource_name: str, id: int) -> Dict:
        """
        Generate meta information

        Means not only information stored in `meta` but other are not directly
        taken from the record
        """

        result = {
            "id": id,
            "identifier": [
                {
                    "use": "usual",
                    "value": f"{resource_name}/{id}",
                    "system": self.system_url,
                }
            ],
        }

        meta = {}
        if profiles := self.resource_profiles.get(resource_name) is not None:
            meta["profile"] = profiles

        if meta:
            result["meta"] = meta

        return result

    def _apply_substitutions(self, record: Dict[str, str]) -> None:
        for entry, value in record.items():
            if entry in self.substitutions:
                record[entry] = self.substitutions[entry].get(value)
