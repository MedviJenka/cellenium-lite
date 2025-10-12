ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION} AS build
WORKDIR /app
COPY pyproject.toml .
ENV PATH='/app/.venv/bin:$PATH'
RUN pip install --upgrade pip uv
RUN uv sync --frozen --no-cache
COPY bini_ai .


FROM build AS bini
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
