FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PDM_VERSION=2.19.3

WORKDIR /app

RUN pip install pdm==${PDM_VERSION}
COPY pyproject.toml pdm.lock ./
RUN pdm install --prod
COPY ./src .

ENTRYPOINT ["pdm", "run", "python", "store/store.py"]
