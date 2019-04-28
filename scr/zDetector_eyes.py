import dlib
import numpy as np
import cv2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("tools\\shape_predictor_68_face_landmarks.dat")

def detector_eyes(img):
    # img = cv2.imread("images\\6.jpg")
    #使用detector进行人脸检测 rects为返回的结果
    rects = detector(img,1)
    if(rects):        
        #使用predictor进行人脸关键点识别
        landmarks = np.matrix([[p.x,p.y] for p in predictor(img,rects[0]).parts()])
        # img = img.copy()
        eyeList=[]
        #使用enumerate 函数遍历序列中的元素以及它们的下标
        for idx,point in enumerate(landmarks):
            pos = (point[0,0],point[0,1])
            eyeList.append(pos)
        return eyeList[36:48]       #返回左右眼共12个坐标
    else:
        return []

#test
img = cv2.imread("images\\6.jpg")
s = detector_eyes(img)
print(s)