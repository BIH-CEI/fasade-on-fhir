from typing import List

from fhir.resources.bundle import Bundle


def create_as_bundle(resource_list: List, type_code: str = "searchset"):
    definition = {
        "type": type_code,
        "total": len(resource_list),
        "entry": [{"resource": entry} for entry in resource_list],
    }

    bundle = Bundle(**definition)
    return bundle
