# Serving SnapML models with Triton Inference Server on Linux on IBM zSystems.
Example materials to demonstrate serving SnapML models with Triton Inference Server on Linux on IBM zSystems.

## Getting started.

Install [Anaconda](https://docs.anaconda.com/anaconda/install/linux-s390x/) for Linux on zSystems.

On Ubuntu systems:
```
apt install default-jdk libssl-dev
```

After installing these packages, follow the steps below:
```
conda install git
git clone https://github.com/IBM/ai-on-z-triton-is-examples.git
cd ai-on-z-triton-is-examples/snapml-examples/
conda env create -f ./environment.yml
conda activate snapenvz
```
## Example 1.  Deploying Random Forest classifier model using triton inference server.

In this examples, Random Forest classifier model trained with scikit-learn will be deployed 
on triton inference server using snapml scoring pipeline and triton python backend.  
`Note:` Here, model repository is `ai-on-z-triton-is-examples/tree/main/snapml-examples/models/rfc_model_py`

### A. Train a Random Forest Classifier model (scikit-learn) using the scikit-learn breast cancer dataset.

We first train a Random Forest Classifier model using the breast cancer sklearn dataset. We save the model as a PMML pipeline.
```
python train.py
```
This generates a PMML pipeline for the model and saves it as `model.pmml`; later, `model.pmml` should be copied to the specific repository `models/rfc_model_py/1/`.
```
cp model.pmml models/rfc_model_py/1/
```
Finally model repository should look like below - 
```
models
└── rfc_model_py
    ├── 1
    │   ├── model.pmml
    │   └── model.py
    └── config.pbtxt
```

### B. Start triton server with model repository.

```
docker run --shm-size=1g --ulimit memlock=-1  --ulimit stack=67108864 --rm -p8000:8000 -p8001:8001 -p8002:8002 -v//<path>/models:/models <imageid> tritonserver --model-repository=/models
```

### C. Test the random forest model deployed in triton server.

```
python test_service.py --model rfc_model_py
```
