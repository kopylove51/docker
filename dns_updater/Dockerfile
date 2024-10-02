FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Копируем файл requirements.txt (тут необходимые библиотеки для работы приложения)
COPY requirements.txt /app/

# Устанавливаем зависимости из requirements.txt (читсим кэш, чтобы облегчить образ)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт
COPY mgs-dns-updater.py /app/

# Переменные окружения (оставляем пустыми, зададим в docker-compose)
ENV CF_API_TOKEN=
ENV CF_ZONE_ID=
ENV CF_DNS_NAME=
ENV CF_TTL=

# Запуск скрипта
CMD ["python", "mgs-dns-updater.py"]