import reconstruct
import numpy as np
import time

def score(video_filepath, timestamp):

    # Get body keypoints and framerate
    kp, fps = reconstruct.reconstruct(video_filepath)

    n_frames = len(kp)
    length = round(n_frames*(1/fps), 2)

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

    # Final dimension of person array is encoded as y, x, confidence
    coords_index = {"y":0, "x":1, "conf":2}

    # Extract keypoints time series
    left_shoulder_y = kp[:, kp_index["left shoulder"], coords_index["y"]]
    left_shoulder_y = 1 - left_shoulder_y   # transform so 1 is highest
    left_ankle_y = kp[:, kp_index["left ankle"], coords_index["y"]]
    left_ankle_y = 1 - left_ankle_y   # transform so 1 is highest

    # Calculate difference between shoulder and ankle during tackle
    tackle_frame = int(round((fps * float(timestamp))))
    print("\n")
    print("------------------------------------------------------")
    print(f"Tackle frame: {tackle_frame}/{n_frames}")
    should_height_tackle = left_shoulder_y[tackle_frame] - left_ankle_y[tackle_frame]

    # Calculate difference between shoulder and ankle at every point before tackle
    lshoulder_pretackle = left_shoulder_y[:tackle_frame-1]
    lankle_pretackle = left_ankle_y[:tackle_frame-1]
    should_height_pretackle = lshoulder_pretackle - lankle_pretackle
    print("Number of pre-tackle frames:", should_height_pretackle.size)

    # Get a mask for selecting which indices have reasonable confidence
    lshoulder_conf = kp[:, kp_index["left shoulder"], coords_index["conf"]]
    lshoulder_conf_pretackle = lshoulder_conf[:tackle_frame-1]
    lshoulder_conf_mask = lshoulder_conf_pretackle > 0.3
    #print("Confidence mask:", lshoulder_conf_mask)

    # Select shoulder-ankle differences which meet confidence threshold
    should_height_pretackle_filtered = should_height_pretackle[lshoulder_conf_mask]
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
    print("Start shoulder height:", round(max_should_height_pretackle, 3))
    print("Tackle shoulder height:", round(should_height_tackle, 3))
    print(f"Percent change in shoulder height: {round(should_percent_change, 2)}%")

    # Scoring percent in shoulder height change
    if(should_percent_change < 20):
        score = 0
    if(20 <= should_percent_change  < 40):
        score = 1
    if(40 <= should_percent_change < 50):
        score = 2
    if(should_percent_change >= 50):
        score = 3

    scores = {}
    scores["height"] = score
    scores["accel"] = 0
    scores["wrap"] = 0

    print("Scores:", scores)
    feedback = {0:"poor", 1:"fair", 2:"good", 3:"excellent"}
    print(f"Tackle height score: {score}/3, {feedback[score]}")
    print("------------------------------------------------------")

    return scores, length

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


if __name__ == '__main__':

    t0 = time.time()

    score(video_filepath='test.mp4', timestamp=2)

    total_time = round(time.time() - t0, 2)

    print("\n")
    print("------------------------------------------------------")
    print("Tackle scoring and pose estimation took", total_time, "seconds")
    print("------------------------------------------------------")
