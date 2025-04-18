# Base image: full Debian-based Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy only what's needed first (better layer caching)
COPY requirements.txt .

# Install Python dependencies (optional: add pwn tools or recon libs)
RUN pip install --no-cache-dir -r requirements.txt

# System tools for recon & networking (lean but powerful)
RUN apt update && apt install -y \
    curl \
    wget \
    netcat \
    iputils-ping \
    procps \
    vim \
    dnsutils \
    lsof \
    strace \
    tcpdump \
    bash \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Copy your main script (implant or recon tool)
COPY victim5.py .

# Optional payload/recon directory
RUN mkdir /payloads && chmod 777 /payloads

# Create a non-root user (simulating real container constraints)
RUN groupadd -g 10001 appuser && useradd -u 10001 -g appuser -s /bin/bash -m appuser

# Set the user
USER 10001

# Expose ports (if applicable)
EXPOSE 8080 2222

# Optional: default command
CMD ["python3", "victim5.py"]
