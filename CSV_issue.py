import csv


with open('prices.txt', 'r', encoding='utf8') as f:
    data = []
    for line in f:
        row = [obj for obj in line.rstrip().split('\t')]
        data.append(row)

print(data)

with open('prices.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)
