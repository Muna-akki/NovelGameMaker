import cv2 as cv
import numpy as np
import utils


# カメラからの入力等を行うクラス
class CameraCapture():
    def __init__(self):
        self.FRAME_WIDTH = 640          # カメラ画像の高さ
        self.FRAME_HEIGHT = 480         # カメラ画像の幅
        self.FRAME_RATE = 30            # カメラのフレームレート
        self.scale = 4.0                # 画像処理に使う画像の縮小率
        self.cap = self.capture_setter()
        self.smallImg = np.empty((int(self.FRAME_HEIGHT/self.scale), int(self.FRAME_WIDTH/self.scale)))
        self.ret, self.input_frame = self.cap.read()
        if not self.ret:
            print("Error: cannot get input_frame")
            exit(0)
        self.gray = np.empty_like(self.input_frame)
        self.smallImg_colored = cv.resize(self.input_frame, (self.smallImg.shape[1],self.smallImg.shape[0]), 0, 0, cv.INTER_LINEAR)
        self.input_window_name = "Input"
        print("CameraCapture Initialization Finished")


    # capの解放とwindowの削除
    def release(self):
        self.cap.release()
        cv.destroyAllWindows()


    # VideoCaptureを設定する関数
    def capture_setter(self):
        cap = cv.VideoCapture(0)
        if(not cap.set(cv.CAP_PROP_FPS, self.FRAME_RATE)):
            print("Error: cannot set frame rate")
        if(not cap.set(cv.CAP_PROP_FRAME_WIDTH, self.FRAME_WIDTH)):
            print("Error: cannot set frame width")
        if(not cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.FRAME_HEIGHT)):
            print("Error: cannot set frame height")
        if(not cap.isOpened()):
            print("Error: Cannot open the video\n")
            exit(0)
        if(abs(cap.get(cv.CAP_PROP_FPS)-self.FRAME_RATE)>0.1):
            print("Warning: invalid value -> FPS")
        return cap

    
    # 検出の前処理
    def update_image(self):
        self.ret, self.input_frame = self.cap.read()
        self.gray = cv.cvtColor(self.input_frame, cv.COLOR_BGR2GRAY)
        self.smallImg = cv.resize(self.gray, (self.smallImg.shape[1],self.smallImg.shape[0]), 0, 0, cv.INTER_LINEAR)
        self.smallImg = cv.equalizeHist(self.smallImg)
        self.smallImg_colored = cv.resize(self.input_frame, (self.smallImg.shape[1],self.smallImg.shape[0]), 0, 0, cv.INTER_LINEAR)
    

    # 画像の上に(物体認識結果の)正方形を表示する関数
    def input_add_rect(self, center, radius, color):
        pt1 = (center[0]-radius, center[1]-radius)
        pt2 = (center[0]+radius, center[1]+radius)
        self.input_frame = cv.rectangle(self.input_frame, pt1, pt2, color,1)


    # 画像に文字を重ねる関数
    def input_add_text(self, text, point, size, color):
        self.input_frame = utils.put_text(self.input_frame, text, point, size, color)
    

    # 入力画像がどう認識されているかを表示
    def show_input(self):
        cv.imshow(self.input_window_name, self.input_frame)




