import Fatigue_Detection as FD
import os
import cv2
import time

time_fatigue = {}
datetime = time.strftime("%Y-%m-%d",time.localtime())
time_fatigue['datetime'] = datetime # 添加
# print(time.strftime("%X",time.localtime()))

def change_timedictiondry(a):
	time_fatigue.update(a)
	# print(time_fatigue)


#read images 可放至周家红
def read_images():
	img_list = []
	for filename in os.listdir("..\\images\\"):
		img = cv2.imread("..\\images\\"+filename)
		img_list.append(img)
	return img_list

if __name__ == '__main__':
	imgs = read_images()
	a,b=FD.deal(imgs)
	print(a,b)
	change_timedictiondry(b)