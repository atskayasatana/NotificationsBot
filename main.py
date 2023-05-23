import argparse
import os
import requests
import telegram
import time

from dotenv import load_dotenv


if __name__ == '__main__':

    load_dotenv()

    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    devman_api_token = os.environ['DEVMAN_API_TOKEN']

    parser = argparse.ArgumentParser()
    parser.add_argument('chat_id',
                        help='id чата в Телеграмме, '
                             'куда будут отправляться сообщения о проверке')
    args = parser.parse_args()
    chat_id = args.chat_id

    bot = telegram.Bot(token=telegram_bot_token)

    url = 'https://dvmn.org/api/long_polling/'

    headers = {'Authorization': devman_api_token
               }

    timestamp = ''

    while True:
        try:
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
                    result_text = \
                        'Преподавателю всё понравилось. ' \
                        'Можно приступать к следующему уроку.'

                text = f'Преподаватель проверил Вашу работу ' \
                       f'"{lesson_title}" ' \
                       f'\n {lesson_url} \n {result_text}'

                timestamp = review_results['last_attempt_timestamp']
                bot.send_message(text=text, chat_id=chat_id)

            else:
                if review_results['request_query']:
                    timestamp = review_results['request_query'][0][1]

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения')
            time.sleep(60)
