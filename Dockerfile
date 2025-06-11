ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION} AS base
WORKDIR /app
COPY pyproject.toml .
RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev
COPY bini_ai .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
