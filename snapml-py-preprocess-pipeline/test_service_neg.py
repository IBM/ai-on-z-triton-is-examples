import requests
import time
import argparse
import json

CLI = argparse.ArgumentParser()
CLI.add_argument("--model", type=str, default="xgboost_model")
args = CLI.parse_args()

file1 = open('input_batch_neg.json', 'r')
input_batch_neg = json.loads(file1.readlines()[0].replace(" ", ""))
#print(input_batch_pos)
jason_data = input_batch_neg
inference_endpoint = "http://localhost:8000/v2/models/xgboost_model/infer"


response = requests.post(inference_endpoint, json=jason_data)
print(response.text)
