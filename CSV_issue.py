import csv


# Задание 1

with open('prices.txt', 'r', encoding='utf8') as f:
    data = []
    for line in f:
        row = [obj for obj in line.rstrip().split('\t')]
        data.append(row)

print(data)

with open('prices.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)


# Задание 2

with open('prices.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    lst = list(reader)

print(lst)

def price_counter(shopping_list):
    prices = 0
    for i in shopping_list:
        price = int(i[1])*int(i[2])
        prices += price
    return prices


print(price_counter(lst))