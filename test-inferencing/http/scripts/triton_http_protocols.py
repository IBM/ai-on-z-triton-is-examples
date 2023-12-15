import requests
import argparse
import json

def get_logging(method_args):
    logging_endpoint = "http://"+method_args.server+"/v2/logging"
    resp_log = requests.get(logging_endpoint)

    if resp_log.status_code == 200:
        if resp_log.content:
            print("PASSED : Logging info and Got status {} and response as {}".format(resp_log.status_code,resp_log.content))
        else:
            print("PASSED : Logging info and Got status as {}.".format(resp_log.status_code))
    else:
        print("FAILED : Logging info and Got status {} and reason as {}".format(resp_log.status_code,resp_log.reason))
    
def update_logging(method_args):
    logging_data = json.dumps({"log_file":"server.log"})
    logging_endpoint = "http://"+method_args.server+"/v2/logging"
    resp_log = requests.post(logging_endpoint, data=logging_data)

    if resp_log.status_code == 200:
        if resp_log.content:
            print("PASSED : Updated logging info and Got status {} and response as {}".format(resp_log.status_code,resp_log.content))
        else:
            print("PASSED : Updated logging info and Got status as {}.".format(resp_log.status_code))
    else:
        print("FAILED : Updated logging info and Got status {} and reason as {}".format(resp_log.status_code,resp_log.reason))

def server_health(method_args):
    health_live_endpoint = "http://"+method_args.server+"/v2/health/live"
    resp_live = requests.get(health_live_endpoint)

    if resp_live.status_code == 200:
        if resp_live.content:
            print("PASSED : Health-live and Got status {} and response as {}".format(resp_live.status_code,resp_live.content))
        else:
            print("PASSED : Health-live and Got status as {}.".format(resp_live.status_code))
    else:
        print("FAILED : Health-live and Got status {} and reason as {}".format(resp_live.status_code,resp_live.reason))

    #Health ready
    health_ready_endpoint = "http://"+method_args.server+"/v2/health/ready"
    resp_ready = requests.get(health_ready_endpoint)

    if resp_ready.status_code == 200:
        if resp_ready.content:
            print("PASSED : Health-ready and Got status {} and response as {}".format(resp_ready.status_code,resp_ready.content))
        else:
            print("PASSED : Health-ready and Got status as {}.".format(resp_ready.status_code))
    else:
        print("FAILED : Health-ready and Got status {} with reason as {}".format(resp_ready.status_code,resp_ready.reason))

def model_health(method_args):
    if method_args.model:
        if method_args.model_version:
            model_ready_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/versions/"+method_args.model_version+"/ready"
        else:
            model_ready_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/ready"
        resp_model_ready = requests.get(model_ready_endpoint)

        if resp_model_ready.status_code == 200:
            if resp_model_ready.content:
                print("PASSED : Model health-ready and Got status {} and response as {}".format(resp_model_ready.status_code,resp_model_ready.content))
            else:
                print("PASSED : Model health-ready and Got status as {}.".format(resp_model_ready.status_code))
        else:
            print("FAILED : Model health-ready and Got status {} and reason as {}".format(resp_model_ready.status_code,resp_model_ready.reason))
    else:
        print("FAILED : Model health-ready, please provide model name.")

def server_metadata(method_args):
    #Server metadata
    server_metadata_endpoint = "http://"+method_args.server+"/v2"
    resp_server = requests.get(server_metadata_endpoint)
    
    if resp_server.status_code == 200:
        if resp_server.content:
            print("PASSED : Server metadata and Got status {} and response as {}".format(resp_server.status_code,resp_server.content))
        else:
            print("PASSED : Server metadata and Got status as {}.".format(resp_server.status_code))
    else:
        print("FAILED : Server metadata and Got status {} and reason as {}".format(resp_server.status_code,resp_server.reason))

