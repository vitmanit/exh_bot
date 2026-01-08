FROM python:3.12-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем ВЕСЬ проект
COPY . .

# Добавляем корень проекта в PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Создаем __init__.py файлы если их нет
RUN find /app -type d -name "*.py" -prune -o -type d -print | xargs -I {} touch {}/__init__.py 2>/dev/null || true