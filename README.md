# Generating pb file for ghz workload generator against Triton Inference Server
This repository demonstrates how to generate a .pb file to use with ghz workload generate to run inferencing with Triton Inference Server using the gRPC protocol.

## Execute the Python script to convert the input data JSON to bytes data:
Usage of `json-to-triton-request-data.py`:
```
python3 json-to-triton-request-data.py -h
usage: json-to-triton-request-data.py [-h] [-m MODEL_NAME] [-v MODEL_VERSION] [-i INPUT] [-d INP_DATATYPE] [-o OUTPUT]
options:
  -h, --help            show this help message and exit
  -m MODEL_NAME, --model_name MODEL_NAME
                        Deployed model name.
  -v MODEL_VERSION, --model_version MODEL_VERSION
                        Deployed model version.
  -i INPUT, --input INPUT
                        Path to input data in json format.
  -d INP_DATATYPE, --inp_datatype INP_DATATYPE
                        Input datatype
  -o OUTPUT, --output OUTPUT
                        Path to output data file to be saved.
```

Sample example to generate bytes data using `model_equals_b_bytes` and `input_b_bytes.json`:

Run command in `grpc-example` dir:
```
python3 json-to-triton-request-data.py -m model_equals_b_bytes -i input_b_bytes.json -d bytes -o triton-request.pb
```