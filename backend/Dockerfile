FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app

EXPOSE 5000

CMD ["uvicorn", "crmevent.main:app", "--host", "0.0.0.0", "--port", "5000"]