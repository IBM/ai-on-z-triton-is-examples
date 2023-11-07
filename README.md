# Triton Inference Server using Python Backend with SnapML & Preprocessing
This repository demonstrates how to build triton inference server with the python backend using SnapML for model inferencing in additional to including data preprocessing code.

## Step 1 - Build Triton Inference Server
Run docker command from terminal
```
docker build .
```

## Step 2 - Start Triton Inference Server
Run docker command from terminal
```
docker run --shm-size 1G -u root --rm -p<Expose_HTTP_PORT_NUM>:8000 -v <your volume mount>:/models <triton docker image id> tritonserver --model-repository=/models
```

For example:
```
docker run --shm-size 1G -u root --rm -p8000:8000 -v//$PWD/snapml-py-preprocess-pipeline/models:/models 3d1f7c309502 tritonserver --model-repository=/models
```

## Step 3 - Model Inferencing using Triton Inference Server
Run sample python code from terminal
- Positive inference example
    ```
    cd snapml-py-preprocess-pipeline/
    python test_service_pos.py
    ```
- Negative inference example
    ```
    cd snapml-py-preprocess-pipeline/
    python test_service_neg.py
    ```