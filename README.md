# Demonstrating inference pipeline creation using triton inference server on IBM zSystems and LinuxONE. 

## 1. Scope

The purpose of this project is to provide to sample artifacts to create inference pipeline using triton inference server on IBM zSystems and LinuxONE. 

All the materials are provided as examples. Provided dockerfiles build open-source based (not proprietary) images. 

The maintainers of this repository do not assert to be experts in containers or container security.
Resources include:
  - [Docker engine security](https://docs.docker.com/engine/security/)
  - [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
  - [Docker getting started resources](https://docs.docker.com/get-started/resources/)

## 2. Usage
These build files commonly rely on base images from the [IBM Z and LinuxONE Container Image Registry (ICR) ](https://ibm.github.io/ibm-z-oss-hub/main/main.html).
This will require free basic authentication. Details can be found at the ICR link above. 

### Steps to build and run docker image. 
- Run docker build using the provided dockerfile i.e `docker build -f ./Dockerfile .`. Using a Ubuntu base image, this will create an environment with both specific Triton Server, Python Backend release with SnapML version.

- Create and run a docker container using the image created on the prior step. As part of this step, you should map the required triton server ports to a port on your local system. An example follows: `docker run --shm-size=1g --ulimit memlock=-1  --ulimit stack=67108864 --rm -p8000:8000 -p8001:8001 -p8002:8002 -v//<path>/models:/models <imageid> tritonserver --model-repository=/models`. This states the image in interactive mode, tells docker to delete the container upon exit, and publishes container HTTP service port at 8000, GRPC Inference Service at 8001, Metrics Service at 8002.

    `Note:` Please do refer each topic(e.g `snapml-examples` ) inside `ai-on-z-triton-is-examples` to create model reposity for the specific use cases. 
 
## 3. Content

| Folder(topic) | Description   |
| ------------- | ------------- |
| snapml-examples     | Serving SnapML models with Triton Inference Server on Linux on IBM zSystems |

`Note:` We also support [onnxmlir-triton-backend](https://github.com/IBM/onnxmlir-triton-backend) on Linux on IBM zSystems. This backend allows the usage of ONNX MLIR compiled models (model.so) with the Triton Inference Server. 

## 4. Additional resources
Find out additional resources about Triton Inference Server in the below links. 
1. [Triton Inference server user guide](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html)
2. [Triton Inference server github organization](https://github.com/triton-inference-server)


## 5. License
If you would like to see the detailed LICENSE click [here](LICENSE).
