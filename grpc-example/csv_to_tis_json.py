import csv
import json

FILEPATH = './tis-data.csv'

data_arr = []

with open(FILEPATH, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        data_arr.append(row[0].split(','))

tis_input_data = {
    "inputs": [
        {
            "name": "IN0",
            "shape": [len(data_arr),len(data_arr[0])],
            "datatype": "BYTES",
            "data": data_arr
        }
    ],
    "outputs": [
        {
            "name":"OUT0"
        }
    ]
}

with open('tis-data.json', 'w') as f:
    json.dump(tis_input_data, f)

print('Conversion successful')