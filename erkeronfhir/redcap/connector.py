from redcap import Project


class RedcapConnector:
    def __init__(self, api_url: str, api_token: str) -> None:
        self.project = Project(api_url, api_token)

    def get_records(self):
        return self.project.export_records()

    def get_metadata(self):
        return self.project.export_metadata()


if __name__ == "__main__":
    from pathlib import Path

    import yaml

    config = yaml.safe_load(Path("config.yml").read_text())

    connector = RedcapConnector(**config["redcap"])
    records = connector.get_records()
    metadata = connector.get_metadata()
    pass
