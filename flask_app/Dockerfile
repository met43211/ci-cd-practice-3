FROM python:3.11-alpine AS builder

WORKDIR /wheels

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    linux-headers

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

FROM python:3.11-alpine AS runtime

WORKDIR /app

RUN apk add --no-cache libpq

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels \
    && find /usr/local/lib/python3.11 -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
