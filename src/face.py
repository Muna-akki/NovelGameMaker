import cv2 as cv
from deepface import DeepFace


# 画像から顔の位置と表情を認識するクラス
class FaceDetection():
    def __init__(self):
        # cascade_setterの引数は、自分で用意したhaarcascadeの正面顔認識モデルを入力する。
        self.cascade_frontalface = self.cascade_setter("model/haarcascade_frontalface_alt.xml")
        self.faces = None
        self.dominant_emotion = 'neutral'
        print("FaceDetection Initialization Finished")


    # haarカスケード分類器の設定
    def cascade_setter(self,cascade_name):
        cascade = cv.CascadeClassifier(cascade_name)
        if(cascade==None):
            print("Error: cascadeFile not found\n")
            exit(0)
        return cascade
    

    # 顔の位置を探索
    def search_face(self, cap_data, output_data):
        self.faces = self.cascade_frontalface.detectMultiScale(cap_data.smallImg, 1.1, 2, cv.CASCADE_SCALE_IMAGE, (20,20))
        for i in range(len(self.faces)):
            center, radius = self.detected_face_setter(cap_data.scale, i)
            cap_data.input_add_rect(center, radius, (0, 255, 0, 0))
            cap_data.input_add_text(self.dominant_emotion, center, 20, (255, 0, 0, 0))
            output_data.update_x(center[0], cap_data.input_frame.shape[0])


    # 縮小画像から検出された顔の座標を、元画像の座標に変換
    def detected_face_setter(self, scale, i):
        x = int((self.faces[i][0]+self.faces[i][2]*0.5)*scale)
        y = int((self.faces[i][1]+self.faces[i][3]*0.5)*scale)
        radius = int((self.faces[i][2]+self.faces[i][3])*0.25*scale)
        center = (x,y)
        return center, radius
    

    # 画像に映る顔から表情を検出
    def emotion_analyze(self, cap_data, output_data):
        try:
            result_emotion = DeepFace.analyze(cap_data.smallImg_colored, actions=['emotion'])
            self.dominant_emotion = result_emotion['dominant_emotion']
            output_data.update_how(self.dominant_emotion)
        except Exception as e:
            pass
