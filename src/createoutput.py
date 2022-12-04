import cv2 as cv
import numpy as np
import utils


# ノベルゲーム風の画面を作成するクラス
class OutputImage():
    # 各種定数
    GIRL_UNIFORM_0 = 0
    GIRL_UNIFORM_1 = 1
    CLASSROOM_NOON          = 0
    CLASSROOM_RAINY         = 1
    CLASSROOM_RAINY_LIGHTED = 2
    CLASSROOM_EVENING       = 3
    CLASSROOM_NIGHT_LIGHTED = 4
    CLASSROOM_NIGHT         = 5
    EMOTION_LIST = {
        "angry":0,      # 怒り
        "disgust":1,    # 嫌悪
        "fear":2,       # 恐怖
        "happy":3,      # 幸せ
        "sad":4,        # 悲しみ
        "surprise":5,   # 驚き
        "neutral":6     # 中立
    }
    NAME_LIST = {
        GIRL_UNIFORM_0:"みさき",
        GIRL_UNIFORM_1:"かなで",
    }
    CHARACTER_FILENAME_LIST = [
        [   # girl_uniform0                             　一人目のキャラクターの
            "img/humans/girl_uniform0/annoyed.png",     # 怒り顔の画像のパス
            "img/humans/girl_uniform0/sleepy.png",      # 嫌悪
            "img/humans/girl_uniform0/anxious.png",     # 恐怖
            "img/humans/girl_uniform0/smile.png",       # 幸せ
            "img/humans/girl_uniform0/anxious.png",     # 悲しみ
            "img/humans/girl_uniform0/shocked.png",     # 驚き
            "img/humans/girl_uniform0/normal.png",      # 中立
        ],
        [   # girl_uniform1                             二人目のキャラクターの
            "img/humans/girl_uniform1/annoyed.png",     # 怒り顔の画像のパス
            "img/humans/girl_uniform1/ridicule.png",    # 嫌悪
            "img/humans/girl_uniform1/fear.png",        # 恐怖
            "img/humans/girl_uniform1/smile.png",       # 幸せ
            "img/humans/girl_uniform1/tired.png",       # 悲しみ
            "img/humans/girl_uniform1/shocked.png",     # 驚き
            "img/humans/girl_uniform1/normal.png",      # 中立
        ]
    ]
    BACKGROUND_FILENAME_LIST = [                        # 背景画像のパスのリスト
        "img/background/classroom_noon.jpg",            # 背景1
        "img/background/classroom_rainy.jpg",           # 背景2
        "img/background/classroom_rainy_lighted.jpg",
        "img/background/classroom_evening.jpg",
        "img/background/classroom_night.jpg",
        "img/background/classroom_night_lighted.jpg",
    ]
    
    
    def __init__(self):
        self.character_list = self.character_setter()
        self.background_list = self.background_setter()
        self.textbox = self.textbox_setter()
        self.who = self.GIRL_UNIFORM_1
        self.how = "neutral"
        self.when = self.CLASSROOM_NOON
        self.background = None
        self.update_background()
        self.character = None
        self.character_name = None
        self.update_character()
        self.x_center = self.background.shape[1]*5/10-self.character.shape[1]/2
        self.x_left = self.background.shape[1]*3/10-self.character.shape[1]/2
        self.x_right = self.background.shape[1]*7/10-self.character.shape[1]/2
        self.p_x = self.x_center
        self.p_y = self.background.shape[0]-self.character.shape[0]
        self.message = "おはよう！調子はどう？" 
        self.output_window_name = "Output"
        self.output_frame = None
        print("OutputImage Initialization Finished")


    # キャラクターの画像を縦600px横400pxに揃える
    def cut_img(self, img):
        h,w = img.shape[:2]
        if(h==600 and w==400):
            return img
        scale = 600/h
        new_width = int(w*scale)
        img = cv.resize(img, (new_width, 600), 0, 0, interpolation=cv.INTER_LANCZOS4)
        if(new_width>=400):
            center = int(new_width//2)
            start = center-199
            goal = center+201
            img = img[:,start:goal,:]
        return img
    

    # PNG画像を重ねる関数(透過込みで)
    def add_png(self, src, dst, point):
        if(src.shape[2]!=4):
            print("Error: this src is not .png\n")
            exit(0)
        if(src.shape[1]+point[0]>dst.shape[1] or src.shape[0]+point[1]>dst.shape[0]):
            print("Error: area over\n")
            exit(0)
        rgb = src[:,:,0:3]
        mask = src[:,:,3]
        dst = np.array(dst, dtype=np.float64)
        y_from = int(point[1])
        y_to = int(point[1]+src.shape[0])
        x_from = int(point[0])
        x_to = int(point[0]+src.shape[1])
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        mask = mask/255
        if(dst.shape[2]==3):
            dst[y_from:y_to, x_from:x_to] *= 1-mask
            dst[y_from:y_to, x_from:x_to] += rgb*mask
        else:
            dst_jpg = self.add_png(src,dst[:,:,0:3],point)
            dst[y_from:y_to, x_from:x_to,3] = [[max(dst[y_from+i,x_from+j,3], src[i,j,3]) for j in range(len(src[0]))] for i in range(len(src))]
            dst[:,:,0:3] = dst_jpg
        dst = np.array(dst, dtype=np.uint8)
        return dst


    # キャラクター画像を読み込む
    def character_setter(self):
        character_list = []
        for i in range(len(self.CHARACTER_FILENAME_LIST)):
            character = []
            for j in range(len(self.CHARACTER_FILENAME_LIST[i])):
                img = cv.imread(self.CHARACTER_FILENAME_LIST[i][j], -1) # 画像の読み込み
                img = self.cut_img(img) # 人画像のサイズが横400、縦600となるように調整
                h,w = img.shape[:2]
                size = 1.2
                width = int(w*size)
                height = int(h*size)
                img = cv.resize(img,(width, height), 0, 0, interpolation=cv.INTER_LANCZOS4)
                character.append(img)
            character_list.append(character)
        return np.array(character_list)
    

    # 背景画像を読み込む
    def background_setter(self):
        background_list = []
        for i in range(len(self.BACKGROUND_FILENAME_LIST)):
            background_list.append(cv.imread(self.BACKGROUND_FILENAME_LIST[i], -1))
        return np.array(background_list)
    

    # テキストボックス画像を読み込む
    def textbox_setter(self):
        parent_filename = "img/Messageframe_31/material/"
        color_filename = "01_red"
        textbox_filename = parent_filename+color_filename+"/01_messageframe/message_1280.png"
        textbox = cv.imread(textbox_filename,-1)
        systembutton_foldername = parent_filename+color_filename+"/02_systembutton/"
        button_list = ["title", "config", "menu", "skip", "auto", "log", "load", "save"]
        p_x = 1200
        p_y = 30
        dp_x = 60
        for name in button_list:
            systembutton_filename = systembutton_foldername+name+".png"
            button = cv.imread(systembutton_filename,-1)
            textbox = self.add_png(button, textbox, (p_x, p_y))
            p_x -= dp_x
        return textbox


    # キャラクターの更新
    def update_character(self):
        self.character = self.character_list[self.who][self.EMOTION_LIST[self.how]]
        self.character_name = self.NAME_LIST[self.who]

    # 背景の更新
    def update_background(self):
        self.background = self.background_list[self.when]
    

    # 時間帯の更新
    def update_when(self, finger):
        self.when = finger%6


    # キャラクターの位置の更新
    def update_x(self, detected_x, input_frame_width):
        if detected_x>input_frame_width*2/3:
            self.p_x = self.x_right
            return 
        elif detected_x>input_frame_width/3:
            self.p_x = self.x_center
            return 
        else:
            self.p_x = self.x_left
            return
        
    
    # キャラクターの変更
    def update_who(self, flag):
        if not flag:
            return
        if self.who==self.GIRL_UNIFORM_0:
            self.who = self.GIRL_UNIFORM_1
        else:
            self.who = self.GIRL_UNIFORM_0


    # キャラクターの表情の更新
    def update_how(self, how):
        self.how = how
    

    # 台詞の更新
    def update_message(self, message):
        self.message = message


    # 出力画像を作成
    def integrate_output(self):
        self.update_background()
        self.update_character()
        self.output_frame = self.add_png(self.character, self.background, (self.p_x, self.p_y))
        self.output_frame = self.add_png(self.textbox, self.output_frame, (0, self.output_frame.shape[0]-self.textbox.shape[0]))
        self.output_frame = utils.put_text(img=self.output_frame, text=self.character_name, point=(170, 535), font_scale=30, color=(255, 255, 255))
        self.output_frame = utils.put_text(img=self.output_frame, text=self.message, point=(200, 580), font_scale=40, color=(0, 0, 0))


    # 出力画像の表示
    def show_output(self):
        self.integrate_output()
        cv.imshow(self.output_window_name, self.output_frame)








