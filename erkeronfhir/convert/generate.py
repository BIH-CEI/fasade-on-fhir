from typing import Any, Dict, List

from erkeronfhir.convert.constants import (
    MAPPING_RECORD_CHOICES,
    RECORD_FIELD_ID,
    MAPPING_RECORD_NAME,
    SYSTEM_URI,
)
from fhir.resources import construct_fhir_element


def create_from_list(
    resource_name: str, records: List[Dict[str, str]], mapping
) -> List[Any]:
    return [create_from_single(resource_name, record, mapping) for record in records]


def create_from_single(resource_name: str, record: Dict[str, str], mappings):
    definitions = {}
    for mapped_name, record_name in mappings[resource_name].items():
        if isinstance(record_name, dict):
            record_name, choices = (
                record_name[MAPPING_RECORD_NAME],
                record_name[MAPPING_RECORD_CHOICES],
            )
            value = choices.get(record[record_name], None)
            if value:
                definitions[mapped_name] = value
        else:
            definitions[mapped_name] = record[record_name]

    # Add identifier
    definitions["identifier"] = [
        {
            "use": "usual",
            "value": f"{resource_name}/{record[RECORD_FIELD_ID]}",
            "system": SYSTEM_URI,
        }
    ]

    return construct_fhir_element(resource_name, definitions)
