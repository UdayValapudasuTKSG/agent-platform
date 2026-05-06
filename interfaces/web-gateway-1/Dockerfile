FROM python:3.11-slim

WORKDIR /app

# Copy libs
COPY libs /app/libs
# Copy gateway code
COPY interfaces/web-gateway-1 /app/interfaces/web-gateway-1

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn google-cloud-aiplatform google-cloud-secret-manager pydantic

# Set python path to include libs
ENV PYTHONPATH=$PYTHONPATH:/app

EXPOSE 8080

CMD ["uvicorn", "interfaces.web-gateway-1.main:app", "--host", "0.0.0.0", "--port", "8080"]
