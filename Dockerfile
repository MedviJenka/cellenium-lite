ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION} AS bini
WORKDIR /app
COPY pyproject.toml .
RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev
COPY bini_ai .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]


FROM bini AS mcp-server
WORKDIR /app
COPY bini_ai/src/server .
CMD ["mcp", "dev", "mcp.py"]
