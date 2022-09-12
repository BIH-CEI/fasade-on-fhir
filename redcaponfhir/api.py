from fastapi import Depends, FastAPI

from redcaponfhir.auth import validate_token
from redcaponfhir.fhir_helpers import create_as_bundle
from redcaponfhir.responses import FhirJsonResponse
from redcaponfhir.service import Service

app = FastAPI()
service = Service()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/Patient", response_class=FhirJsonResponse)
async def get_patients(token_valid=Depends(validate_token)):
    results = service.get_patients()
    bundle = create_as_bundle(results)
    return bundle.dict()


@app.get("/Observation", response_class=FhirJsonResponse)
async def get_observations(token_valid=Depends(validate_token)):
    results = service.get_observations()
    bundle = create_as_bundle(results)
    return bundle.dict()


@app.get("/metadata", response_class=FhirJsonResponse)
async def get_metadata():
    result = service.get_capability()
    return result.dict()
