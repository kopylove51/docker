from os import makedirs, path, getenv
from subprocess import run
from socket import gethostbyname
from requests import get, put
from time import sleep
import logging
import sys
from datetime import datetime

# Создаем папку logs, если она не существует
log_dir = 'logs'
makedirs(log_dir, exist_ok=True)

api_token = getenv("CF_API_TOKEN")
zone_id = getenv("CF_ZONE_ID")
dns_name = getenv("CF_DNS_NAME")
ttl = getenv("CF_TTL")

# Ежедневное создание нового лог файла
def setup_logging():
    log_file = path.join(log_dir, f'dns_update_{datetime.now().strftime("%Y-%m-%d")}.log')
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)

# Функция поиска record_id
def get_record_id(zone_id, dns_name, retries=3, delay=10): #Можно поменять кол-во попыток и дилей между ними
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    params = {
        "name": dns_name
    }

    attempt = 0
    while attempt < retries:
        attempt += 1
        logging.info(f"Получение record_id для {dns_name}")

        # Отправляем запрос на получение DNS-записей зоны
        response = get(url, headers=headers, params=params)

        if response.status_code == 200:
            records = response.json().get('result', [])
            if records:
                record_id = records[0].get('id')  # Получаем ID первой записи
                logging.info(f"Record ID для {dns_name}: {record_id}")
                return record_id
            else:
                logging.error(f"DNS-запись с именем {dns_name} не найдена.")
                return None  # Если запись не найдена, возвращаем None
        else:
            logging.error(f"Ошибка при получении record_id: {response.status_code}")
            logging.error(response.json())

        # Дилей перед новой попыткой
        logging.info(f"Следующая попытка запроса состоится через {delay} секунд...")
        sleep(delay)

    logging.error(f"Не удалось получить record_id после {retries} попыток. Проверьте предоставленные данные.")
    sys.exit("Ошибка: Не удалось получить record_id после нескольких попыток.")

def update_dns_record():

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"

    url_ip = 'https://icanhazip.com/'
    fact_ip = run(['curl', '-s', url_ip], capture_output=True, text=True)
    fact_ip = fact_ip.stdout.strip()

    ip_address = gethostbyname(dns_name)
    logging.info(f"fact_ip: {fact_ip}")
    logging.info(f"cloudflare_ip: {ip_address}")

    if fact_ip != ip_address:
        # Данные для обновления DNS-записи
        data = {
            "type": "A",  # или "AAAA" для IPv6
            "name": dns_name,  # Доменное имя, которое обновляется
            "content": fact_ip,  # Новый IP-адрес
            "ttl": int(ttl),  # Время жизни (TTL) записи
            "proxied": False  # True если вы хотите использовать Cloudflare proxy, False если нет
        }

        # Заголовки для запроса
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        # Отправка запроса
        response = put(url, json=data, headers=headers)

        # Проверка результата
        if response.status_code == 200:
            logging.info(f"DNS-запись успешно обновлена! Текущий IP {fact_ip}")
            sleep(ttl)  # в случае успеха дилей на время ttl
        else:
            logging.error(f"Ошибка: {response.status_code}")
            logging.error(response.json())
    else:
        logging.info("IP актуальный")

# Начинаем логировать + находим record_id для нашей DNS записи
setup_logging()
record_id = get_record_id(zone_id, dns_name)

# Бесконечный цикл с проверкой раз в минуту
previous_day = None
while True:
    current_day = datetime.now().strftime("%Y-%m-%d")
    if current_day != previous_day:  # Проверяем, наступил ли новый день
        setup_logging()
        previous_day = current_day

    update_dns_record()
    sleep(60)  # Ожидание 60 секунд