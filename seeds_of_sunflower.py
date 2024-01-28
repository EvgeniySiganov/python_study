import json


# calculation of factorial
def factorial(n):
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f


# choosing the correct name of the calculated object
def choose_plural(digit, three_varieties):
    s = str(digit)
    if int(s[-1:]) == 0 or int(s[-1:]) >= 5:
        choose = three_varieties[2]
    elif len(s) > 1 and 11 <= int(s[-2:]) <= 14:
        choose = three_varieties[2]
    elif 2 <= int(s[-1:]) <= 4:
        choose = three_varieties[1]
    else:
        choose = three_varieties[0]
    return s + " " + choose


# encrypt message "s" by offset "k"
def encrypt(s, k):
    letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    result = ""
    for i in s.upper():
        index = letters.find(i)
        if index != -1:
            result += letters[(index + k) % len(letters)]
        else:
            result += i
    return result


def sum_of_two_digits():
    try:
        a = int(input("Введите первое число: "))
        b = int(input("Введите второе число: "))
        print("Сумма равна: " + str((a + b)))
    except ValueError:
        print('Вы ввели не число')


# enter three products and their counts. It will be written to catalog.json
def online_shopping():
    catalog = {}

    with open('catalog.json', 'a+') as f:
        f.seek(0)
        s = f.read()
        if len(s) > 0:
            catalog = json.loads(s)

    for i in range(3):
        n = input("Введите наименование товара: ")
        c = int(input("Введите количество: "))
        if catalog.__contains__(n):
            catalog[n] = catalog[n] + c
        else:
            catalog[n] = c

    with open('catalog.json', 'w') as f:
        f.write(json.dumps(catalog))


def sort_words_without_letter_case():
    words = input('Enter words:\n')
    arr = words.split()
    arr.sort(key=lambda x: x.lower())
    print(" ".join(arr))