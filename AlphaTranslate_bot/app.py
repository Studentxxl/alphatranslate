import telebot
import func
from datetime import datetime
from time import sleep
from os import path
import requests

TOKEN: str = '7848309765:AAE5tvF-OzZqfVxTcW3Zbk6whDkpQXFDZss'
bot = telebot.TeleBot(TOKEN)


bot_admin_list = [6753632098]
admin_id = 6753632098
developer_id = 6591039077

stop_symbols = ['=', '+', '/', '*', '{', '}', '[', ']', '(', ')']

def date_time_now():
    #
    return datetime.now().strftime("%Y-%m-%d--%H:%M")


def log(file_path, text):
    filename = datetime.now().strftime("%Y-%m-%d" + ".txt")
    if path.exists(file_path + filename) == False:
        open(file=file_path + filename, mode='a', encoding='utf-8').close()

    with open(file=file_path + filename, mode='a', encoding='utf-8') as file:
        file.write(text)


# * Пути
patch_to_log = "./log/"


@bot.message_handler(content_types=['text'])
def text_message(message):
    if func.check_symbols(obj=message.text, forbidden_symbols=stop_symbols):
        res = requests.get(f'http://91.205.164.229:8090/translate/?user_query={message.text}')
        date = date_time_now()
        info_message = (f'***\n'
                        f'{date} url: {res.url}\n'
                        f'response: {res.text}\n\n')
        log(file_path=patch_to_log, text=info_message)
        print(info_message)
        bot.send_message(message.chat.id, res.text)
    else:
        info_message = ('***\n'
                        'В тексте не должно быть символов:\n'
                        '=+/*{}[]()')
        bot.send_message(chat_id=message.chat.id, text=info_message)



if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            sleep(8)

