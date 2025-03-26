import json
import csv
from functools import reduce

with open('student_list.json', 'r') as file:
    students = json.load(file)

print(students)



# Задание 1
def get_average_score(data: dict[str, dict]) -> dict[str, float|int]:
    avs = {}
    for k, v in data.items():
        grades = v['grades'].values()
        sum_ = sum(grades)
        average = sum_/len(grades)
        avs[k] = average
    return avs

for key, value in get_average_score(students).items():
    print(f'Средний балл для студента {key}: {value}')
print() # визуальный разделитель, не более....



# Задание 2
def get_best_student(data: dict[str, dict]) -> str:
    avs = get_average_score(data)
    best = (sorted(avs.items(), key=lambda x: x[1]))[-1]
    return f'Наилучший студент: {best[0]} (Средний балл: {best[1]})'

print(get_best_student(students))
print()


def get_worst_student(data: dict[str, dict]) -> str:
    avs = get_average_score(data)
    best = (sorted(avs.items(), key=lambda x: x[1]))[0]
    return f'Худший студент: {best[0]} (Средний балл: {best[1]})'

print(get_worst_student(students))
print()



# Задание 3
def find_student(name: str, data: dict[str, dict]):
    result = data.get(name, 'Студент с таким именем не найден')
    if isinstance(result, dict):
        print('name:', name)
        for k, v in result.items():
            print(f'{k}: {v}')
    else:
        print(result)

find_student('John', students)
print()
find_student('Niels', students)
print()



# Задание 4
sorted_average_scores = sorted(get_average_score(students).items(), key=lambda x: x[1], reverse=True)

print('Сортировка студентов по среднему баллу:')
for info in sorted_average_scores:
    print(f'{info[0]}: {info[1]}')
print()



# Задание 5:
result = []
for name in list(students.keys()):
    dct = {}
    dct['name'] = name
    dct.update(students[name])
    result.append(dct)

print(result)
print()



# Задание 6
almost_csv = []
for name in list(students.keys()):
    dct = {}
    dct['name'] = name
    dct['age'] = students[name]['age']
    dct['grade'] = get_average_score(students)[name]
    almost_csv.append(dct)

with open('students_info.csv', 'w') as csvfile:
    fieldnames = ['name', 'age', 'grade']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(almost_csv)