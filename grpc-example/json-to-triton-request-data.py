import grpc_service_pb2
import json
import numpy as np
import struct
import argparse

def to_triton_data(input_,input_tensor):
    if input_.datatype == "BYTES":
        if input_tensor.size == 0:return np.empty([0], dtype=np.object_)
        if (input_tensor.dtype != np.object_) and (input_tensor.dtype.type != np.bytes_): raise Exception("cannot serialize bytes tensor: invalid datatype")
        flattened_ls = []
        for obj in np.nditer(input_tensor, flags=["refs_ok"], order='C'):
            if input_tensor.dtype == np.object_:
                s = obj.item() if type(obj.item()) == bytes else str(obj.item()).encode('utf-8')
            else:
                s = obj.item()
            flattened_ls.append(struct.pack("<I", len(s)))
            flattened_ls.append(s)
        flattened = b''.join(flattened_ls)
        serialized_output = np.asarray(flattened, dtype=np.object_)
        if not serialized_output.flags['C_CONTIGUOUS']:
            serialized_output = np.ascontiguousarray(serialized_output,dtype=np.object_)
        return serialized_output.item() if serialized_output.size > 0 else b''
    else:
        return input_tensor.tobytes()

def data_convertion(method_args):
    #load input data
    file = open(method_args.input, 'r')
    input_batch = json.loads(''.join(file.readlines()).replace(" ", "").replace("\n",""))
    #input data defining
    input_ = grpc_service_pb2.ModelInferRequest().InferInputTensor()
    input_.name = input_batch['inputs'][0]['name']
    input_.ClearField("shape")
    input_.shape.extend(input_batch['inputs'][0]['shape'])
    input_.datatype = input_batch['inputs'][0]['datatype']
    input0_data = np.array(input_batch['inputs'][0]['data'], dtype=np.dtype(method_args.inp_datatype))
    #output data defining
    output = grpc_service_pb2.ModelInferRequest().InferRequestedOutputTensor(name=input_batch['outputs'][0]['name'])
    #service_pb2 request
    request_ = grpc_service_pb2.ModelInferRequest(model_name=method_args.model_name, model_version=method_args.model_version)
    request_.inputs.extend([input_])
    request_.raw_input_contents.extend([to_triton_data(input_, input0_data)])
    request_.outputs.extend([output])

    with open(method_args.output, 'wb') as f:
        f.write(request_.SerializeToString())

    print("done the conversion!!!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model_name", type=str, required=False, help="Deployed model name.")
    parser.add_argument("-v", "--model_version", type=str, required=False, default="", help="Deployed model version.")
    parser.add_argument("-i", "--input", type=str, required=False, help="Path to input data in json format.")
    parser.add_argument('-d', '--inp_datatype', type=str, default='float32', help="Input datatype")
    parser.add_argument("-o", "--output", type=str, required=False, help="Path to output data file to be saved.")
    FLAGS = parser.parse_args()

    data_convertion(FLAGS)