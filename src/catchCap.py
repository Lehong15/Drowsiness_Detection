from cv2 import cv2  
import Fatigue_Detection as FD
import time
import driving_overtime as do
import warning as w 

rval = True
time_fatigue = {}
datetime = time.strftime("%Y-%m-%d",time.localtime())
time_fatigue['datetime'] = datetime # 添加
# print(time.strftime("%X",time.localtime()))

def Read_Video():
	global rval
	cap = cv2.VideoCapture(0) #计算机自带的摄像头为0，外部设备为1
	c=1 
	if cap.isOpened(): #判断是否正常打开
	    rval, image = cap.read()
	else:
	    rval = False
	image_List = []
	while rval:   #循环读取视频帧
		for i in range(0,25):	
			timeF=10
			rval, image = cap.read()
			if(c%timeF == 0): #每隔timeF帧进行存储操作 
				image_List.append(image)
			c = c + 1
			print(c)
			
			#cv2.imwrite('E:\\save\\drowsy_driver\\result_image\\' + str(len(image_List)) + '.jpg',image) #存储为图像
		
		
		if len(image_List) == 25:
			b = image_List[0]
			if do.driving(b):
				w.warning(b)
			
			fatigue_flag,f = FD.deal(image_List)
			change_timedictiondry(f)
			print(fatigue_flag)
			#陈浩返回该驾驶员未超时的bollen值
			#判断是否报警fatigue_flag
			
			image_List = []
				
		# cv2.imshow("Vshow",image)
		if cv2.waitKey(1) & 0xFF == ord('q'):#若检测到按键 ‘q’，退出
			break
	cap.release()

def change_timedictiondry(a):
	time_fatigue.update(a)
	print(time_fatigue)

def change_rval():
	rval = not rval


if __name__ == "__main__":
	Read_Video()
