import os
import cv2
import dlib
import numpy as np
import Detector_PERCLOS

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("..\\tools\\shape_predictor_68_face_landmarks.dat")

#read images 可放至周家红
def read_images():
	img_list = []
	for filename in os.listdir("..\\images\\"):
		img = cv2.imread("..\\images\\"+filename)
		img_list.append(img)
	return img_list

#特征点--眼睛坐标数据
def detector_eyes(img):
    # img = cv2.imread("6.jpg")
    #使用detector进行人脸检测 rects为返回的结果
    rects = detector(img,0)
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

#deal images 以及 疲劳度计算
def deal(img_list):
	data_eyes = []
	for imgfile in img_list:
		eyes_list = detector_eyes(imgfile)
		if(eyes_list):
			data_eyes.append(eyes_list)

	#判断闭眼睛图片数量n    #陈浩
	close_eyes_num = Detector_PERCLOS.close_count(data_eyes, 0.2)
	# print(close_eyes_num)

	#疲劳度计算
	fatigue = close_eyes_num/len(img_list)
	fatigue_flag=0

	if fatigue < 0.3:
		fatigue_flag =0
	elif fatigue >= 0.3 and fatigue < 0.4:
		fatigue_flag = -1
	else:
		fatigue_flag = 1

	# print(data_eyes,fatigue,fatigue_flag,len(img_list))
	return data_eyes,fatigue,fatigue_flag



if __name__ == '__main__':
	imgs = read_images()
	c,a,b=deal(imgs)
	print(a,b)
