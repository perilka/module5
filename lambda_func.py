# Задание 1
from tkinter.font import names

from pract_1 import average_performance

strings = ["apple", "kiwi", "banana", "fig"]
print(list(filter(lambda x: len(x) > 4, strings)))

# Задание 2
students = [{"name": "John", "grade": 90}, {"name": "Jane", "grade": 85}, {"name": "Dave", "grade": 92}]
print(max(students, key=lambda student: student['grade']))

# Задание 3
tuples = [(1, 5), (3, 2), (2, 8), (4, 3)]
print(sorted(tuples, key=lambda x: x[0] + x[1]))

# Задание 4
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(list(filter(lambda x: x % 2 == 0, numbers)))

# Задание 5
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age})"

persons = [Person('Pupa', 20), Person('Lupa', 88), Person('Dupa', 15)]
print(sorted(persons, key=lambda x: x.age))