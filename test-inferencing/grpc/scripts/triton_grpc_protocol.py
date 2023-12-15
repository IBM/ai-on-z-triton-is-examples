import argparse
import sys
import json
import numpy as np

import tritonclient.grpc as grpcclient

def server_health(method_args):
    try:
        triton_client = grpcclient.InferenceServerClient(
            url=method_args.server, verbose=method_args.verbose
        )
    except Exception as e:
        print("context creation failed: " + str(e))
        sys.exit()

    if not triton_client.is_server_live(headers={"test": "1", "dummy": "2"}):
        print("FAILED : is_server_live")
        sys.exit(1)
    else:
        print("PASSED : Health-live\n")

    if not triton_client.is_server_ready():
        print("FAILED : is_server_ready")
        sys.exit(1)
    else:
        print("PASSED : Health-ready\n")

def model_health(method_args):
    try:
        triton_client = grpcclient.InferenceServerClient(
            url=method_args.server, verbose=method_args.verbose
        )
    except Exception as e:
        print("context creation failed: " + str(e))
        sys.exit()

    if FLAGS.model:
        if not triton_client.is_model_ready(FLAGS.model):
            print("FAILED : is_model_ready")
            sys.exit(1)
        else:
            print("PASSED : Model health-ready\n")
    else:
        print("FAILED : Model health-ready, please provide model name.")

def server_metadata(method_args):
    try:
        triton_client = grpcclient.InferenceServerClient(
            url=method_args.server, verbose=method_args.verbose
        )
    except Exception as e:
        print("context creation failed: " + str(e))
        sys.exit()

    metadata = triton_client.get_server_metadata()
    if not (metadata.name == "triton"):
        print("FAILED : get_server_metadata")
        sys.exit(1)
    else:
        print("Passed: Get the metadata of {} server successfully.".format(metadata.name))

def model_metadata(method_args):
    try:
        triton_client = grpcclient.InferenceServerClient(
            url=method_args.server, verbose=method_args.verbose
        )
    except Exception as e:
        print("context creation failed: " + str(e))
        sys.exit()
    
    if method_args.model:
        metadata = triton_client.get_model_metadata(
            method_args.model, headers={"test": "1", "dummy": "2"}
        )
        if not (metadata.name == method_args.model):
            print("FAILED : get_model_metadata")
            sys.exit(1)
        else:
            print("Passed: Get the metadata of {} successfully.".format(method_args.model))
    else:
        print("FAILED : Model metadata, please provide model name.")

def model_configuration(method_args):
    try:
        triton_client = grpcclient.InferenceServerClient(
            url=method_args.server, verbose=method_args.verbose
        )
    except Exception as e:
        print("context creation failed: " + str(e))
        sys.exit()

    if method_args.model:
        config = triton_client.get_model_config(method_args.model)
        if not (config.config.name == method_args.model):
            print("FAILED: get_model_config")
            sys.exit(1)
        else:
            print("Passed: Get the configuration of {} successfully.".format(method_args.model))
    else:
        print("FAILED : Model configuration, please provide model name.")

def model_infer(method_args):
    try:
        triton_client = grpcclient.InferenceServerClient(
            url=method_args.server, verbose=method_args.verbose
        )
    except Exception as e:
        print("context creation failed: " + str(e))
        sys.exit()

    #Inferense
    inputs = []
    outputs = []

    #Model infer with inputs
    if method_args.model and method_args.input:
        #load input data
        file = open(method_args.input, 'r')
        j = file.readlines()
        j = ''.join(j)
        j = j.replace(" ", "").replace("\n","")
        input_batch = json.loads(j)

        data = input_batch['inputs'][0]['data']
        input_data = grpcclient.InferInput(input_batch['inputs'][0]['name'], input_batch['inputs'][0]['shape'], input_batch['inputs'][0]['datatype'])
        input0_data = np.array(data, dtype=np.dtype(method_args.datatype))
        input_data.set_data_from_numpy(input0_data)
        inputs = [input_data]

        #output data defining
        output = grpcclient.InferRequestedOutput(method_args.output_arg)
        outputs = [output]

        # Test with outputs
        results = triton_client.infer(
            model_name=method_args.model,
            inputs=inputs,
            outputs=outputs,
            headers={'test': '1'})
        
        prediction_result = results.as_numpy(method_args.output_arg)

        if type(prediction_result[0]) is np.ndarray and method_args.datatype == "bytes":
            prediction_result = list(map(lambda x: str(x,"utf=8"), prediction_result[0]))
            data = data[0]
        elif method_args.datatype == "bytes":
            prediction_result = list(map(lambda x: str(x,"utf=8"), prediction_result))

        print("Passed: Get the inference of {} successfully and predicted as {}\n".format(method_args.model, prediction_result))

        statistics = triton_client.get_inference_statistics(model_name=method_args.model)
        if len(statistics.model_stats) != 1:
            print("FAILED: Inference Statistics")
            sys.exit(1)
    else:
        print("FAILED : Model inference, please provide model name and input data file location.")

def model_explicit_methods_test(method_args):
    #Health live
    server_health(method_args)
    #Model ready state
    model_health(method_args)
    #Server metadata
    server_metadata(method_args)
    #Model metadata
    model_metadata(method_args)
    #Model configuration
    model_configuration(method_args)
    #Model infer with inputs
    model_infer(method_args)

switcher={
    "server_health":server_health,
    "server_metadata":server_metadata,
    "model_metadata":model_metadata,
    "model_health":model_health,
    "model_configuration":model_configuration,
    "model_infer":model_infer,
    "all":model_explicit_methods_test
    }

def switch(method_args):
    return switcher.get(method_args.method_name, model_explicit_methods_test)(method_args)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        default=False,
        help="Enable verbose output",
    )
    parser.add_argument(
        "-s",
        "--server",
        type=str,
        required=False,
        default="localhost:8000",
        help="Inference server URL. Default is localhost:8001.",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        required=False,
        help="Deployed model name.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=False,
        help="Path to input data in json format.",
    )
    parser.add_argument(
        '-d', 
        '--datatype', 
        type=str, 
        default='float32',
        help="datatype")
    parser.add_argument(
        '-o', 
        '--output_arg', 
        type=str, 
        default='OUT0',
        help="Output argument name.")
    parser.add_argument(
        "-f",
        "--method_name",
        type=str,
        required=False,
        help="API method to call the triton server. Default is all.",
    )

    FLAGS = parser.parse_args()
    switch(FLAGS)
