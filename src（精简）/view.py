from tkinter import *
from tkinter.messagebox import *
from dateutil import rrule
from datetime import datetime
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler 
from matplotlib.figure import Figure 
import threading
import cv2  
import Fatigue_Detection as FD
import driving_overtime as do
import warning as w 
import numpy as np


#View页面。实际上是最主要的部分。里面用类详细定义了每一个页面的元素，控件与摆放。
#其中，主界面涉及到的变量如下：self.on_hit:为False，驾驶行为未开始，点击按钮开始；为True，驾驶行为开始，点击按钮结束。
#重点：时间；页面和数据刷新；折线图放置


rval = True
time_fatigue = {}
datetime1 = datetime.now().strftime('%H:%M:%S')  
time_fatigue['datetime'] = datetime1 

pilao=0.20
time_now=datetime.now().strftime('%H:%M:%S')
time_start=datetime.now().strftime('%H:%M:%S')
time_jiashi=datetime.now().strftime('%H:%M:%S')
time_now_c=datetime.now()
time_start_c=datetime.now()
time_jiashi_c=datetime.now()
time_zuichang=90
color='green'
zhuangtai=0
xingwei='正常'
on_hit = False 
zhanghao='admin'
mima='admin'
yonghuming='司机'
zhishu=str(pilao)
pilao_list=[0]
x_list=[0]
iii=0

#数据部分，其中以上均为全局变量，在方法中要使用global关键词进行更改

class InputFrame(Frame): # 继承Frame类 
 def __init__(self, master=None): 
  Frame.__init__(self, master) 
  self.root = master #定义内部变量root 
  self.itemName = StringVar() 
  self.kaishi=StringVar()
  self.createPage() 
  self.kaishi.set('开始驾驶')
 
 

  
 def createPage(self): 

 
  l=Label(self, text="警戒颜色", bg=color, font=("Arial",35))
  l.pack(padx=0,pady=0)
  
  var_time_now=StringVar()
  var_time_jiashi=StringVar()
  var_zhishu=StringVar()
  var_xingwei=StringVar()


  def change_timedictiondry(a):
    time_fatigue.update(a)
    # print(time_fatigue)


  def Read_Video():
    global rval,pilao,zhishu,pilao_list,x_list,iii
    cap = cv2.VideoCapture(0) #计算机自带的摄像头为0，外部设备为1
    c=1 
    if cap.isOpened(): #判断是否正常打开
        rval, image = cap.read()
    else:
        rval = False
    image_List = []
    while rval:   #循环读取视频帧
      for i in range(0,20): 
        timeF=4
        rval, image = cap.read()
        if(c%timeF == 0): #每隔timeF帧进行存储操作 
          image_List.append(image)
        c = c + 1
        # print(c)
        
        #cv2.imwrite('E:\\save\\drowsy_driver\\result_image\\' + str(len(image_List)) + '.jpg',image) #存储为图像
      
      
      if len(image_List) == 20:
        b = image_List[0]
        if do.driving(b):
          w.warning(1)
       
        fatigue_flag,f,pilao = FD.deal(image_List)
        change_timedictiondry(f)

        pilao_list.append(pilao)
        
        zhishu=str(pilao)

        print("当前疲劳值为："+zhishu)

        print(pilao_list)
        zhishu_c=str(10*pilao)
        #陈浩返回该驾驶员未超时的bollen值
        #判断是否报警fatigue_flag
        if (fatigue_flag == 1):
          w.warning(3)
        elif (fatigue_flag == -1):
          w.warning(2)
        else:
          pass
        
        image_List = []
          
      # cv2.imshow("Vshow",image)
      if cv2.waitKey(1) & 0xFF == ord('q'):#若检测到按键 ‘q’，退出
        break
    cap.release()
    

  def hit_me():
    
    global on_hit,time_start,time_start_c,color,i
    if on_hit == False:     # 从 False 状态变成 True 状态
        on_hit = True
        self.kaishi.set('结束驾驶')   # 设置标签的文字为 'you hit me'
       
        rval=True
        Read_Video()
    else:       # 从 True 状态变成 False 状态
        on_hit = False
        self.kaishi.set('开始驾驶')
        

  def thread_it(func, *args):
    global on_hit
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    
    t.setDaemon(True) 
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()

  def refresh_data():
     # 需要刷新数据的操作
     # 代码...
     global time_now,time_now_c,time_jiashi,time_jiashi_c,time_start_c,on_hit,color,i,i_list,zhishu,pilao
     time_now_c = datetime.now()
     time_now = datetime.now().strftime('%H:%M:%S')  
     if on_hit==True:
       time_jiashi_c=(time_now_c - time_start_c).seconds
     elif on_hit==False:
       time_jiashi_c=0
      
     time_jiashi=str(time_jiashi_c)
     #将两个STR变量的值加上‘当前/驾驶+时间’，赋予相应的var_
     var_time_now.set('当前时间：'+time_now)
     var_time_jiashi.set('驾驶时间：'+time_jiashi)
     if time_jiashi_c>=time_zuichang:
        color='red'
        l.configure(bg=color)
        var_xingwei.set('推荐行为：立刻休息')
     if pilao<0.3 and time_jiashi_c< time_zuichang:
        color='green'
        l.configure(bg=color)
        var_xingwei.set('推荐行为：正常驾驶')
     if pilao>=0.3 and pilao<=0.4 and time_jiashi_c< time_zuichang:
        color='yellow'
        l.configure(bg=color)
        var_xingwei.set('推荐行为：注意休息')
     if pilao>0.4 and time_jiashi_c<time_zuichang:
        color='red'
        l.configure(bg=color)
        var_xingwei.set('推荐行为：立刻休息')
     
     var_zhishu.set('疲劳指数：'+zhishu)
     self.after(1000, refresh_data)   
  
  refresh_data()

  Button(self, textvariable= self.kaishi,font=('Arial',14),width=8, height=2, command=lambda: thread_it(hit_me)).pack(padx=5,pady=10)      # 点击按钮式执行的命令

  frm_1 = Frame(self)
  frm_3 = Frame(self)

  frm_1.pack(side='left')
  frm_3.pack(side='right')

 
  
  #使用变量来给text赋值，以来实现变量的实时刷新
  Label(frm_1, textvariable=var_zhishu, font=('Arial',12)).pack(padx=40,pady=15)
  Label(frm_1, textvariable=var_time_now,font=('Arial',12)).pack(padx=40,pady=15)
  Label(frm_3, textvariable=var_time_jiashi ,font=('Arial',12)).pack(padx=40,pady=15)
  Label(frm_3, textvariable=var_xingwei,font=('Arial',12)).pack(padx=40,pady=15)

  def yanse():
    if on_hit==False:
      color='green'
      l.configure(bg=color)
    self.after(1000,yanse)
  yanse()

  
