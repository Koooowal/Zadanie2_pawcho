# ======== Budowanie ========
FROM python:3.11-slim AS builder
LABEL org.opencontainers.image.authors="Jan Kowalski"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev curl && \
    pip install --upgrade pip setuptools==80.9.0 wheel && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ======== Rozruch ========
FROM python:3.11-slim
LABEL org.opencontainers.image.authors="Jan Kowalski"

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY app.py ./
COPY templates ./templates/
COPY static ./static

RUN chown -R app:app /app
USER app

EXPOSE ${PORT}

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/ || exit 1

CMD ["python", "app.py"]
