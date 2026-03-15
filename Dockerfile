FROM python:3.11-slim

WORKDIR /app

# Copy source files
COPY requirements.txt ./
RUN grep -vE '^(pytest|pytest-)\b' requirements.txt > requirements.runtime.txt \
    && pip install --no-cache-dir -r requirements.runtime.txt \
    && rm requirements.runtime.txt

COPY app.py ./
COPY src/ ./src/
COPY web/ ./web/
COPY config/ ./config/

# Create output directory
RUN mkdir -p /data

ENV HOST=0.0.0.0 \
    PORT=8003 \
    DATA_DIR=/data \
    LOG_LEVEL=INFO \
    STORAGE_BACKEND=file

EXPOSE 8003

CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "8003", "--data-dir", "/data"]
