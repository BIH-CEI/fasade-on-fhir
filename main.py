from redcaponfhir.config import config
from redcaponfhir.convert.generate import Mapper
from redcaponfhir.redcap.provider import RedcapProvider

connector = RedcapProvider(config.redcap.api_url, config.redcap.api_token)
records = connector.get_records()

mapper = Mapper(
    config.mapping.resources,
    config.mapping.substitutions,
    config.fhir.system_url,
    config.fhir.profiles_per_resource,
)

results = mapper.create_from_list(records, resource_filter=["Observation"])

pass
