from redcaponfhir.convert.generate import create_from_list
from redcaponfhir.convert.metadata import fill_metadata
from redcaponfhir.redcap.connector import RedcapConnector

connector = RedcapConnector()
records = connector.get_records()
metadata = connector.get_metadata()

fill_metadata(records, metadata)

patients = create_from_list("Patient", records)

pass
