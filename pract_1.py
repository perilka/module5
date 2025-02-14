import json, csv


# Задание 1

with open('students.json', 'r') as file:
    students_data = json.load(file)

def number_counter(data: list) -> str:
    return f'Общее количество студентов: {len(data)}'
print(number_counter(students_data))

def oldest_student(data: list) -> str:
    ages = [info['возраст'] for info in data]
    i = ages.index(max(ages))
    return (f'Студент с самым высоким возрастом: '
            f'имя - {data[i]['имя']}, '
            f'возраст - {data[i]['возраст']}, '
            f'город - {data[i]['город']}.')
print(oldest_student(students_data))

def subject_counter(data: list, subject: str) -> str:
    num = 0
    for student in data:
        if subject in student['предметы']:
            num += 1
    return f'Количество студентов, изучающих {subject}: {num}'
print(subject_counter(students_data, 'Python'))


# Задание 2

with open('sales.csv', 'r') as file:
    reader = csv.reader(file)
    sales_data = list(reader)

def total_sales_counter(data: list) -> str:
    summ = 0
    for i in range(1, len(data)):
        summ += float(data[i][2])
    return f'Общая сумма продаж за весь период: {summ} рублей'
print(total_sales_counter(sales_data))

def top_product(data: list) -> str:
    products = []
    sales_dict = {}
    for i in range(1, len(data)):
        if data[i][1] not in products:
            products.append(data[i][1])
            sales_dict[data[i][1]] = float(data[i][2])
        else:
            sales_dict[data[i][1]] += float(data[i][2])
    return f'Продукт с самым высоким объемом продаж: {max(sales_dict, key=sales_dict.get).strip()}'
print(top_product(sales_data))

def monthly_sales(data: list) -> dict:
    months = []
    sales_dict = {}
    for i in range(1, len(data)):
        if data[i][0][5:7] not in months:
            months.append(data[i][0][5:7])
            sales_dict[data[i][0][5:7]] = float(data[i][2])
        else:
            sales_dict[data[i][0][5:7]] += float(data[i][2])
    return sales_dict
print(monthly_sales(sales_data))


# Задание 3

with open('employees.json', 'r') as file:
    employees_data = json.load(file)

with open('performance.csv', 'r') as file:
    reader = csv.reader(file)
    performance_data = list(reader)

def info_comparison(employees: list, performance: list) -> dict:
    info = {}
    for employee in employees:
        for i in range(1, len(performance)):
            if int(performance[i][0]) == int(employee['id']):
                info[employee['имя']] = int(performance[i][1])
    return info
print(info_comparison(employees_data, performance_data))

def average_performance(performance: list) -> int|float:
    performance_list = []
    for i in range(1, len(performance)):
        performance_list.append(int(performance[i][1]))
    return sum(performance_list)/len(performance_list)
print(average_performance(performance_data))

def max_performance(employees: list, performance: list):
    dct = info_comparison(employees_data, performance_data)
    return f'Имя сотрудника: {max(dct, key=dct.get)}, производительность: {dct[max(dct, key=dct.get)]}'
print(max_performance(employees_data, performance_data))