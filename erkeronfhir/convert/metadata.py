from typing import Dict, List

from erkeronfhir.convert.constants import RECORD_FIELD_CHOICES, RECORD_FIELD_NAME


def fill_metadata(records: List[Dict[str, str]], metadata: List[Dict]):
    choices = _get_choices(metadata)
    _replace_with_choices(records, choices)


def _get_choices(metadata: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    result = {}
    for entry in metadata:
        choices = entry.get(RECORD_FIELD_CHOICES, None)
        if choices:
            choices = choices.split("|")

            if len(choices) < 2:
                continue

            options = {}
            for choice in choices:
                key, value = tuple(choice.split(",", maxsplit=1))
                options[key.strip()] = value.strip()
            result[entry[RECORD_FIELD_NAME]] = options

    return result


def _replace_with_choices(
    records: List[Dict[str, str]], choices: Dict[str, Dict[str, str]]
) -> None:
    for entry in records:
        for key in entry.keys():
            if key in choices:
                value = choices[key].get(entry[key], None)
                if value:
                    entry[key] = value
