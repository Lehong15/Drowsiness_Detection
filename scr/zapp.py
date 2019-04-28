import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

from A import Decorator


class App():
    def __init__(self, root=None):
        self.root = root
                
        lb = tk.Label(root,
                      text='test',  # 标签的文字
                      font=18,  # 字体和字体大小
                      width=10, height=3  # 标签长宽
                      )
        lb.pack()               # 固定窗口位置

        btn3 = tk.Button(root, text='测试',
                         bg='blue',
                         font=18,
                         width=15, height=3,
                         command=self.add_glass
                         )
        btn3.pack()
        self.face = cv2.imread("1.jpg")

    def add_glass(self):
        # python是传引用（对象）的，所以不能face直接作为参数，会改变原来的图像，导致第二次戴眼镜的时候眼镜重叠了
        res = Decorator().on_glass(self.face)
        cv2.imshow("results", res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    root = tk.Tk('test')
    root.geometry('400x300')
    app = App(root)
    try:
        app.root.mainloop()
    except Exception() as e:
        print(e)
