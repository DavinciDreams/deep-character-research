# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies required for pip packages (lxml, chromadb, sentence-transformers, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

# Copy requirements.txt only for better cache usage
COPY --link requirements.txt ./

# Create virtual environment and install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

# Copy the rest of the application code (excluding .env, .git, etc. via .dockerignore)
COPY --link . .

FROM base AS final

# Create a non-root user
RUN useradd -m appuser

# Copy app source and virtual environment from builder
COPY --from=builder /app /app
COPY --from=builder /app/.venv /app/.venv

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose FastAPI port
EXPOSE 8000

USER appuser

# Default command to run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
