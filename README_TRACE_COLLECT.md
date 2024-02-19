# Collecting Traces from Triton Inference Server
Example materials to demonstrate enabling and collecting traces from Triton Inference Server. 

## Useful trace flag information
Tracing can be enabled by command-line arguments when running the tritonserver executable.
There are many options setting up the traces. please do refer https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/trace.html#global-settings for more details. 

## Start the Triton Inference server with Trace enabled
```
docker run --shm-size 1G -u root --rm -p<Expose_PORT>:8000 -p<Expose_PORT>:8001 -p<Expose_PORT>:8002 -v//<path>/models:/models <imageid> tritonserver --model-repository=/models --trace-config triton,file=trace.json --trace-config triton,log-frequency=<number> --trace-config rate=<number> --trace-config level=TIMESTAMPS --trace-config count=<number>
``` 
`Note`: `--trace-config triton,file` option indicates where the trace output should be written. It will capture traces once inference requests (reqiured) are recieved at server. 


## Collecting Trace files

Once Trace files are generated, these files can be found inside container.

Example: 
```
ibm-user@<container_id>:~$ ls
trace.json.0 trace.json.1 ...
```

## Reference resources

- https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/trace.html