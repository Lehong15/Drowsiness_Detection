from cv2 import cv2  

cap = cv2.VideoCapture("car.MP4") #计算机自带的摄像头为0，外部设备为1

c=1 
if cap.isOpened(): #判断是否正常打开
    rval, image = cap.read()
else:
    rval = False
image_List = []
while rval:   #循环读取视频帧
    cap.set(cv2.CAP_PROP_POS_MSEC, 1 * 1000 * c)   #截取图片的方法  此处是0.5秒截取一个  可以改变参数设置截取间隔的时间
    rval, image = cap.read()
    image_List.append(image)
    # cv2.imwrite('E:\\save\\drowsy_driver\\result_image\\' + str(c) + '.jpg',image) #存储为图像
    # if c<255:
    # 	c = c + 1
    # else:
    # 	c = 1
    print(image_List)  	
cv2.waitKey(1)
cap.release()


