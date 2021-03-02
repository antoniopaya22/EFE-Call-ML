import math
import cv2

count = 0

def convert_video_to_frames(video_file, model_name, name="frame", frame_rate_value=5):
    count = 0
    cap = cv2.VideoCapture(video_file)  # capturing the video from the given path
    frame_rate = cap.get(frame_rate_value)  # frame rate
    subfolder_name = model_name + "_frames"
    if name == "frame":
        subfolder_name = subfolder_name + "/training"
    else:
        subfolder_name = subfolder_name + "/test"

    while cap.isOpened():
        frame_id = cap.get(1)  # current frame number
        ret, frame = cap.read()
        if ret is not True:
            break
        if frame_id % math.floor(frame_rate) == 0:
            filename = f'data/frames/{subfolder_name}/{name}{count}.jpg'
            count += 1
            cv2.imwrite(filename, frame)
    cap.release()



def convert_video_to_frames_and_crop(video_file, model_name, name="frame", frame_rate_value=5):
    global count
    # count = 0
    cap = cv2.VideoCapture(video_file)  # capturing the video from the given path
    frame_rate = cap.get(frame_rate_value)  # frame rate
    subfolder_name = model_name + "_frames"
    if name == "frame":
        subfolder_name = subfolder_name + "/training"
    else:
        subfolder_name = subfolder_name + "/test"
    # x,y,h,w = 0,980,1080,1920 # resolution 1920x980
    x,y,h,w = 0,642,720,1280 # resolution 1280x720
    while cap.isOpened():
        frame_id = cap.get(1)  # current frame number
        ret, frame = cap.read()
        if ret is not True:
            break
        if frame_id % math.floor(frame_rate) == 0:
            filename = f'data/frames/{subfolder_name}/{name}{count}.jpg'
            count += 1
            crop_frame = frame[y:y+h, x:x+w]
            cv2.imwrite(filename, crop_frame)
    cap.release()
