import telebot
import TOKEN
from datetime import datetime
from time import sleep
import requests
from os import path


bot = telebot.TeleBot(TOKEN.token)


# ****************************
# COMMANDS
# ****************************

"""
pip freeze > requirements.txt
pip install -r requirements.txt
"""

# ****************************
# CONFIG
# ****************************

stop_symbols: list = ['=', '+', '/', '*', '{', '}', '[', ']', '(', ')']
server_url: str = 'http://91.205.164.229:8090'
patch_to_log: str = "./log/"


# ****************************
# FUNC
# ****************************

def check_symbols(obj: str, forbidden_symbols: list[str]):
    """
    Проверяет строку на наличие запрещенных символов
    :param obj: строка
    :param forbidden_symbols: список строк с запрещенными символами
    :return: False | True
    """
    for i in obj:
        if i in forbidden_symbols:
            return False
    return True


def date_time_now() -> str:
    """
    :return: Форматированная строка дата, время
    [гггг-мм-дд--чч-мм]
    """
    return datetime.now().strftime("%Y-%m-%d--%H:%M")


def log(file_path: str, text: str) -> None:
    """
    Пишет логи в файл txt
    :param file_path: путь к папке логов
    :param text: текст, который будет записан
    :return: None
    """
    # имя файла [гггг-мм-дд.txt]
    filename = datetime.now().strftime("%Y-%m-%d" + ".txt")
    # создает файл с текущей датой, если его не существует
    if not path.exists(file_path + filename):
        open(file=file_path + filename, mode='a', encoding='utf-8').close()
    # пишет текст из переданного параметра
    with open(file=file_path + filename, mode='a', encoding='utf-8') as file:
        file.write(text)


# ****************************
# APP
# ****************************

# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    # сообщение пользователю, отправившему команду /start
    msg = (f'Приветствую, !\n'
           f'Я бот-переводчик.\n'
           f'Отправь мне /help чтобы узнать, как пользоваться командами.')
    # отправка msg
    bot.send_message(chat_id=message.chat.id, text=msg)


# обработчик команды /help

# обработчик текста
@bot.message_handler(content_types=['text'])
def text_message(message):
    # текущая дата [гггг-мм-дд--чч-мм]
    date = date_time_now()
    try:
        # Если прошла проверка на запрещенные символы
        if check_symbols(obj=message.text, forbidden_symbols=stop_symbols):
            # запрос на сервер
            res = requests.get(f'{server_url}/translate/?user_query={message.text}')

            # Если сервер вернул ошибку,
            if res.text == '"error905"':
                err_text = ('Перед английским текстом должен быть знак ! \n'
                            'Перед русским ?\n\n'
                            'пример:\n'
                            '!Hello\n'
                            '?Привет')
                # то в чат отправляется инструкция по выполнению запросов
                bot.send_message(chat_id=message.chat.id, text=err_text)

            # Если сервер вернул переведенный текст,
            else:
                info_message = (f'***\n'
                                f'{date} url: {res.url}\n'
                                f'response: {res.text}\n\n')
                # запись события в лог
                log(file_path=patch_to_log, text=info_message)
                print(info_message)
                # отправка ответа в чат
                bot.send_message(chat_id=message.chat.id, text=res.text)

        # Если не прошла проверка на запрещенные символы
        else:
            info_message = ('***\n'
                            'В тексте не должно быть символов:\n'
                            '=+/*{}[]()')
            bot.send_message(chat_id=message.chat.id, text=info_message)

    # Если возникло исключение в блоке try
    except Exception as e:
        print(f'{date} Исключение внутри функции [text_message]\n'
              f'error: {e}')
        bot.send_message(chat_id=message.chat.id, text="except")


# ****************************
# START
# ****************************

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f'Исключение внутри блока [START]\n'
                  f'error: {e}')
            sleep(8)