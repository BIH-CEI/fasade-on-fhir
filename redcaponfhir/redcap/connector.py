from redcaponfhir.config import config

from redcap import Project


class RedcapConnector:
    def __init__(self) -> None:
        self.project = Project(
            config.redcap.api_url,
            config.redcap.api_token,
        )

    def get_records(self):
        return self.project.export_records()

    def get_metadata(self):
        return self.project.export_metadata()
