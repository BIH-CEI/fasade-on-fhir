from typing import Any, Dict, List

from fhir.resources import construct_fhir_element


def create_from_list(
    resource_name: str, records: List[Dict[str, str]], mapping
) -> List[Any]:
    return [create_from_single(resource_name, record, mapping) for record in records]


RECORD_NAME = "name"
RECORD_CHOICES = "choices"
RECORD_ID = "record_id"
SYSTEM_URI = "https://redcap.charite.de/genAdipositas"


def create_from_single(resource_name: str, record: Dict[str, str], mappings):
    definitions = {}
    for mapped_name, record_name in mappings[resource_name].items():
        if isinstance(record_name, dict):
            record_name, choices = record_name[RECORD_NAME], record_name[RECORD_CHOICES]
            value = choices.get(record[record_name], None)
            if value:
                definitions[mapped_name] = value
        else:
            definitions[mapped_name] = record[record_name]

    # Add identifier
    definitions["identifier"] = [
        {
            "use": "usual",
            "value": f"{resource_name}/{record[RECORD_ID]}",
            "system": SYSTEM_URI,
        }
    ]

    return construct_fhir_element(resource_name, definitions)
