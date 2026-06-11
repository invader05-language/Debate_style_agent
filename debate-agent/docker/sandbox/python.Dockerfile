# Python sandbox image for code execution
# Security: non-root user, no network, read-only filesystem, resource limits
FROM python:3.11-slim AS base

# Install system dependencies for common Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash sandbox

# Install common test/analysis libraries
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    requests \
    numpy \
    pandas \
    httpx \
    pydantic

# Create writable temp directory for sandbox
RUN mkdir -p /tmp/sandbox && chown sandbox:sandbox /tmp/sandbox

# Set working directory
WORKDIR /app

# Switch to non-root user
USER sandbox

# Default command
CMD ["python"]
