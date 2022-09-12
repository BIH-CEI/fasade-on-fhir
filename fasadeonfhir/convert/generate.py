import json
import re
from typing import Any, Dict, List

from fasadeonfhir.convert.constants import RECORD_FIELD_ID
from fasadeonfhir.helpers import clean_empty
from fhir.resources import construct_fhir_element
from jinja2 import Template


class Mapper:
    def __init__(
        self,
        resource_mappings: List[Dict[str, Any]],
        substitutions: Dict[str, Dict[str, str]],
        system_url: str,
        resource_profiles: Dict[str, List[str]],
    ) -> None:
        self.substitutions = substitutions
        self.system_url = system_url
        self.resource_profiles = resource_profiles

        self.generate_resource_templates(resource_mappings)

    def generate_resource_templates(self, mappings: List[Dict[str, Any]]):
        self.resource_templates = []
        for entry in mappings:
            name, template_dict = entry.popitem()
            string_template = json.dumps(template_dict)
            string_template = re.sub(r"\$(\w+)", r"{{ \1 }}", string_template)
            self.resource_templates.append((name, Template(string_template)))

    def create_from_list(
        self, records: List[Dict[str, str]], resource_filter: List[str] = None
    ) -> List[Any]:
        result = []
        for record in records:
            resources = self.generate_from_record(record, resource_filter)
            result += resources
        return result

    def generate_from_record(self, record: Dict[str, str], resource_filter: List[str] = None):
        # Fill substitutions
        self._apply_substitutions(record)

        resources = []
        for resource, template in self.resource_templates:
            if resource_filter and resource not in resource_filter:
                continue

            metadata = self._generate_metadata(resource, record[RECORD_FIELD_ID])
            resource = self._generate_resource_from_record(record, metadata, resource, template)
            resources.append(resource)
        return resources

    def _generate_resource_from_record(
        self,
        record: Dict[str, str],
        metadata: Dict,
        resource_name: str,
        resource_template: Template,
    ):
        rendered = resource_template.render(**record)
        definitions = json.loads(rendered)
        definitions.update(metadata)
        definitions = clean_empty(definitions)

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
        if (profiles := self.resource_profiles.get(resource_name)) is not None:
            meta["profile"] = profiles

        if meta:
            result["meta"] = meta

        return result

    def _apply_substitutions(self, record: Dict[str, str]) -> None:
        for entry, value in record.items():
            if entry in self.substitutions:
                record[entry] = self.substitutions[entry].get(value)
