import os
import tensorflow as tf
import cv2
import numpy as np
import time
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from typing import Dict, List, Union

# suppress all tensorflow info messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

# Adapted from https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_custom_trained_model_sample.py
def vertex_ai_predict(instances: Union[Dict, List[Dict]], client, endpoint):

    # jsonify inputs
    instances = [json_format.ParseDict(instances[0], Value())]

    # Query model on VertexAI
    response = client.predict(endpoint=endpoint, instances=instances)

   # The predictions are a google.protobuf.Value representation of the model's predictions.
    return response.predictions


def load_vertex_ai_client(api_endpoint: str):

    # This client only needs to be initialized once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": api_endpoint})
    return client


def reconstruct(video_filepath):

    # Load VertexAI info from environment
    project = os.environ['GCLOUD_PROJECT_ID']
    endpoint_id = os.environ["VERTEX_AI_ENDPOINT_ID"]
    location = os.environ["VERTEX_AI_LOCATION"]
    api_endpoint = os.environ["VERTEX_AI_API_ENDPOINT"]

    ''' for debugging
    print("\n")
    print("------------------------------------------------------")
    print("Initializing VertexAI client")
    print("------------------------------------------------------")
    '''

    # Initialize VertexAI client
    client = load_vertex_ai_client(api_endpoint)
    endpoint = f"projects/{project}/locations/{location}/endpoints/{endpoint_id}"

    print("\n")
    print("------------------------------------------------------")
    print(f"Analyzing video file from {video_filepath} ...")
    print("------------------------------------------------------")

    keypoints_timeseries = []
    cap = cv2.VideoCapture(video_filepath)
    fps = round(cap.get(cv2.CAP_PROP_FPS), 2)

    while cap.isOpened():
        ret, frame = cap.read()

        # All video frames have been read
        if frame is None:
            print("\n")
            print("------------------------------------------------------")
            print("Pose estimation of video completed")
            print("------------------------------------------------------")
            break

        # Resize frame dims to multiple of 32 and longer side 256
        # 160:256 is closer to original aspect ratio but VertexAI can
        # only handle inputs up to 1.5 MB
        img = frame.copy()
        print("WEEEEEEEEeeeeeEEEEEEEEEEE")
        print(type(img))
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 128,256)

        # Cast to 32-bit int representation
        img = tf.cast(img, dtype=tf.int32)

        # Represent input as a list for python client api
        img_list = img.numpy().tolist()

        ''' for debugging
        print("\n")
        print("------------------------------------------------------")
        print("Connecting to VertexAI to get prediction")
        print("------------------------------------------------------")
        '''

        # Get prediction
        results = vertex_ai_predict( instances=img_list, client=client,\
                                     endpoint=endpoint)

        ''' for debugging
        print("\n")
        print("------------------------------------------------------")
        print("Prediction received")
        print("------------------------------------------------------")
        '''

        # Extract first person, truncate bounding box info, and reshape
        # 17 body keypoints each with x, y, and confidence score
        results = np.array(results[0][0])[:51].reshape(17, 3)
        keypoints_timeseries.append(results)

    cap.release()
    cv2.destroyAllWindows()

    return np.array(keypoints_timeseries), fps

if __name__ == "__main__" :

    t0 = time.time()

    keypoints, fps = reconstruct('test.mp4')

    total_time = round(time.time() - t0, 2)

    print("\n")
    print("------------------------------------------------------")
    print("Shape of keypoints:", keypoints.shape) # (frames, 17, 3)
    print("Frame rate:", fps)
    print("Pose estimation took", total_time, "seconds")
    print("------------------------------------------------------")
