FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "python", "app/main.py"]
