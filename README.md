# REDCap on FHIR

[![Python application](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/python-app.yml/badge.svg)](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/python-app.yml)
[![Docker](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/docker-publish.yml)

## Workflow

Multiple parts:
* REDCap interface to request data using the REDCap API
    * using pycap
* Mapping from REDCap records to FHIR resources
    * dynamic specification from e.g. YAML file
* FHIR interface to provide read-access for resources
* Authentication (binding Charite AD)

@startuml
object REDCap
object REDCapInterface
object Mapping
object FHIRInterface

REDCap <- REDCapInterface
REDCapInterface <- Mapping
Mapping <- FHIRInterface
@enduml

## Start

### From Source

Start with 

```bash
uvicorn api:app --reload
```

### Using Docker

```bash
docker run --rm \
    -v $(pwd)/configs:/app/configs \
    -p 8765:8000 \
    [-e http_proxy=<proxy>]
    [-e https_proxy=<proxy>]
    ghcr.io/bih-cei/redcap-on-fhir:main
```

## Package

Install this repository as Python package using

```bash
pip install git+https://github.com/BIH-CEI/redcap-on-fhir#egg=redcap-on-fhir
```
