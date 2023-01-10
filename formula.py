import numpy as np
import tensorflow_hub as hub
import time
import math
import reconstruct
import sys

def analyze_height(kp, kp_index, coords_index, tackle_frame, side):

    # Extract keypoints time series
    shoulder_y = kp[:, kp_index[f"{side} shoulder"], coords_index["y"]]
    shoulder_y = 1 - shoulder_y   # transform so 1 is highest
    ankle_y = kp[:, kp_index[f"{side} ankle"], coords_index["y"]]
    ankle_y = 1 - ankle_y   # transform so 1 is highest

    # Calculate difference between shoulder and ankle at tackle
    should_height_tackle = shoulder_y[tackle_frame] - ankle_y[tackle_frame]

    # Calculate difference between shoulder and ankle at every point before tackle
    shoulder_pretackle = shoulder_y[:tackle_frame-1]
    ankle_pretackle = ankle_y[:tackle_frame-1]
    should_height_pretackle = shoulder_pretackle - ankle_pretackle
    print("Number of pre-tackle frames:", should_height_pretackle.size)

    # Get a mask for selecting which indices have reasonable confidence
    shoulder_conf = kp[:, kp_index["left shoulder"], coords_index["conf"]]
    shoulder_conf_pretackle = shoulder_conf[:tackle_frame-1]
    shoulder_conf_mask = shoulder_conf_pretackle > 0.1
    #print("Confidence mask:", lshoulder_conf_mask)

    # Select shoulder-ankle differences which meet confidence threshold
    should_height_pretackle_filtered = should_height_pretackle[shoulder_conf_mask]
    print("Number of filtered pre-tackle frames:", should_height_pretackle_filtered.size)
    print("------------------------------------------------------")

    # Calculate max difference between shoulder and ankle before tackle
    max_should_height_pretackle = np.amax(should_height_pretackle_filtered)

    # Calculate difference in shoulder height
    should_diff = max_should_height_pretackle - should_height_tackle

    # Calculate percent change in shoulder height
    should_percent_change = abs(100 * (should_diff/max_should_height_pretackle))

    print("\n")
    print("------------------------------------------------------")
    print(f"Percent change in shoulder height: {round(should_percent_change, 2)}%")

    # Scoring percent in shoulder height change
    if(should_percent_change < 20):
        return 0
    if(20 <= should_percent_change  < 40):
        return 1
    if(40 <= should_percent_change < 50):
        return 2
    if(should_percent_change >= 50):
        return 3

def analyze_speed(kp, kp_index, coods_index, tackle_frame, side):
    '''
        # code for calculating acceleration
        left_shoulder_x = person0[:, kp_index["left shoulder"], coords_index["x"]]
        score0 = person0[:, kp_index["left shoulder"], coords_index["conf"]]
        score_mask = score0 > 0.5
        print("Shape of score mask:", score_mask.shape)
        print("Number of frames with score > 0.5:", score_mask.sum())
        # don't include frames with a score less than 0.5
        left_shoulder_x = left_shoulder_x[score_mask]
        left_shoulder_x = 1 - left_shoulder_x   # transform so 1 is highest

        visualize(shoulder_avankle_diff)
        '''

    return 0

def analyze_arm(kp, kp_index, coords_index, tackle_frame, side):

    # Step 1: calulate l, the distance between shoulder and elbow
    should_x = (kp[:, kp_index[f"{side} shoulder"], coords_index["x"]])
    should_y = 1 - (kp[:, kp_index[f"{side} shoulder"], coords_index["y"]])

    elbow_x = (kp[:, kp_index[f"{side} elbow"], coords_index["x"]])
    elbow_y = 1 - (kp[:, kp_index[f"{side} elbow"], coords_index["y"]])

    should_x = should_x[tackle_frame]
    should_y = should_y[tackle_frame]
    elbow_x = elbow_x[tackle_frame]
    elbow_y = elbow_y[tackle_frame]

    l = math.sqrt( (elbow_x-should_x)**2 + (elbow_y-should_y)**2 )


    # Step 2: calculate x, the horizontal between the shoulder and elbow
    x = elbow_x - should_x

    # Step 3: calculate x/l to determine how extended the arm was
    extension_ratio = round(x/l, 2)
    if side == "right":
        extension_ratio = extension_ratio * -1
    print("Arm extension ratio:", extension_ratio)

    # Scoring percent in shoulder height change
    if(extension_ratio < 0.1):
        return 0
    if(0.1 <= extension_ratio  < 0.2):
        return 1
    if(0.2 <= extension_ratio < 0.4):
        return 2
    if(extension_ratio >= 0.4):
        return 3

def score(model, video_filepath, timestamp, side):

    # Get body keypoints and framerate
    kp, fps = reconstruct.reconstruct(model, video_filepath)

    n_frames = len(kp)
    length = round(n_frames*(1/fps), 3)

    print("\n")
    print("------------------------------------------------------")
    print("Shape of keypoints:", kp.shape)
    print("Frame rate:", fps, "fps")
    print("Number of frames:", n_frames)
    print(f"Length of video: {length}s")
    print("------------------------------------------------------")

    body_kp = ["nose", "left eye", "right eye", "left ear",
            "right ear", "left shoulder", "right shoulder", "left elbow",
            "right elbow", "left wrist", "right wrist", "left hip", "right hip",
            "left knee", "right knee", "left ankle", "right ankle"]
    kp_ints = np.arange(len(body_kp))
    kp_index = dict(zip(body_kp, kp_ints))

    # Final dimension of kp array is encoded as y, x, confidence
    coords_index = {"y":0, "x":1, "conf":2}

    # Calculate difference between shoulder and ankle during tackle
    tackle_frame = int(round((fps * float(timestamp))))
    print("\n")
    print("------------------------------------------------------")
    print(f"Tackle timestamp: {round(timestamp, 2)}")
    print(f"Tackle frame: {tackle_frame}/{n_frames}")

    h_score = analyze_height(kp, kp_index, coords_index, tackle_frame, side)
    s_score = analyze_speed(kp, kp_index, coords_index, tackle_frame, side)
    a_score = analyze_arm(kp, kp_index, coords_index, tackle_frame, side)


    scores = {}
    scores["height"] = h_score
    scores["speed"] = s_score
    scores["arm"] = a_score

    print("Scores:", scores)
    feedback = {0:"poor", 1:"fair", 2:"good", 3:"excellent"}
    print(f"Tackle height score: {h_score}/3, {feedback[h_score]}")
    print(f"Arm extension score: {a_score}/3, {feedback[a_score]}")

    print("------------------------------------------------------")

    return scores, length



if __name__ == '__main__':

    t0 = time.time()

    model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
    model = model.signatures['serving_default'] # default model

    score(model, video_filepath='test.mp4', timestamp=2, side="left")

    total_time = round(time.time() - t0, 2)

    print("\n")
    print("------------------------------------------------------")
    print("Tackle scoring and pose estimation took", total_time, "seconds")
    print("------------------------------------------------------")
