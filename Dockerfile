FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY redcaponfhir redcaponfhir
COPY api.py .

ENTRYPOINT [ "uvicorn", "api:app", "--host", "0.0.0.0" ]