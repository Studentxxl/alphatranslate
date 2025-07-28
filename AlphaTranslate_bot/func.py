from datetime import datetime
from os import path


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
    if path.exists(file_path + filename) == False:
        open(file=file_path + filename, mode='a', encoding='utf-8').close()
    # пишет текст из переданного параметра
    with open(file=file_path + filename, mode='a', encoding='utf-8') as file:
        file.write(text)