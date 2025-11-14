#Базовый образ — Linux с Python
FROM python:3.11-slim

#Рабочая папка внутри контейнера
WORKDIR /app

#Скопировать зависимости
COPY requirements.txt .

#Установить зависимости
RUN pip install -r requirements.txt

#Скопировать код внутрь контейнера
COPY ./app ./app/

#Команда для запуска
CMD ["python", "server.py"]
