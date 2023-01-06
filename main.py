import logging
import os
import requests
import time
import tzlocal

from apscheduler.schedulers.background import BackgroundScheduler

PING_EVERY_MINUTES = os.getenv('PING_EVERY_MINUTES')
PING_URL = os.getenv('PING_URL')
PING_TIMEOUT = int(os.getenv('PING_TIMEOUT'))
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def notify(text: str) -> None:
    logging.info('Sending notify..')
    requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
        params={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': text,
        }
    )


def ping() -> None:
    global last_result
    try:
        requests.get(PING_URL, timeout=PING_TIMEOUT)
        text = 'Ping OK!'
        result = True
        logging.info(text)

    except Exception as e:
        text = str(e)
        result = False
        logging.error(text)

    if result != last_result:
        notify(text)

    last_result = result


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
        datefmt='%d.%m.%Y %H:%M:%S'
    )
    logging.getLogger('apscheduler').setLevel(logging.WARNING)

    last_result = True
    ping()

    scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
    scheduler.add_job(ping, 'cron', minute=f'*/{PING_EVERY_MINUTES}')
    scheduler.start()

    while True:
        time.sleep(1)
