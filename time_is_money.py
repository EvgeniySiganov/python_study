import datetime
import tkinter
import sys

import seeds_of_sunflower as sos


def show_time():
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=400, height=400, bg='white')
    canvas.pack()
    text_object = canvas.create_text(200, 200, text='00:00:00', fill='orange')

    while True:
        my_datetime = datetime.datetime.now()
        datetime_str = my_datetime.strftime('%H:%M:%S')
        canvas.itemconfig(text_object, text=datetime_str)
        canvas.update()


def time_to_date_x():
    text = 'До часа "Икс" '
    text_and = ' и '
    days_plural = ['день', 'дня', 'дней']
    hours_plural = ['час', 'часа', 'часов']
    minutes_plural = ['минута', 'минуты', 'минут']

    now = datetime.datetime.now()
    now_trim = now.replace(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute,
                           second=now.second)

    datetime_str = input('Введите дату/время в формате ДД.ММ.ГГГГ ЧЧ:ММ\n')
    date_x = None
    try:
        date_x = datetime.datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')
    except ValueError:
        print('Ошибка')
        sys.exit()

    difference = date_x - now_trim + datetime.timedelta(minutes=1)
    days = difference.days
    hours = difference.seconds // (60 * 60)
    minutes = (difference.seconds - (hours * 60 * 60)) // 60

    if difference.total_seconds() < 0:
        print('Ошибка')
    elif days > 0:
        text += sos.choose_plural(days, days_plural)
        if hours > 0:
            text += text_and + sos.choose_plural(hours, hours_plural)
        print(text)
    elif hours > 0:
        text += sos.choose_plural(hours, hours_plural)
        if minutes > 0:
            text += text_and + sos.choose_plural(minutes, minutes_plural)
        print(text)
    else:
        text += sos.choose_plural(minutes, minutes_plural)
        print(text)
