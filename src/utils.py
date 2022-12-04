from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2 as cv
import pyttsx3


# 文章を一定の長さごとに改行していく関数
def cut_text(text):
    maximum_length = 23
    text = text.replace(' ', '')
    text = text.replace('　','')
    n = len(text)
    ret = ""
    index = 0
    last_index = 0
    while(True):
        if(n-index>maximum_length):
            index += maximum_length
            ret += text[last_index:index]
            last_index += maximum_length
        else:
            ret += text[last_index:]
            break
        ret += "\n"
    return ret


# 画像の上に日本語含む文字を重ねる関数
# font-face部分には、自分で用意したフォントデータのパスを入力する。
def put_text(img, text, point, font_scale, color, font_face='font/JK-Maru-Gothic-M.otf'):
    x, y = point
    imgPIL = Image.fromarray(img)
    draw = ImageDraw.Draw(imgPIL)
    fontPIL = ImageFont.truetype(font=font_face, size=font_scale)
    w, h = draw.textsize(text, font=fontPIL)
    draw.text(xy=(x,y), text=str(text), fill=color, font=fontPIL)
    return np.array(imgPIL, dtype=np.uint8)


# waitKey周りの関数
def break_key_setter(t):
    key = cv.waitKey(t)&0xFF
    if(key==ord('q') or key==ord('Q') or key==27):
        return True
    else:
        return False


# 文字を音声に合成して発話する関数
def text_to_speech_pyttsx3(ph):
    engine = pyttsx3.init()
    engine.setProperty("rate",100)
    engine.say(ph)
    engine.runAndWait()

