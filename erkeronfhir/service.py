from pathlib import Path

import yaml

from erkeronfhir.convert.generate import create_from_list
from erkeronfhir.convert.metadata import fill_metadata
from erkeronfhir.redcap.connector import RedcapConnector

config = yaml.safe_load(Path("config.yml").read_text())
mapping = yaml.safe_load(Path("mappings.yml").read_text())

connector = RedcapConnector(**config["redcap"])
records = connector.get_records()
metadata = connector.get_metadata()

fill_metadata(records, metadata)

patients = create_from_list("Patient", records, mapping)


class Service:
    def __init__(
        self, config_file: str = "config.yml", mappings_file: str = "mappings.yml"
    ) -> None:
        self.config = yaml.safe_load(Path(config_file).read_text())
        self.mappings = yaml.safe_load(Path(mappings_file).read_text())

        self.connector = RedcapConnector(**self.config["redcap"])
        self.metadata = connector.get_metadata()

    def get_patients(self):
        records = self.connector.get_records()
        fill_metadata(records, metadata)

        patients = create_from_list("Patient", records, mapping)
        return patients
