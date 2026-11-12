FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv::0.13.8 /uv /bin/uv
WORKDIR /app
COPY . .
RUN uv sync --frozen
ENTRYPOINT ["uv", "run", "ddlml", "--help"]
