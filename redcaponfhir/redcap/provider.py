from typing import Dict, List

from redcaponfhir.convert.constants import RECORD_FIELD_CHOICES, RECORD_FIELD_NAME
from redcaponfhir.redcap.connector import RedcapConnector


class RedcapProvider:
    def __init__(self, api_url: str, api_token: str) -> None:
        self.connector = RedcapConnector(api_url, api_token)
        self.choices = None

    def get_records(self):
        if self.choices is None:
            self.initialize_options()

        records = self.connector.get_records()
        self.replace_from_choices(records)

        return records

    def initialize_options(self) -> None:
        metadata = self.connector.get_metadata()

        choice_list = {}
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
                choice_list[entry[RECORD_FIELD_NAME]] = options

        self.choices = choice_list

    def replace_from_choices(self, records: List[Dict[str, str]]) -> None:
        for choice, options in self.choices.items():
            for record in records:
                record[choice] = options.get(record.get(choice))
