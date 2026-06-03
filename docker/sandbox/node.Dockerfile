# Node.js sandbox image for code execution
FROM node:20-slim

# Create non-root user
RUN useradd -m sandbox

# Set working directory
WORKDIR /app

# Switch to non-root user
USER sandbox

# Default command
CMD ["node"]
