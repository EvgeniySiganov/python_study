import os
import sqlite3
import re
import time
import argparse
import csv
import pandas as pd

from functools import reduce

# try:
#     import pandas as pd
# except ImportError:
#     print('Please, install pandas:\n'
#           ' pip install pandas')
#     raise

def give_value(text: str) -> int:
    """Возвращает количество воды, которое пытались налить или вылить из бочки. Если пытались налить, то положительное
    число, иначе - отрицательное.
    :param text: str, строка содержащая описание действия с бочкой;
    :return: int со знаком;
    """
    match = re.search(r"wanna\s+(.*?)\s+(\d*)l", text)
    if not match:
        return 0
    if match[1] == 'top up':
        return int(match[2])
    return -int(match[2])
def give_date(date: str) -> float:
    """Возвращает unix-время для переданной даты.
    :param date: str, дата в формате YYYY-mm-ddTHH:MM:SS или YYYY-mmddTHH:MM:SS.[0-9]{6}Z;
    :return: float, unix-время.
    """
    datetime = date.split('.')
    if len(datetime) > 1:
        date, ms = datetime
        ms = float(f"0.{ms[:-1]}")
    else:
        date, ms = datetime[0], 0
    clock = time.mktime(time.strptime(date, '%Y-%m-%dT%H:%M:%S'))
    clock += ms
    return clock
def give_data(filename: str) -> tuple or None:
    """Возвращает данные из файла лога.
    :param filename: str, путь до файла;
    :return: (VOLUME, barrel_volume, data), где:
        VOLUME - int, максимальный объем бочки;
        barrel_volume - int, объем воды в бочке;
        data - pandas dataframe('date', 'username', 'action', 'status').
    """
    with open(filename) as file:
        ok = file.readline()  # прочли первую строку
        if not ok:
            return None
        VOLUME = ok
        barrel_volume = int(file.readline().split()[0])
        data = pd.read_table(  # читаем файл как таблицу сразу
            file, sep='(?: - )|(?:\()',  # в качестве разделителй используем " - " или "("
            names = ['date', 'username', 'action', 'status'],  # имена столбцов
            engine = 'python',  # pandas запускает numpy, а numpy - библиотеки на чистом С, в которых разделитель sep
            # воспринимается как тип данных char - один символ, этот параметр указывает использует структуру Питона,
            # чтобы была возможность в sep указать регулярное выражение
        )
    data['date'] = data['date'].apply(give_date)  # применяет переданную функцию ко всем значениям столбца 'date'
    data['action'] = data['action'].apply(give_value)
    data['status'] = data['status'] == 'успех)'  # True, если успех, иначе False
    return VOLUME, barrel_volume, data
def give_args():
    parser = argparse.ArgumentParser()
    parser.usage = (
        f"db_sqlite3.py [path_to_log_file] [date1] [date2]\n"
        f"date1, date2 - date in YYYY-mm-ddTHH:MM:SS"
    )
    parser.add_argument('path_to_log', action='store', type=str, help='path_to_log_file')
    parser.add_argument('date1', action='store', type=str, help='lower bound of the date period')
    parser.add_argument('date2', action='store', type=str, help='upper bound of the date period')
    return parser.parse_args()

def execute_query(con, query):
    """Замыкание для запросов в БД.
    :param con: клиент подключения к БД
    :param query: str, исполняемый запрос
    :return: (result_count, sum_of_results), где
    result_count - количество строк в результате запроса,
    sum_of_results - сумма объемов в результате запроса.
    """
    result = con.execute(query)
    count = 0
    volume = 0
    for line in result:
        count += 1
        volume += abs(line[2])
    return count, volume
def write_result(filename):
    """Write result in csv-filename."""
    with open(filename, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(['Действие', 'Добавление воды', 'Забор воды'])
        writer.writerow(['Попытки', len_top_up, len_scoop])
        writer.writerow(['Процент ошибок', percent_top_up, percent_scoop])
        writer.writerow(['Удалось, л', top_up_volume, scoop_volume])
        writer.writerow(['Не удалось, л', fail_top_up_volume, fail_scoop_volume])
        writer.writerow([' ', 'Начало периода', 'Конец периода'])
        writer.writerow(['Объем воды, л', before_volume, after_volume])

if __name__ == '__main__':
    args = give_args()
    date1 = give_date(args.date1)
    date2 = give_date(args.date2)
    data = give_data(args.path_to_log)
    if not data:
        raise KeyboardInterrupt('Wrong data.')
    VOLUME, barrel_volume, dataframe = data
    database_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'barrel_database.db')
    with sqlite3.connect(database_filename) as con:
        # создаем подключение к БД sqlite3 (указываем просто имя файла, в котором и будет БД)
        dataframe.to_sql('barrel_data', con, index=False)
        # отправляем все данные нашей таблички pandas.DataFrame в БД

        len_top_up, all_top_up_volume = execute_query(con,f"""SELECT * FROM barrel_data WHERE date >= {date1} AND 
        date <= {date2} AND action > 0""")
        len_fail_top_up, fail_top_up_volume = execute_query(con,f"""SELECT * FROM barrel_data WHERE date >= {date1} 
        AND date <= {date2} AND action > 0 AND status == 0""")
        percent_top_up = len_fail_top_up/len_top_up*100 if len_top_up else 0
        len_scoop, all_scoop_volume = execute_query(con,f"""SELECT * FROM barrel_data WHERE date >= {date1} AND 
        date <= {date2} AND action < 0""")
        len_fail_scoop, fail_scoop_volume = execute_query(con,f"""SELECT * FROM barrel_data WHERE date >= {date1} 
        AND date <= {date2} AND action < 0 AND status == 0""")
        percent_scoop = len_fail_scoop/len_scoop*100 if len_scoop else 0
        before = con.execute(f"""SELECT * FROM barrel_data WHERE date < {date1} AND status == 1""")
        before_volume = 0
        for line in before:
            before_volume += line[2]
        if len_top_up + len_scoop:
            before_volume += barrel_volume
        top_up_volume = all_top_up_volume - fail_top_up_volume
        scoop_volume = all_scoop_volume - fail_scoop_volume
        after_volume = before_volume + top_up_volume - scoop_volume
        input("Посмотри, какой файл сформировался для БД sqlite3 и нажми любую клавишу.")
    os.remove(database_filename)
    print(f"Какой объем воды был в бочке в начале указанного периода?\n"
        f"{before_volume}\n"
        f"Какой в конце указанного периода?\n"
        f"{after_volume}\n"
        f"Какое количество попыток налить воду в бочку было за "
        f"указанный период?\n"
        f"{len_top_up}\n"
        f"Какой процент ошибок был допущен за указанный период?\n"
        f"{percent_top_up}\n"
        f"Какой объем воды был налит в бочку за указанный период?\n"
        f"{top_up_volume}l\n"
        f"Какой объем воды был не налит в бочку за указанный период?\n"
        f"{fail_top_up_volume}l\n"
        f"Какое количество попыток забора воды из бочки было за "
        f"указанный период?\n"
        f"{len_scoop}\n"
        f"Какой процент ошибок был допущен за указанный период?\n"
        f"{percent_scoop}\n"
        f"Какой объем воды был забран из бочки за указанный период?\n"
        f"{scoop_volume}l\n"
        f"Какой объем воды был не забран из бочки за указанный период?\n"
        f"{fail_scoop_volume}l\n"
    )
    result_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'answer.csv')
    write_result(result_file)