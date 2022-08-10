ARG VERSION=3.10-alpine


FROM python:$VERSION AS builder

WORKDIR /app

COPY redcaponfhir redcaponfhir
COPY README.md .
COPY pyproject.toml .

RUN pip install --upgrade build
RUN python -m build


FROM python:$VERSION

WORKDIR /app

COPY requirements.txt .
RUN apk add --virtual build-dependencies build-base \
    && pip install -r requirements.txt \
    && apk del build-dependencies

COPY --from=builder /app/dist/*.whl .
RUN pip install $(find . -name "*.whl")

ENTRYPOINT [ "python", "-m", "redcaponfhir" ]