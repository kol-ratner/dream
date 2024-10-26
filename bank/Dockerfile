FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PDM_VERSION=2.19.3

WORKDIR /app

RUN pip install pdm==${PDM_VERSION}

# Copy module dependencies first
COPY modules ./modules
COPY pyproject.toml pdm.lock ./

# Install dependencies
RUN pdm install --prod

# Copy application code
COPY ./src .

ENTRYPOINT ["pdm", "run", "python", "bank/bank.py"]
