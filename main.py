import argparse
import os
import requests
import telegram

from dotenv import load_dotenv

CHAT_ID = 874442731


if __name__ == '__main__':

    load_dotenv()

    TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
    DEVMAN_API_TOKEN = os.environ['DEVMAN_API_TOKEN']

    parser = argparse.ArgumentParser()
    parser.add_argument('chat_id',
                        help='id чата в Телеграмме, '
                             'куда будут отправляться сообщения о проверке')
    args = parser.parse_args()
    chat_id = args.chat_id

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    url = 'https://dvmn.org/api/long_polling/'

    headers = {'Authorization': DEVMAN_API_TOKEN
               }

    timestamp = 0

    while True:
        try:
            if timestamp:
                payload = {"timestamp": timestamp}
                response = requests.get(url, headers=headers, params=payload)
                response.raise_for_status()
                timestamp = response.json()['last_attempt_timestamp']

            else:
                response = requests.get(url, headers=headers, timeout=25)
                response.raise_for_status()
                timestamp = response.json()['new_attempts'][0]['timestamp']

            if response.json()['status'] == 'found':
                lesson_title = \
                    response.json()['new_attempts'][0]['lesson_title']
                lesson_returned = \
                    response.json()['new_attempts'][0]['is_negative']
                lesson_url = \
                    response.json()['new_attempts'][0]['lesson_url']

                if lesson_returned:
                    result_text = 'К сожалению, в работе нашлись ошибки.'
                else:
                    result_text = \
                        'Преподавателю всё понравилось. ' \
                        'Можно приступать к следующему уроку.'

                text = f'Преподаватель проверил Вашу работу ' \
                       f'"{lesson_title}" ' \
                       f'\n {lesson_url} \n {result_text}'

                timestamp = response.json()['last_attempt_timestamp']

            bot.send_message(text=text, chat_id=CHAT_ID)

        except requests.exceptions.ReadTimeout:
            print('Сервер не отвечает')
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения')
