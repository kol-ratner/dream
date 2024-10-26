FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PDM_VERSION=2.19.3

WORKDIR /app

RUN pip install pdm==${PDM_VERSION}

# Copy dependencies first
COPY modules /modules
COPY bank/pyproject.toml bank/pdm.lock ./

# Install dependencies
RUN pdm install --prod

# Copy application code
COPY bank/src .

ENTRYPOINT ["pdm", "run", "python", "bank/bank.py"]
