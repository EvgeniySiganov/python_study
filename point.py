import math

class Point:
    """Реализует точку на плоскости."""
    count=0 # статический атрибут, атрибут класса
    def __init__(self, x, y):
        self.x = x
        self.y = y
    # инициализировали атрибуты объекта

    def distance_from_origin(self):
        """Возвращает расстояние до центра."""
        return math.hypot(self.x, self.y)


    def __eq__(self, other):
        """Возвращает результат сравнения двух объектов.
        :param self: Point, первый объект
        :param other: Point, второй объект
        :return: bool
        """
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """Реализует возвращаемое значение для функции repr()."""
        return f"Point({self.x!r}, {repr(self.y)})"
        # !r - спецификатор формата метода format() - использует repr()
        # для используемых строк, то есть берет их, как есть:
        # аналогичные строки на выходе

    def __str__(self):
        """Реализует возвращаемую строку для str() - человекочитаемую."""
        return "({0.x!r}, {0.y!r})".format(self)

    def __add__(self, other):
        x = self.__x + other.x
        y = self.__y + other.y
        return Point(x, y)

    def __iadd__(self, other):
        self.__x += other.x
        self.__y += other.y
        return self

    def __sub__(self, other):
        x = self.__x - other.x
        y = self.__y - other.y
        return Point(x, y)

    def __isub__(self, other):
        self.__x -= other.x
        self.__y -= other.y
        return self

    def __mul__(self, mul):
        x = self.__x * mul
        y = self.__y * mul
        return Point(x, y)

    def __imul__(self, mul):
        self.__x *= mul
        self.__y *= mul
        return self

    def __truediv__(self, div):
        x = self.__x / div
        y = self.__y / div
        return Point(x, y)

    def __itruediv__(self, div):
        self.__x /= div
        self.__y /= div
        return self

    def __floordiv__(self, div):
        x = self.__x // div
        y = self.__y // div
        return Point(x, y)

    def __ifloordiv__(self, div):
        self.__x //= div
        self.__y //= div
        return self

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @y.deleter # удалить через del p.y
    def y(self):
        del self.__y

n = 2
p = Point(4, 5)
print(p.x) # 4
p.y = 10
print(p.y) # 10
print(p.__dict__) # {'_Point__x': 4, '_Point__y': 10}

q = Point(10, 1)
r = Point(2, 2)

p = q + r
print(p.__dict__)

p += q
print(p.__dict__)

p = q - r
print(p.__dict__)

p -= q
print(p.__dict__)

p = q * n
print(p.__dict__)

p *= n
print(p.__dict__)

p = q / n
print(p.__dict__)

p /= n
print(p.__dict__)

p = q // n
print(p.__dict__)

p //= n
print(p.__dict__)



