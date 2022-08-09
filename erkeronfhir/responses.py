from fastapi.responses import JSONResponse


class FhirJsonResponse(JSONResponse):
    media_type = "application/fhir+json"
