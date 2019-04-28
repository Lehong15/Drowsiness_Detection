from cv2 import cv2  
import Fatigue_Detection as FD

def Read_Video():
	cap = cv2.VideoCapture(0) #计算机自带的摄像头为0，外部设备为1
	c=1 
	if cap.isOpened(): #判断是否正常打开
	    rval, image = cap.read()
	else:
	    rval = False
	image_List = []
	while rval:   #循环读取视频帧
	    cap.set(cv2.CAP_PROP_POS_MSEC, 0.4 * 1000 * c) #截取图片 此处是0.2秒截取一个 可以改变参数设置截取间隔的时间
	    rval, image = cap.read()
	    image_List.append(image)
	    cv2.imwrite('E:\\save\\drowsy_driver\\result_image\\' + str(len(image_List)) + '.jpg',image) #存储为图像
	    if len(image_List) == 25:
	    	eyes,fatigue,fatigue_flag = FD.deal(image_List)
	    	print(fatigue,fatigue_flag)

	    	#判断是否报警fatigue_flag
	    	pass
	    	#把当前疲劳度反馈到界面
	    	pass

	    	image_List = []

	    cv2.imshow("Vshow",image)
	    if cv2.waitKey(1) & 0xFF == ord('q'):#若检测到按键 ‘q’，退出
	        break
	cap.release()


Read_Video()

