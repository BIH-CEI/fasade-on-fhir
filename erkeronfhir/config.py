from pathlib import Path
from typing import Dict

import yaml

CONFIG_FILE = "config.yml"
MAPPINGS_FILE = "mappings.yml"


class FhirConfig:
    def __init__(self, config_dict) -> None:
        self.config_dict = config_dict

    @property
    def system_url(self) -> str:
        return self.config_dict.get("system_uri")

    @property
    def profiles_per_resource(self) -> Dict:
        return self.config_dict.get("profiles")


class RedcapConfig:
    def __init__(self, config_dict) -> None:
        self.config_dict = config_dict

    @property
    def api_url(self) -> str:
        return self.config_dict.get("api_url")

    @property
    def api_token(self) -> str:
        return self.config_dict.get("api_token")


class Config:
    def __init__(self) -> None:
        self._config = yaml.safe_load(Path(CONFIG_FILE).read_text())
        self._mappings = yaml.safe_load(Path(MAPPINGS_FILE).read_text())

        self.__fhir = FhirConfig(self._config.get("fhir"))
        self.__redcap = RedcapConfig(self._config.get("redcap"))

    @property
    def fhir(self) -> FhirConfig:
        return self.__fhir

    @property
    def redcap(self) -> RedcapConfig:
        return self.__redcap

    @property
    def mappings(self) -> Dict:
        return self._mappings


config = Config()
