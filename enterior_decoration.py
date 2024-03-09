import cmath


name = 'Evgenii'


def helloer(name):
    print('Hello, ' + name)


def enter_numbers():
    s = input('Enter numbers: \n')
    while s.isdigit():
        yield int(s)
        s = input()


def get_result_entering_numbers():
    l = list(enter_numbers())
    print(f'numbers {l}\n'
          f'count of any numbers = {len(l)}\n'
          f'sum of numbers = {sum(l)}\n'
          f'min of numbers = {min(l)}\n'
          f'max of numbers = {max(l)}\n'
          f'medium of numbers = {sum(l)/2}\n')


def quadratic_equation(a, b, c):
    delta = cmath.sqrt(b**2 - 4*a*c)
    print(f"quadratic equation: {a}x**2 + {b}x + {c}\n")
    print(f"delta: {delta}\n")
    solution1 = (-b + delta) / (2 * a)
    solution2 = (-b - delta) / (2 * a)
    print(f"solution 1: {solution1}\n")
    print(f"solution 2: {solution2}\n")
    print(f"equals? : {solution1 == solution2}\n")


def enter_three_num():
    l = ('a', 'b', 'c')
    for i in l:
        n = input(f"{i} = ")
        yield int(n)


if __name__ == '__main__':
    #helloer(name)
    #get_result_entering_numbers()
    quadratic_equation(*enter_three_num())


