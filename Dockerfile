FROM python:3.11-slim

# Рабочая папка
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем папку app внутрь контейнера
COPY app/ .

# Команда для запуска
CMD ["python", "server.py"]