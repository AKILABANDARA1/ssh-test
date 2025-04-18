# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the required files first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your actual script
COPY victim5.py .

# Create a non-root user with UID 10001 (valid for Choreo checks)
RUN groupadd -g 10001 appuser && useradd -u 10001 -g appuser -s /bin/sh -m appuser

# Set the user to be used for the container
USER 10001

# Expose port 8080 for the Flask app and port 2222 for SSH
EXPOSE 8080 2222

# ✅ Run your victim script
CMD ["python", "victim5.py"]
