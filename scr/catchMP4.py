from cv2 import cv2  

cap = cv2.VideoCapture(0) #计算机自带的摄像头为0，外部设备为1
d=1
timeE=3

if cap.isOpened(): #判断是否正常打开
    rval, frame = cap.read()
else:
    rval = False
frame_List = []
while rval:   #循环读取视频帧
    frame_List.append(frame)
    rval, frame = cap.read()
        if(d% timeE == 0): #每隔timeE帧进行存储操作
            cv2.imwrite('D:/cppfile/opencv_file/opencv_face/images/'+str(d) + '.jpg',frame) #存储为图像
        d = d + 1 
    # cv2.imwrite('E:\\save\\drowsy_driver\\result_image\\' + str(c) + '.jpg',image) #存储为图像
    # if c<255:
    # 	c = c + 1
    # else:
    # 	c = 1
    print(image_List)  	
cv2.waitKey(1)
cap.release()
