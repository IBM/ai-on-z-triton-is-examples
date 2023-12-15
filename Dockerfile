FROM icr.io/ibmz/tritonserver-s390x:23.04-py3.10
RUN apt-get install llvm -y

COPY ./requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt
