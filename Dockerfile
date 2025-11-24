# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr b/bin/uv

WORKDIR /app

# Copy lockfile and install dependencies (super fast cached layer)
ADD uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project

# Copy source code
ADD src ./src

# Install the actual project in editable mode (optional but nice)
RUN uv sync --frozen

CMD ["uv", "run", "src/report_generator.py"]
