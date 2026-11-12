FROM python:3.15-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY . .
RUN uv sync --frozen
ENTRYPOINT ["uv", "run", "ddlml", "--help"]