def model_metadata(method_args):
    if method_args.model:
        if method_args.model_version:
            model_metadata_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/versions/"+method_args.model_version
        else:
            model_metadata_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model
        resp_model_meta = requests.get(model_metadata_endpoint)

        if resp_model_meta.status_code == 200:
            if resp_model_meta.content:
                print("PASSED : Model metadata and Got status {} and response as {}".format(resp_model_meta.status_code,resp_model_meta.content))
            else:
                print("PASSED : Model metadata and Got status as {}.".format(resp_model_meta.status_code))
        else:
            print("FAILED : Model metadata and Got status {} and reason as {}".format(resp_model_meta.status_code,resp_model_meta.reason))
    else:
        print("FAILED : Model metadata, please provide model name.")

def model_statistics(method_args):
    if method_args.model:
        if method_args.model_version:
            model_stats_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/versions/"+method_args.model_version+"/stats"
        else:
            model_stats_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/stats"
        resp_model_stats = requests.get(model_stats_endpoint)

        if resp_model_stats.status_code == 200:
            if resp_model_stats.content:
                print("PASSED : Model statistics and Got status {} and response as {}".format(resp_model_stats.status_code,resp_model_stats.content))
            else:
                print("PASSED : Model statistics and Got status as {}.".format(resp_model_stats.status_code))
        else:
            print("FAILED : Model statistics and Got status {} and reason as {}".format(resp_model_stats.status_code,resp_model_stats.reason))
    else:
        print("FAILED : Model statistics, please provide model name.")   

def model_configuration(method_args):
    if method_args.model:
        if method_args.model_version:
            model_config_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/versions/"+method_args.model_version+"/config"
        else:
            model_config_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/config"
        resp_model_config = requests.get(model_config_endpoint)

        if resp_model_config.status_code == 200:
            if resp_model_config.content:
                print("PASSED : Model configuration and Got status {} and response as {}".format(resp_model_config.status_code,resp_model_config.content))
            else:
                print("PASSED : Model configuration and Got status as {}.".format(resp_model_config.status_code))
        else:
            print("FAILED : Model configuration and Got status {} and reason as {}".format(resp_model_config.status_code,resp_model_config.reason))
    else:
        print("FAILED : Model configuration, please provide model name.")

def model_repository(method_args):
    index_endpoint = "http://"+method_args.server+"/v2/repository/index"
    resp_index = requests.post(index_endpoint)

    if resp_index.status_code == 200:
        if resp_index.content:
            print("PASSED : Model repository index and Got status {} and response as {}".format(resp_index.status_code,resp_index.content))
        else:
            print("PASSED : Model repository index and Got status as {}.".format(resp_index.status_code))
    else:
        print("FAILED : Model repository index and Got status {} and reason as {}".format(resp_index.status_code,resp_index.reason))

def get_model_trace(method_args):
    if method_args.model: 
        trace_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/trace/setting"
        resp_trace = requests.get(trace_endpoint)

        if resp_trace.status_code == 200:
            if resp_trace.content:
                print("PASSED : Model trace and Got status {} and response as {}".format(resp_trace.status_code,resp_trace.content))
            else:
                print("PASSED : Model trace and Got status as {}.".format(resp_trace.status_code))
        else:
            print("FAILED : Model trace and Got status {} and reason as {}".format(resp_trace.status_code,resp_trace.reason))
    else:
        print("FAILED : Model trace, please provide model name.")

def update_model_trace(method_args):
    if method_args.model:   
        trace_data = json.dumps({"trace_rate":"1000"})
        trace_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/trace/setting"
        resp_trace = requests.post(trace_endpoint, data=trace_data)

        if resp_trace.status_code == 200:
            if resp_trace.content:
                print("PASSED : Updated model trace and Got status {} and response as {}".format(resp_trace.status_code,resp_trace.content))
            else:
                print("PASSED : Updated model trace and Got status as {}.".format(resp_trace.status_code))
        else:
            print("FAILED : Updated model trace and Got status {} and reason as {}".format(resp_trace.status_code,resp_trace.reason))
    else:
        print("FAILED : Update model trace, please provide model name.")

