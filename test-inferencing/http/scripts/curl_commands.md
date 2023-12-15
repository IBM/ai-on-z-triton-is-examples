Model Management: Triton operates in one of three model control modes: NONE, EXPLICIT, or POLL. The model control determines how Triton handles changes to the model repository and which protocols and APIs are available.
#Run Triton server with different modes of model control:
#Model Control Mode NONE: Changes to the model repository while the server is running will be ignored.
Default PORTS exposed by TRITION IS: HTTP:8000 GRPC:8001 Metrics:8002

```
docker run --shm-size 1G --rm -p<EXPOSE_HTTP_PORT_NUM>::8000 -p <EXPOSE_GRPC_PORT_NUM>:8001 -p<EXPOSE_Metrics_PORT_NUM>:8002 -v//$PWD/models:/models <TRITON_SERVER_IMAGE_ID> tritonserver --model-repository=/models  
```

## HEALTH API
Health Live
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/health/live
```
Health Ready
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/health/ready
```
Model Health
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/models/<MODEL_NAME>/ready
```
Model Health with version
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/models/<MODEL_NAME>/versions/ <MODEL_VERSION>/ready
```

## METADATA API
Server Metadata
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2
```
Model Metadata
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/models/<MODEL_NAME>
```
Model Metadata with version
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/models/<MODEL_NAME>/versions/ <MODEL_VERSION>
```

## INFERENCE API
```
curl -X POST -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/models/<MODEL_NAME>/versions/<MODEL_VERSION>/infer --data <INPUT_DATA>
```

## MODEL CONFIG API
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/models/<MODEL_NAME>/versions/ <MODEL_VERSION>/config
```

## MODEL REPOSITORY API
```
curl -X POST -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/repository/index
```

## STATISTICS API
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/models/<MODEL_NAME>/versions/<MODEL_VERSION>/stats
```

## TRACE API
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/trace/setting
curl -X POST -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/models/<MODEL_NAME>/trace/setting -d <TRACE_DATA>
```

## LOGGING API
```
curl -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/logging
curl -X POST -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/logging -d <LOGGING_DATA>
```

Model Control Mode EXPLICIT: Triton loads only those models specified explicitly with the --load-model command-line option. To load ALL models at startup, specify --load-model=*
#Load all models in model repository:
Default PORTS exposed by TRITION IS: HTTP:8000 GRPC:8001 Metrics:8002

```
docker run --shm-size 1G --rm -p<EXPOSE_HTTP_PORT_NUM>::8000 -p <EXPOSE_GRPC_PORT_NUM>:8001 -p<EXPOSE_Metrics_PORT_NUM>:8002 -v//$PWD/models:/models <TRITON_SERVER_IMAGE_ID> tritonserver --model-repository=/models  --model-control-mode=explicit --load-model=*
```

#Load specific model:
Default PORTS exposed by TRITION IS: HTTP:8000 GRPC:8001 Metrics:8002

```
docker run --shm-size 1G --rm -p<EXPOSE_HTTP_PORT_NUM>::8000 -p <EXPOSE_GRPC_PORT_NUM>:8001 -p<EXPOSE_Metrics_PORT_NUM>:8002 -v//$PWD/models:/models <TRITON_SERVER_IMAGE_ID> tritonserver --model-repository=/models  --model-control-mode=explicit --load-model=<MODEL_NAME>
```

Model Load
```
curl -X POST -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/repository/models/<MODEL_NAME>/load
```

Model Unload
```
curl -X POST -v <TRITON_SERVER_IP: EXPOSE_HTTP_PORT_NUM>/v2/repository/models/<MODEL_NAME>/unload
```

#Model Control Mode POLL: Changes to the model repository will be detected and Triton will attempt to load and unload models as necessary based on those changes. We can control the polling interval with the --repository-poll-secs option by default it is 15 sec.

Default PORTS exposed by TRITION IS: HTTP:8000 GRPC:8001 Metrics:8002
```
docker run --shm-size 1G --rm -p<EXPOSE_HTTP_PORT_NUM>::8000 -p <EXPOSE_GRPC_PORT_NUM>:8001 -p<EXPOSE_Metrics_PORT_NUM>:8002 -v//$PWD/models:/models <TRITON_SERVER_IMAGE_ID> tritonserver --model-repository=/models  --model-control-mode=poll 
```