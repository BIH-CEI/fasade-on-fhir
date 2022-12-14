from typing import Dict, List

from fhir.resources.bundle import Bundle


def create_as_bundle(resource_list: List, type_code: str = "searchset") -> Bundle:
    definition = {
        "type": type_code,
        "total": len(resource_list),
        "entry": [{"resource": entry} for entry in resource_list],
    }

    bundle = Bundle(**definition)
    return bundle


def as_bundle_dict(resource_list: List, type_code: str = "searchset") -> Dict:
    bundle = create_as_bundle(resource_list, type_code)
    return bundle.dict()
