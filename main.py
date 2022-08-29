from redcaponfhir.config import config
from redcaponfhir.convert.generate import create_from_list
from redcaponfhir.redcap.provider import RedcapProvider

connector = RedcapProvider(config.redcap.api_url, config.redcap.api_token)
records = connector.get_records()

patients = create_from_list("Patient", records)

pass
