from pathlib import Path
from typing import Dict

import yaml

CONFIG_FILE = "configs/config.yml"
MAPPING_FILE = "configs/mapping.yml"


class AuthConfig:
    def __init__(self, config_dict: Dict = {}) -> None:
        self.config_dict = config_dict

    @property
    def algorithm(self) -> str:
        return self.config_dict.get("algorithm", "")

    @property
    def secret_key(self) -> str:
        return self.config_dict.get("secret_key", "")


class FhirConfig:
    def __init__(self, config_dict: Dict = {}) -> None:
        self.config_dict = config_dict

    @property
    def system_url(self) -> str:
        return self.config_dict.get("system_uri", "")

    @property
    def profiles_per_resource(self) -> Dict:
        return self.config_dict.get("profiles", {})


class RedcapConfig:
    def __init__(self, config_dict: Dict = {}) -> None:
        self.config_dict = config_dict

    @property
    def api_url(self) -> str:
        return self.config_dict.get("api_url", "")

    @property
    def api_token(self) -> str:
        return self.config_dict.get("api_token", "")


class Config:
    def __init__(self) -> None:
        config_file = Path(CONFIG_FILE)
        mapping_file = Path(MAPPING_FILE)

        self.__config = yaml.safe_load(config_file.read_text()) if config_file.exists() else None
        self.__mapping = yaml.safe_load(mapping_file.read_text()) if mapping_file.exists() else None

        self.__auth = AuthConfig(self.__config.get("auth")) if self.__config else AuthConfig()
        self.__fhir = FhirConfig(self.__config.get("fhir")) if self.__config else FhirConfig()
        self.__redcap = (
            RedcapConfig(self.__config.get("redcap")) if self.__config else RedcapConfig()
        )

    @property
    def auth(self) -> AuthConfig:
        return self.__auth

    @property
    def fhir(self) -> FhirConfig:
        return self.__fhir

    @property
    def redcap(self) -> RedcapConfig:
        return self.__redcap

    @property
    def mapping(self) -> Dict:
        return self.__mapping

    @mapping.setter
    def mapping(self, value) -> None:
        self.__mapping = value


config = Config()