def model_load(method_args):
    if method_args.model:
        load_endpoint = "http://"+method_args.server+"/v2/repository/models/"+method_args.model+"/load"
        resp_load = requests.post(load_endpoint)

        if resp_load.status_code == 200:
            if resp_load.content:
                print("PASSED : Model loaded and Got status {} and response as {}".format(resp_load.status_code,resp_load.content))
            else:
                print("PASSED : Model loaded and Got status as {}.".format(resp_load.status_code))
        else:
            print("FAILED : Model loaded and Got status {} with reason as {}".format(resp_load.status_code,resp_load.reason))
    else:
        print("FAILED : Model load, please provide model name.")

def model_unload(method_args):
    if method_args.model:
        unload_endpoint = "http://"+method_args.server+"/v2/repository/models/"+method_args.model+"/unload"
        resp_unload = requests.post(unload_endpoint)

        if resp_unload.status_code == 200:
            if resp_unload.content:
                print("PASSED : Model unloaded info and Got status {} and response as {}".format(resp_unload.status_code,resp_unload.content))
            else:
                print("PASSED : Model unloaded and Got status as {}.".format(resp_unload.status_code))
        else:
            print("FAILED : Model unloaded and Got status {} and reason as {}".format(resp_unload.status_code,resp_unload.reason))
    else:
        print("FAILED : Model unload, please provide model name.")

def model_infer(method_args):
    if method_args.model and method_args.input:
        #load input data
        file = open(method_args.input, 'r')
        j = file.readlines()
        j = ''.join(j)
        j = j.replace(" ", "").replace("\n","")
        input_batch = json.loads(j)

        if method_args.model_version:
            inference_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/versions/"+method_args.model_version+"/infer"
        else:
            inference_endpoint = "http://"+method_args.server+"/v2/models/"+method_args.model+"/infer"
            
        resp_infer = requests.post(inference_endpoint, json=input_batch)

        if resp_infer.status_code == 200:
            if resp_infer.content:
                print("PASSED : Model inferenceo and Got status {} and response as {}".format(resp_infer.status_code,resp_infer.content))
            else:
                print("PASSED : Model inference and Got status as {}.".format(resp_infer.status_code))
        else:
            print("FAILED : Model inference and Got status {} and reason as {}".format(resp_infer.status_code,resp_infer.reason))
    else:
        print("FAILED : Model inference, please provide model name and input data file location.")

def model_explicit_methods_test(method_args):
    #Logging info
    get_logging(method_args)
    #Logging info updated
    update_logging(method_args)
    #Health live
    server_health(method_args)
    #Server metadata
    server_metadata(method_args)
    #Model metadata
    model_metadata(method_args)
    #Model statistics
    model_statistics(method_args)
    #Model ready state
    model_health(method_args)
    #Trace info
    get_model_trace(method_args)
    #Update trace info
    update_model_trace(method_args)
    #Model configuration
    model_configuration(method_args)
    #Model Repository Extension
    #Model repository index
    model_repository(method_args)
    #Model unload
    model_unload(method_args)
    #Model load
    model_load(method_args)
    #Model infer with inputs
    model_infer(method_args)

switcher={"get_logging":get_logging,
    "update_logging":update_logging,
    "server_health":server_health,
    "server_metadata":server_metadata,
    "model_metadata":model_metadata,
    "model_statistics":model_statistics,
    "model_health":model_health,
    "get_model_trace":get_model_trace,
    "update_model_trace":update_model_trace,
    "model_configuration":model_configuration,
    "model_index":model_repository,
    "model_unload":model_unload,
    "model_load":model_load,
    "model_infer":model_infer,
    "all":model_explicit_methods_test
    }

def switch(method_args):
    return switcher.get(method_args.method_name, model_explicit_methods_test)(method_args)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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
        "-v",
        "--model_version",
        type=str,
        required=False,
        help="Deployed model version.",
    )
    parser.add_argument(
        "-f",
        "--method_name",
        type=str,
        required=False,
        help="API method to call the triton server. Default is all.",
    )

    FLAGS = parser.parse_args()
    switch(FLAGS)
    