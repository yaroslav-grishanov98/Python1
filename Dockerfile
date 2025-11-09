# Используем официальный slim-образ Python (версия 3.10 для совместимости с Django)
FROM python:3.10-slim

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их (используем кэш Docker для оптимизации)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .

# Экспортируем порт (для web-сервиса; остальные игнорируют, если не нужно)
EXPOSE 8000

