FROM python:3.9

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install only essential tools (using actual package names)
RUN apt update && apt install -y \
    curl \
    wget \
    netcat-openbsd \
    iputils-ping \
    procps \
    vim \
    && apt clean && rm -rf /var/lib/apt/lists/*

COPY victim5.py .

# Optional payload dir
RUN mkdir /payloads && chmod 777 /payloads

# Create non-root user
RUN groupadd -g 10001 appuser && useradd -u 10001 -g appuser -s /bin/bash -m appuser

USER 10001

EXPOSE 8080 2222

CMD ["python3", "victim5.py"]
