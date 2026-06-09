# Node.js sandbox image for code execution
# Security: non-root user, no network, read-only filesystem, resource limits
FROM node:20-slim AS base

# Create non-root user
RUN useradd -m -s /bin/bash sandbox

# Install common npm packages globally
RUN npm install -g \
    jest \
    typescript \
    ts-node \
    && npm cache clean --force

# Create writable temp directory for sandbox
RUN mkdir -p /tmp/sandbox && chown sandbox:sandbox /tmp/sandbox

# Set working directory
WORKDIR /app

# Switch to non-root user
USER sandbox

# Default command
CMD ["node"]
