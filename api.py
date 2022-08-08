from fastapi import FastAPI

from erkeronfhir.fhir_helpers import create_as_bundle
from erkeronfhir.service import Service

app = FastAPI()
service = Service()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/Patient")
async def get_patients():
    patients = service.get_patients()
    bundle = create_as_bundle(patients)
    return bundle.dict()
