# syntax=docker/dockerfile:1

# Stage 1: Get the official uv binary (tiny, official image)
FROM ghcr.io/astral-sh/uv:latest AS uv

# Stage 2: Final image
FROM python:3.11-slim

# Copy uv from the official image
COPY --from=uv /uv /usr/bin/uv

# Create non-root user (best practice)
RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser/app

# Copy lockfile + pyproject.toml first (best Docker layer caching)
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Install dependencies (cached if lockfile unchanged)
RUN uv sync --frozen --no-cache

# Copy source code
COPY --chown=appuser:appuser src ./src

# Optional: make project editable (nice for dev)
# RUN uv sync --frozen

# Default command
CMD ["uv", "run", "src/report_generator.py"]
