ARG VERSION=3.12-slim

FROM python:$VERSION AS build

WORKDIR /app

RUN apt-get update && apt-get install -y curl

ENV PYTHONPATH=/app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip install uv

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen

COPY core/bini .

EXPOSE 8081

FROM build AS bini
CMD ["uv", "run", "uvicorn", "services.bini:app", "--host", "0.0.0.0", "--port", "8081"]
