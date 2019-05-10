import os
import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
import time

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("..\\tools\\shape_predictor_68_face_landmarks.dat")

#特征点--眼睛坐标数据
def detector_eyes(img):
    #使用detector进行人脸检测 rects为返回的结果
    rects = detector(img,0)
    if(rects):        
        #使用predictor进行人脸关键点识别
        landmarks = np.matrix([[p.x,p.y] for p in predictor(img,rects[0]).parts()])
        eyeList=[]
        #使用enumerate 函数遍历序列中的元素以及它们的下标
        for idx,point in enumerate(landmarks):
            pos = (point[0,0],point[0,1])
            eyeList.append(pos)
        return eyeList[36:48]       #返回左右眼共12个坐标
    else:
        return []

#两特征点距离
def is_close(eye,threshold):
	# 计算两组垂直眼标之间的距离
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	# 计算水平眼标间的距离
	C = dist.euclidean(eye[0], eye[3])
	# 计算眼镜纵横比
	ear = (A + B) / (2.0 * C)
	# print(ear)
	if ear < threshold:
		return True

#闭眼判断
def close_count(eyes, threshold):
	count = 0
	for eye in eyes:
		right = eye[0:6]
		left = eye[6:12]
		
		if is_close(right,threshold) and is_close(left,threshold):
			count += 1
	return count

#deal images 以及 疲劳度计算
def deal(img_list):
	data_eyes = []
	time_fatigue = {}
	# i=1
	for imgfile in img_list:
		eyes_list = detector_eyes(imgfile)
		# print(i)
		# i=i+1
		if(eyes_list):
			data_eyes.append(eyes_list)
		# print(len(data_eyes))

	#判断闭眼睛图片数量n  
	close_eyes_num = close_count(data_eyes, 0.2)

	#疲劳度计算
	fatigue_flag=0
	fatigue = close_eyes_num/len(img_list)	
	
	now_time = time.strftime("%X",time.localtime())
	time_fatigue[now_time] = fatigue # 添加

	if fatigue < 0.3:
		fatigue_flag =0
	elif fatigue >= 0.3 and fatigue < 0.4:
		fatigue_flag = -1
	else:
		fatigue_flag = 1

	return fatigue_flag,time_fatigue


# #read images 可放至周家红
# def read_images():
# 	img_list = []
# 	for filename in os.listdir("..\\images\\"):
# 		img = cv2.imread("..\\images\\"+filename)
# 		img_list.append(img)
# 	print(len(img_list))
# 	return img_list

# if __name__ == '__main__':
# 	imgs = read_images()
# 	a,b=deal(imgs)
# 	print(a,b)
