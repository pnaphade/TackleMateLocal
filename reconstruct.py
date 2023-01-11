import os
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np

# suppress all tensorflow info messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

def reconstruct(model, video_filepath):

    print("\n")
    print("-----------------------------------------------------------")
    print("Reading video from file", video_filepath)
    print("-----------------------------------------------------------")

    kp_vid = []
    cap = cv2.VideoCapture(video_filepath)
    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()

        if frame is None:
            print("\n")
            print("-----------------------------------------------------------")
            print("Pose estimation complete")
            print("-----------------------------------------------------------")
            break

        # Resize frame dims to multiple of 32 and longer side 256
        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 160,256)

        # Represent image to 32-bit ints
        img = tf.cast(img, dtype=tf.int32)

        # Inference
        if model is None:
            print("*********model being loaded on the fly********")
            model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
            model = model.signatures['serving_default']
        kp_frame = model(img)

        # Extract first person
        # 17 keypoints with  y coord, x coord, confidence predictions
        kp_frame = kp_frame['output_0'].numpy()[0,0,:51].reshape((17,3))
        kp_vid.append(kp_frame)

    cap.release()

    return np.array(kp_vid), fps