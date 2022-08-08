from pathlib import Path

import yaml

from erkeronfhir.convert.generate import create_from_list
from erkeronfhir.convert.metadata import fill_metadata
from erkeronfhir.redcap.connector import RedcapConnector


class Service:
    def __init__(
        self, config_file: str = "config.yml", mappings_file: str = "mappings.yml"
    ) -> None:
        self.config = yaml.safe_load(Path(config_file).read_text())
        self.mappings = yaml.safe_load(Path(mappings_file).read_text())

        self.connector = RedcapConnector(**self.config["service"]["redcap"])
        self.metadata = self.connector.get_metadata()

    def get_patients(self):
        records = self.connector.get_records()
        fill_metadata(records, self.metadata)

        patients = create_from_list(
            "Patient", records, self.mappings, self.config["profiles"]
        )
        return patients
