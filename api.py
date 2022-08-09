from fastapi import FastAPI
from fastapi.responses import JSONResponse

from erkeronfhir.fhir_helpers import create_as_bundle
from erkeronfhir.responses import FhirJsonResponse
from erkeronfhir.service import Service

app = FastAPI()
service = Service()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/Patient", response_class=FhirJsonResponse)
async def get_patients():
    patients = service.get_patients()
    bundle = create_as_bundle(patients)
    return bundle.dict()
