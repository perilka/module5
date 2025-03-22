import csv
import json
from pprint import pprint

with open('данные.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    python_obj = []
    json_data = []
    for row in reader:
        python_obj.append(row)
        json_data.append(json.dumps(row))

pprint(python_obj, indent=4)
print()
pprint(json_data, indent=4)