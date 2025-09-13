FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Set work directory
WORKDIR /app


# Copy UV files
COPY pyproject.toml uv.lock ./
COPY README.md ./

# Default to production dependencies for safety.
# Override with --build-arg INSTALL_EXTRAS=production for production builds.
ARG INSTALL_EXTRAS=development
ENV INSTALL_EXTRAS=${INSTALL_EXTRAS}

# Install Python dependencies in a virtual environment
RUN uv venv --clear /opt/venv \
  && uv pip install --no-cache-dir ".[${INSTALL_EXTRAS}]" --python /opt/venv/bin/python \
  && uv pip list --python /opt/venv/bin/python

# Copy project files
COPY apps/ ./apps/
COPY conf/ ./conf/
COPY scripts/ ./scripts/
COPY manage.py ./
COPY templates/ ./templates/

# Make scripts executable
RUN chmod +x /app/scripts/*.sh

# Activate virtual environment for all subsequent commands
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint-django.sh"]
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
