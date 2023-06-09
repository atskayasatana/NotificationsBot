import logging
import os
import requests
import telegram
import time

from dotenv import load_dotenv
from telegram.error import BadRequest, \
                           Unauthorized, \
                           InvalidToken, \
                           NetworkError, \
                           TelegramError


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger('dvmn_bot_logger')


if __name__ == '__main__':

    logger.setLevel(logging.DEBUG)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        filename='bot.log',
        filemode='w'
    )

    load_dotenv()

    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    devman_api_token = os.environ['DEVMAN_API_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

    try:
        bot = telegram.Bot(token=telegram_bot_token)
        url = 'https://dvmn.org/api/long_polling/'
        headers = {'Authorization': devman_api_token
                   }
        timestamp = ''

        logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))
        logger.info('Бот запущен')

        while True:

            payload = {"timestamp": timestamp}
            response = requests.get(url,
                                    headers=headers,
                                    params=payload,
                                    timeout=120)
            response.raise_for_status()

            review_results = response.json()

            if review_results['status'] == 'found':

                new_attempt = review_results['new_attempts'][0]
                lesson_title = new_attempt['lesson_title']
                lesson_returned = new_attempt['is_negative']
                lesson_url = new_attempt['lesson_url']

                if lesson_returned:
                    result_text = 'К сожалению, в работе нашлись ошибки.'
                else:
                    result_text = 'Преподавателю всё понравилось.' \
                                  'Можно приступать к следующему уроку.'

                text = f'Преподаватель проверил Вашу работу ' \
                       f'"{lesson_title}" ' \
                       f'\n {lesson_url} \n {result_text}'

                timestamp = review_results['last_attempt_timestamp']
                bot.send_message(text=text, chat_id=telegram_chat_id)

            else:
                if review_results['request_query']:
                    timestamp = review_results['request_query'][0][1]
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:
        logger.error('Не удается подключиться к серверу')
        time.sleep(15)
    except Unauthorized:
        logger.error('Неправильное значение токена')
    except BadRequest:
        logger.error('Бот не может обработать запрос')
    except InvalidToken:
        logger.error('Неверный токен бота')
    except NetworkError:
        logger.error('Проблемы с подключением')
    except TelegramError:
        logger.error('Бот упал (((')
