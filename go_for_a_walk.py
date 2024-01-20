import requests
import yaml
import time


def parsing_of_page():
    result = requests.get('https://letpy.com/simple-html-example/')
    s = result.text
    #print(s)
    parse_start = 'Случайное число: <strong>'
    parse_end = '</strong>'
    n = s.find(parse_start)
    s = s[n + len(parse_start):]
    n = s.find(parse_end)
    s = s[:n]

    print(s)


def telegram_bot():
    with open('credentials.yaml', 'r') as file:
        data = yaml.safe_load(file)
    credentials = data.get('telegram')

    last_upd_id = 0
    while True:
        result = requests.get('https://api.telegram.org/bot' + credentials + '/getUpdates',
                              params={'offset': last_upd_id + 1})
        data = result.json()
        for update in data['result']:
            print(update['message']['text'])
            last_upd_id = update['update_id']
            chat_id = update['message']['chat']['id']

            send_result = requests.get('https://api.telegram.org/bot' + credentials + '/sendMessage',
                                       params={'chat_id': chat_id, 'text': 'hi '
                                                                           + update['message']['chat']['first_name']})
        time.sleep(1)
