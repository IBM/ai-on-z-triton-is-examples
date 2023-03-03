# Copyright contributors to the ai-on-z-triton-is-examples project.

import requests
import numpy as np
import time
import argparse
from sklearn import datasets

# Note: This example borrows from https://github.com/IBM/snapml-examples

CLI = argparse.ArgumentParser()
CLI.add_argument("--model", type=str, default="rfc_model_py")
args = CLI.parse_args()
# X, y = datasets.load_breast_cancer(return_X_y=True)
jason_data = {
  "inputs" : [
    {
      "name" : "IN0",
      "shape" : [ 1,30 ],
      "datatype" : "FP32",
      "data" : [[1.308e+01, 1.571e+01, 8.563e+01, 5.200e+02, 1.075e-01, 1.270e-01,
       4.568e-02, 3.110e-02, 1.967e-01, 6.811e-02, 1.852e-01, 7.477e-01,
       1.383e+00, 1.467e+01, 4.097e-03, 1.898e-02, 1.698e-02, 6.490e-03,
       1.678e-02, 2.425e-03, 1.450e+01, 2.049e+01, 9.609e+01, 6.305e+02,
       1.312e-01, 2.776e-01, 1.890e-01, 7.283e-02, 3.184e-01, 8.183e-02]]
    }
  ],
  "outputs" : [
    {
      "name" : "OUT0"
    }
  ]
}
inference_endpoint = "http://0.0.0.0:8000/v2/models/"+args.model+"/infer"
response = requests.post(inference_endpoint, json=jason_data)
print(response.text)

