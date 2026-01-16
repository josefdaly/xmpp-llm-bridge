FROM ghcr.io/astral-sh/uv:debian-slim

# Copy the script into the container
COPY ./app /app

WORKDIR /app
RUN uv sync

ENTRYPOINT ["uv", "run", "main.py"]