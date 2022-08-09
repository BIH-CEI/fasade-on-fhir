# ERKERonFHIR

[![Python application](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/python-app.yml/badge.svg)](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/python-app.yml)
[![Docker](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/cybernop/ERKER-on-FHIR/actions/workflows/docker-publish.yml)

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
    ghcr.io/cybernop/erker-on-fhir:main
```
