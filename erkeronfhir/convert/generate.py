from typing import Any, Dict, List

from erkeronfhir.convert.constants import (
    MAPPING_RECORD_CHOICES,
    MAPPING_RECORD_NAME,
    RECORD_FIELD_ID,
    SYSTEM_URI,
)
from fhir.resources import construct_fhir_element


def create_from_list(
    resource_name: str, records: List[Dict[str, str]], mapping, resource_profiles: Dict
) -> List[Any]:
    return [
        create_from_single(resource_name, record, mapping, resource_profiles)
        for record in records
    ]


def create_from_single(
    resource_name: str, record: Dict[str, str], mappings, resource_profiles: Dict
):
    # Start with meta information
    definitions = _get_metadata(
        resource_name, record[RECORD_FIELD_ID], resource_profiles
    )
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

    return construct_fhir_element(resource_name, definitions)


def _get_metadata(resource_name: str, id: int, resource_profiles: Dict) -> Dict:
    """
    Gets meta information

    Means not only information stored in `meta` but other are not directly taken from the record
    """

    result = {
        "meta": {"profile": resource_profiles[resource_name]},
        "id": id,
        "identifier": [
            {
                "use": "usual",
                "value": f"{resource_name}/{id}",
                "system": SYSTEM_URI,
            }
        ],
    }

    return result
