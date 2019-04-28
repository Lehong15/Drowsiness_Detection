import dlib
import cv2

predictor_path = "shape_predictor_68_face_landmarks.dat"

class Decorator():
    def __init__(self):        
        self.predictor = dlib.shape_predictor(predictor_path)
        self.detector = dlib.get_frontal_face_detector()


    def on_glass(face):
        # img = cv2.imread(face)
        rect = detector(face, 0)
        landmarks = np.matrix([[p.x, p.y] for p in predictor(img,rect).parts()])
        for idx, point in enumerate(landmarks):
            pos = (point[0, 0], point[0, 1])
            print(idx,pos)


            # 利用cv2.circle给每个特征点画一个圈，共68个
            cv2.circle(img, pos, 5, color=(0, 255, 0))
            # 利用cv2.putText输出1-68
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(idx+1), pos, font, 0.8, (0, 0, 255), 1,cv2.LINE_AA)

            cv2.namedWindow("img", 2)
            cv2.imshow("img", img)
            cv2.waitKey(0)
    

        return face