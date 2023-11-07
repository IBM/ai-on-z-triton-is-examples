FROM nvcr.io/nvidia/tritonserver:23.10-py3

# Install SnapML 
RUN pip install scikit-learn==1.1.2
RUN pip install snapml==1.13.0
RUN pip install xgboost==1.7.5