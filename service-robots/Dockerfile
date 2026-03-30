FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY service-robots/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY service-robots/ ./
ENV PYTHONUNBUFFERED=1
RUN useradd -r -s /bin/false robotuser
USER robotuser
# The specific robot script and port are set via CMD and EXPOSE in docker-compose
CMD ["python", "medical_robot.py"]
