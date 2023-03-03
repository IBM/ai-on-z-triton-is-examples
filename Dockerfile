# Copyright contributors to the ai-on-z-triton-is-examples project.
#
# Copyright 2019-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

FROM icr.io/ibmz/ubuntu:22.04

ARG DEBIAN_FRONTEND="noninteractive"
ARG TRITON_VERSION=2.30.0
ARG RELEASE_BRANCH=r23.01
ARG SNAPML_VERSION=1.12.0


RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    rapidjson-dev libboost-dev \
    libre2-dev libnuma-dev \
    uuid-dev zlib1g-dev \
    libarchive-dev libb64-dev \
    libssl-dev libcurl4-openssl-dev \
    python3 python3-dev python3-pip python3-scipy \
    libblas3 liblapack3 liblapack-dev libopenblas-dev \
    libopenblas-dev libopenblas64-dev gfortran \
    pkg-config cmake git wget curl

ENV PATH=/opt/tritonserver/bin:$PATH \ 
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/tritonserver/lib/ \ 
    BUILD_DIR=/tmp/triton_build

WORKDIR ${BUILD_DIR}

RUN curl -Lsk "https://cmake.org/files/v3.24/cmake-3.24.1.tar.gz" -o cmake-3.24.1.tar.gz && \
    tar -xzvf cmake-3.24.1.tar.gz && \
    cd cmake-3.24.1/ && \
    ./bootstrap  && \
    make -j2 && \
    make install

#by default ubuntu:22.04 is having gcc 11.3 and python3.10
RUN git clone --branch ${RELEASE_BRANCH} https://github.com/triton-inference-server/server.git && \
    mkdir -p server/build && \
    cd server/build && \ 
    export CXXFLAGS="-std=c++14 -Wno-range-loop-construct -Wno-maybe-uninitialized" && \
    cmake -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX:PATH=/opt/tritonserver \
    -DTRITON_VERSION:STRING=${TRITON_VERSION} \
    -DTRITON_COMMON_REPO_TAG:STRING=${RELEASE_BRANCH} \
    -DTRITON_CORE_REPO_TAG:STRING=${RELEASE_BRANCH} \
    -DTRITON_BACKEND_REPO_TAG:STRING=${RELEASE_BRANCH} \
    -DTRITON_THIRD_PARTY_REPO_TAG:STRING=${RELEASE_BRANCH} \
    -DTRITON_ENABLE_LOGGING:BOOL=ON \
    -DTRITON_ENABLE_STATS:BOOL=ON \
    -DTRITON_ENABLE_METRICS:BOOL=ON \
    -DTRITON_ENABLE_METRICS_GPU:BOOL=OFF \
    -DTRITON_ENABLE_METRICS_CPU:BOOL=ON \
    -DTRITON_ENABLE_TRACING:BOOL=ON \
    -DTRITON_ENABLE_NVTX:BOOL=OFF \
    -DTRITON_ENABLE_GPU:BOOL=OFF \
    -DTRITON_ENABLE_MALI_GPU:BOOL=OFF \
    -DTRITON_ENABLE_GRPC:BOOL=ON \
    -DTRITON_ENABLE_HTTP:BOOL=ON \
    -DTRITON_ENABLE_SAGEMAKER:BOOL=OFF \
    -DTRITON_ENABLE_VERTEX_AI:BOOL=OFF \
    -DTRITON_ENABLE_GCS:BOOL=OFF \
    -DTRITON_ENABLE_S3:BOOL=OFF \
    -DTRITON_ENABLE_AZURE_STORAGE:BOOL=OFF \
    -DTRITON_ENABLE_ENSEMBLE:BOOL=OFF \
    -DTRITON_ENABLE_TENSORRT:BOOL=OFF .. && \ 
    make install 


RUN git clone -b ${RELEASE_BRANCH} https://github.com/triton-inference-server/python_backend.git && \
    mkdir -p  python_backend/build && \ 
    cd python_backend/build && \
    cmake  -DTRITON_ENABLE_GPU=OFF \ 
    -DTRITON_BACKEND_REPO_TAG=${RELEASE_BRANCH} \ 
    -DTRITON_COMMON_REPO_TAG=${RELEASE_BRANCH} \ 
    -DTRITON_CORE_REPO_TAG=${RELEASE_BRANCH} \ 
    -DCMAKE_INSTALL_PREFIX:PATH=/opt/tritonserver/ .. && \
    make install

#Build dependencies
RUN pip3 install setuptools==59.6.0 joblib==1.2.0 six==1.16.0 \ 
    threadpoolctl==3.1.0 cython==0.29.33 meson==1.0.0 pkgconfig==1.5.5 \ 
    ninja==1.11.1 pythran==0.12.1 
# Runtime dependencies
RUN pip3 install numpy==1.22.3 scipy==1.10.0 scikit-learn==1.1.2 \
    pandas==1.4.2

# Install SnapML 
RUN pip3 install snapml==${SNAPML_VERSION}

# clean up
WORKDIR ${BUILD_DIR}
RUN rm -rf *
