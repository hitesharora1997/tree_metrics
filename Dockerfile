# --- Builder stage ---
FROM python:3.9-slim as builder

WORKDIR /build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --target=/build/deps -r requirements.txt

# --- Runtime stage ---
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/deps /usr/local/lib/python3.9/site-packages

COPY src/ /app/src/
COPY main.py config.py README.md /app/

RUN mkdir -p data outputs logs

ENTRYPOINT ["python", "main.py"]

CMD ["--help"]
