import time
import threading
import face_recognition
import cv2
import numpy as np

driving_start = time.time()
previous_img = np.array([])


def is_similar(img1, img2):
    faces1 = face_recognition.face_encodings(img1)
    faces2 = face_recognition.face_encodings(img2)
    if len(faces1)==0 or len(faces2)==0: #如果没有检测到人脸，返回相似
        return True
    results = face_recognition.compare_faces([faces1[0]], faces2[0])
    return results[0]

def change_driver(new_img):
    global previous_img
    if previous_img.size == 0:
        previous_img = new_img
        return True
    elif is_similar(previous_img, new_img):
        return False
    else:
        previous_img = new_img
        return True

def driving(img):
    global driving_start
    # print("start:", driving_start)
    if change_driver(img):
        driving_start = time.time()
        # print("yigengxin")
        # print("start:", driving_start)
    else:
        # print("now:",time.time())
        # atime = 60
        atime = 14400     #4h
        if((time.time()-driving_start) > atime):
            # print("驾驶时间超过60s")
            return True


