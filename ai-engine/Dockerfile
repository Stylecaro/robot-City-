FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ && rm -rf /var/lib/apt/lists/*
COPY ai-engine/requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
RUN pip install --no-cache-dir --prefix=/install prometheus-client psutil

FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /install /usr/local
COPY ai-engine/ ./
ENV PYTHONUNBUFFERED=1
EXPOSE 8765
RUN useradd -r -s /bin/false aiuser
USER aiuser
CMD ["python", "main.py"]
