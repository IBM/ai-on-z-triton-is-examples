import tritonclient.grpc as grpcclient
import tritonclient.http as httpclient

from google.protobuf import json_format
import json

def check_server_initial_state():
    # Helper function to make sure the log setting is properly
    # initialized / reset before actually running the test case.
    # Note that this function uses HTTP client so the pass/fail of
    # the HTTP log setting test cases should be checked to make sure
    # the initial state is checked properly before running other test cases.
    initial_settings = {
        "log_file": "",
        "log_info": True,
        "log_warning": True,
        "log_error": True,
        "log_verbose_level": 0,
        "log_format": "default",
    }
    triton_client = httpclient.InferenceServerClient("Server_ip:http_port")#9.76.XX.XX:8007
    print("initial_settings:\n",initial_settings, "\n", "triton_client.get_log_settings():\n",triton_client.get_log_settings(), "\n","******************\n")

def test_grpc_get_settings():
    # Log settings will be the same as default settings since
    # no update has been made.
    initial_settings = grpcclient.service_pb2.LogSettingsResponse()
    json_format.Parse(
        json.dumps(
            {
                "settings": {
                    "log_file": {"stringParam": ""},
                    "log_info": {"boolParam": True},
                    "log_warning": {"boolParam": True},
                    "log_error": {"boolParam": True},
                    "log_verbose_level": {"uint32Param": 0},
                    "log_format": {"stringParam": "default"},
                }
            }
        ),
        initial_settings,
    )
    triton_client = grpcclient.InferenceServerClient("Server_ip:grpc_port")#9.76.XX.XX:8008
    print(initial_settings,"\n",triton_client.get_log_settings(),"\n","*****************\n")


def test_grpc_update_settings():
    # Update each possible log configuration
    # field and check that they are reflected
    # by the server
    check_server_initial_state()

    triton_client = grpcclient.InferenceServerClient("Server_ip:grpc_port")#9.76.XX.XX:8008
    for i in range(22):
        log_settings_1 = {
            "log_file": "log_file{0}.log".format(i),
            "log_info": True,
            "log_warning": True,
            "log_error": True,
            "log_verbose_level": 0,
            "log_format": "default",
        }
        print(log_settings_1["log_file"])
        expected_log_settings_1 = grpcclient.service_pb2.LogSettingsResponse()
        json_format.Parse(
            json.dumps(
                {
                    "settings": {
                        "log_file": {"stringParam": "log_file{0}.log".format(i)},
                        "log_info": {"boolParam": True},
                        "log_warning": {"boolParam": True},
                        "log_error": {"boolParam": True},
                        "log_verbose_level": {"uint32Param": 0},
                        "log_format": {"stringParam": "default"},
                    }
                }
            ),
            expected_log_settings_1,
        )
    
        print("expected_log_settings_1:\n",
            expected_log_settings_1,"\n",
            "triton_client.update_log_settings(settings=log_settings_1):\n",
            triton_client.update_log_settings(settings=log_settings_1),"\n",
            "********************\n",
        )


if __name__ == "__main__":
    print("get intial setting for grpc logger:\n")
    test_grpc_get_settings()
    print("updated setting for grpc:\n")
    test_grpc_update_settings()