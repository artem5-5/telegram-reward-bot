FROM python:3.11-slim

# Отключаем создание pyc и буферизацию
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем системные зависимости (иногда нужны aiogram)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Сначала зависимости (для кеша)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом код
COPY . .

CMD ["python", "main.py"]