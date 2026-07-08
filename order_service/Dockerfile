FROM python:3.13-slim AS builder

RUN apt update && apt install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipx && \
    pipx install poetry==2.4.1

RUN pipx inject poetry poetry-plugin-export

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry export --only main --without-hashes -o requirements.txt

FROM python:3.13-slim AS runtime

RUN apt update && apt install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache-dir --disable-pip-version-check \
    -r requirements.txt

WORKDIR /app
COPY --chown=appuser:appuser src/. .
COPY --chown=appuser:appuser migrations/ migrations/
COPY --chown=appuser:appuser alembic.ini .

USER appuser

CMD ["uvicorn", "order_service.main:app", "--host", "0.0.0.0", "--port", "8000"]