class QueryFrame(Frame): # 继承Frame类 
 def __init__(self, master=None): 
  Frame.__init__(self, master) 
  self.root = master #定义内部变量root 
  self.itemName = StringVar() 
  self.createPage() 
  
 def createPage(self): 
  def hit_me_again():
    global mosttime,time_zuichang
    mosttime=e.get()
    time_zuichang=int(mosttime)
    var33.set('最长驾驶时间为：'+mosttime+'秒')

  global mosttime,time_zuichang
  var33=StringVar()
  mosttime=str(time_zuichang)
  var33.set('最长驾驶时间为：'+mosttime+'秒')
  Label().pack(pady=10)
  Label(self, textvariable=var33, font=("Arial",10)).pack(pady=2)
  Label(self, text= '更新时间为：', font=("Arial",10)).pack(pady=2)
  e=Entry(self)
  e.pack()
  
  Label(self).pack(pady=10)
  
  Button(self, text= '确定',font=('Arial',12),width=6, height=2,command =hit_me_again).pack(padx=5,pady=20)      # 点击按钮式执行的命令
 
    
  
 
  #Label(self, text= mosttime +'小时' , font=("Arial",16)).grid(row=1, column=1, stick=E)
class CountFrame(Frame): # 继承Frame类 
 def __init__(self, master=None): 
  Frame.__init__(self, master) 
  self.root = master #定义内部变量root 
  self.createPage() 
  
   
 def createPage(self): 
  var44=StringVar()
  
  def hit_me_again_twice():
    global yonghuming,mima
    yonghuming=e1.get()
    mima=e2.get()
    var44.set('驾驶人姓名为：'+yonghuming)
    f = open("zhanghao.txt","r")

  var44.set('驾驶人姓名为：'+yonghuming)
  Label(self, textvariable=var44, font=("Arial",10)).pack(pady=10)
  Label(self, text= '更改注册驾驶人为：', font=("Arial",10)).pack(pady=10)
  e1=Entry(self)
  e1.pack()
  Label(self, text= '更改密码：', font=("Arial",10)).pack(pady=10)
  e2=Entry(self)
  e2.pack()
  Button(self, text= '确定',font=('Arial',12),width=6, height=2,command =hit_me_again_twice).pack(padx=5,pady=20)      # 点击按钮式执行的命令
class AboutFrame(Frame): # 继承Frame类 
 def __init__(self, master=None): 
  Frame.__init__(self, master) 
  self.root = master #定义内部变量root 
  self.createPage() 
  
 def createPage(self): 
  Label(self, text='制作小组信息', font=("Arial",12)).grid(row=0, stick=N, pady=5) 
  Label(self, text='疲劳检测组长：李二红', font=("Arial",10)).grid(row=1, stick=W, pady=5) 
  Label(self, text='疲劳算法设计：陈浩', font=("Arial",10)).grid(row=2, stick=W, pady=5) 
  Label(self, text='图像提取处理：周家宏', font=("Arial",10)).grid(row=3, stick=W, pady=5) 
  Label(self, text='界面设计制作：黄翔宇', font=("Arial",10)).grid(row=4, stick=W, pady=5) 
  Label(self, text='报警机制设计：张丁旗', font=("Arial",10)).grid(row=5, stick=W, pady=5) 
  
