import telebot
import func
from time import sleep
import requests
import SECRET
import CONFIG


bot = telebot.TeleBot(SECRET.TOKEN)


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
    date = func.date_time_now()
    try:
        # Если прошла проверка на запрещенные символы
        if func.check_symbols(obj=message.text, forbidden_symbols=CONFIG.stop_symbols):
            # запрос на сервер
            res = requests.get(f'{CONFIG.server_url}/translate/?user_query={message.text}')

            # Если есть ответ на запрос
            if res:

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
                    func.log(file_path=CONFIG.patch_to_log, text=info_message)
                    print(info_message)
                    # отправка ответа в чат
                    bot.send_message(chat_id=message.chat.id, text=res.text)

            #  Если нет ответа от сервера,
            else:
                # отправка сообщения об ошибке
                msg = 'Ошибка сервера. Нет ответа. Попробуй позже'
                bot.send_message(chat_id=message.chat.id, text=msg)

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