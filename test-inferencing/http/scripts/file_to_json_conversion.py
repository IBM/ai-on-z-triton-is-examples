import json

file1 = open("<INPUT_DATA_FILE>", 'r')
j = file1.readlines()
j = ''.join(j)
j = j.replace(" ", "").replace("\n","")
input_batch = json.loads(j)


