# Copyright (c) 2021, NVIDIA CORPORATION. All rights reserved.
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

import json
import joblib
from snapml import BoostingMachineClassifier
import numpy as np
from pathlib import Path
import triton_python_backend_utils as pb_utils
import random
import string
import time
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

SNAPML_MODEL_FILE = "model_xgb.json"
SNAPML_MODEL_PREPROCESS_FILE = "pipeline_xgb.joblib"

class TritonPythonModel:
    """Your Python model must use the same class name. Every Python model
    that is created must have "TritonPythonModel" as the class name.
    """

    def initialize(self, args):
        """`initialize` is called only once when the model is being loaded.
        Implementing `initialize` function is optional. This function allows
        the model to intialize any state associated with this model.
        Parameters
        ----------
        args : dict
          Both keys and values are strings. The dictionary keys and values are:
          * model_config: A JSON string containing the model configuration
          * model_instance_kind: A string containing model instance kind
          * model_instance_device_id: A string containing model instance device ID
          * model_repository: Model repository path
          * model_version: Model version
          * model_name: Model name
        """

        # You must parse model_config. JSON string is not parsed here
        self.model_config = model_config = json.loads(args['model_config'])

        # Get OUT0 configuration
        output0_config = pb_utils.get_output_config_by_name(model_config, "OUT0")

        # Convert Triton types to numpy types
        self.output0_dtype = pb_utils.triton_string_to_numpy(output0_config['data_type'])

        load_path = Path(__file__).parent

        # Load the pipeline
        self.pipeline = joblib.load(str(load_path / SNAPML_MODEL_PREPROCESS_FILE))
        self.normalizer = self.pipeline['preprocessor'].transformers_[0][1]['normalizer']
        self.discretizer = self.pipeline['preprocessor'].transformers_[0][1]['discretizer']
        self.onehot = self.pipeline['preprocessor'].transformers_[1][1]['onehot']

        # Load the model into SnapML
        self.snap_model = BoostingMachineClassifier()
        self.snap_model.import_model(str(load_path / SNAPML_MODEL_FILE), 
                                     input_type="xgb_json", tree_format="compress_trees")

    def execute(self, requests):
        """`execute` MUST be implemented in every Python model. `execute`
        function receives a list of pb_utils.InferenceRequest as the only
        argument. This function is called when an inference request is made
        for this model. Depending on the batching configuration (e.g. Dynamic
        Batching) used, `requests` may contain multiple requests. Every
        Python model, must create one pb_utils.InferenceResponse for every
        pb_utils.InferenceRequest in `requests`. If there is an error, you can
        set the error argument when creating a pb_utils.InferenceResponse
        Parameters
        ----------
        requests : list
          A list of pb_utils.InferenceRequest
        Returns
        -------
        list
          A list of pb_utils.InferenceResponse. The length of this list must
          be the same as `requests`
        """
        output0_dtype = self.output0_dtype
        responses = []
        slice_start =  np.zeros((len(requests),), dtype=int)
        slice_end =    np.zeros((len(requests),), dtype=int)

        # Every Python backend must iterate over everyone of the requests
        # and create a pb_utils.InferenceResponse for each of them.
        req_counter=0
        # stacking the input arrays and prepare for scoring.
        for request in requests:
            in_0 = pb_utils.get_input_tensor_by_name(request, "IN0")
            
            if ( req_counter > 0 ):
                array_final = np.concatenate((array_final, in_0.as_numpy()), axis=0)
                slice_start[req_counter] = slice_end[req_counter-1]
                slice_end[req_counter] = slice_end[req_counter-1]+in_0.as_numpy().shape[0]

            else:
                array_final = in_0.as_numpy()
                slice_start[req_counter] = 0
                slice_end[req_counter] = in_0.as_numpy().shape[0]

            req_counter+=1
        # Define the inference preprocessing steps
        #n_cat_feats = 20
        n_num_feats = 15

        num_data = array_final[:,0:n_num_feats].astype(np.float32)
        cat_data = array_final[:,n_num_feats:].astype('<U4')
        
        #transform the data
        num_data = self.normalizer.transform(num_data)
        num_data = self.discretizer.transform(num_data)

        cat_data = self.onehot.transform(cat_data)

        X_test =  np.concatenate((num_data, cat_data), axis=1)
       
        out_0 = self.snap_model.predict(X_test)
        out_0[out_0 < 0] = 0
        out_0[out_0 > 0] = 1

        
        res_counter=0
        # objects to create pb_utils.InferenceResponse.
        for request in requests:
            out_tensor_0 = pb_utils.Tensor("OUT0",
                out_0[slice_start[res_counter]:slice_end[res_counter]].astype(output0_dtype)) 
            # Create InferenceResponse. You can set an error here in case
            # there was a problem with handling this inference request.
            # Below is an example of how you can set errors in inference
            # response:
            #
            # pb_utils.InferenceResponse(
            #    output_tensors=..., TritonError("An error occured"))
            inference_response = pb_utils.InferenceResponse(
                output_tensors=[out_tensor_0])
            responses.append(inference_response)
            res_counter+=1 

        # You should return a list of pb_utils.InferenceResponse. Length
        # of this list must match the length of `requests` list.
        return responses

    def finalize(self):
        """`finalize` is called only once when the model is being unloaded.
        Implementing `finalize` function is OPTIONAL. This function allows
        the model to perform any necessary clean ups before exit.
        """
        print('Cleaning up...')
