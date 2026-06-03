# Python sandbox image for code execution
FROM python:3.11-slim

# Create non-root user
RUN useradd -m sandbox

# Install common test/analysis libraries
RUN pip install --no-cache-dir pytest requests numpy pandas

# Set working directory
WORKDIR /app

# Switch to non-root user
USER sandbox

# Default command
CMD ["python"]
