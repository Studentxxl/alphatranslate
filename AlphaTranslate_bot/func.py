from datetime import datetime
from os import path


def check_symbols(obj: str, forbidden_symbols: list):
    for i in obj:
        if i in forbidden_symbols:
            return False
    return True


def date_time_now():
    #
    return datetime.now().strftime("%Y-%m-%d--%H:%M")


def log(file_path, text):
    filename = datetime.now().strftime("%Y-%m-%d" + ".txt")
    if path.exists(file_path + filename) == False:
        open(file=file_path + filename, mode='a', encoding='utf-8').close()

    with open(file=file_path + filename, mode='a', encoding='utf-8') as file:
        file.write(text)