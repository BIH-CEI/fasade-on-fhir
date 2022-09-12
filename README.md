# Fasade on FHIR

[![Python application](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/python-app.yml/badge.svg)](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/python-app.yml)
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

## Package

Install this repository as Python package using

```bash
pip install git+https://github.com/BIH-CEI/fasdade-on-fhir@v0.1.0#egg=fasadeonfhir
```
