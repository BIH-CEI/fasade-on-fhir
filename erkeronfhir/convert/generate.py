from typing import Any, Dict, List

from erkeronfhir.config import config
from erkeronfhir.convert.constants import (
    MAPPING_RECORD_CHOICES,
    MAPPING_RECORD_NAME,
    RECORD_FIELD_ID,
)
from fhir.resources import construct_fhir_element


def create_from_list(resource_name: str, records: List[Dict[str, str]]) -> List[Any]:
    return [create_from_single(resource_name, record) for record in records]


def create_from_single(resource_name: str, record: Dict[str, str]):
    # Start with meta information
    definitions = _get_metadata(resource_name, record[RECORD_FIELD_ID])
    for mapped_name, record_name in config.mapping[resource_name].items():
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


def _get_metadata(resource_name: str, id: int) -> Dict:
    """
    Gets meta information

    Means not only information stored in `meta` but other are not directly taken from the record
    """

    result = {
        "id": id,
        "identifier": [
            {
                "use": "usual",
                "value": f"{resource_name}/{id}",
                "system": config.fhir.system_url,
            }
        ],
    }

    profiles = config.fhir.profiles_per_resource.get(resource_name)
    meta = {}
    if profiles:
        meta["profile"] = profiles

    if meta:
        result["meta"] = meta

    return result
