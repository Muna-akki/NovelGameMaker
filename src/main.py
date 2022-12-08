import sounddevice as sd

import createoutput as co
import capture
import face
import voice
import hand
import utils

def main():
    output_data = co.OutputImage()          # ノベルゲーム風の画像を合成
    cap_data = capture.CameraCapture()      # カメラからの入力を処理
    face_data = face.FaceDetection()        # 顔の位置・表情の認識
    voice_data = voice.VoiceRecognition()   # 音声処理
    hand_data = hand.HandDetection()        # 手の認識

    # 音声を取得
    with sd.RawInputStream(
        samplerate=voice_data.samplerate, 
        blocksize=8000, device=None, 
        dtype="int16", channels=1,
        callback=voice_data.callback
        ):
        print("Sound Input Opened")

        count = 0       # ループ回数 (mod 10)

        # 処理ループ
        while True:
            cap_data.update_image()                                         # カメラからの入力を次のフレームへ進める
            voice_data.get_message_data(output_data)                        # 音声認識結果を取得
            face_data.search_face(cap_data, output_data)                    # 画像から顔認識
            

            # 以下の処理は重たく、また全フレームでの処理が不要なのでcountが10になるごとに行う
            if count==10:
                count = 0             
                hand_data.execute_hand_detection(cap_data, output_data)     # 画像から手を認識                                  
                face_data.emotion_analyze(cap_data, output_data)            # 画像から表情を認識
            else:
                count += 1

            output_data.show_output()                                       # 画像を合成して表示                                     
            cap_data.show_input()                                           # 入力がどう認識されているかを表示

            if utils.break_key_setter(1) or voice_data.goodbye_checker():   # 終了判定
                break
    
    cap_data.release()      # OpenCVによるカメラ画像取得の終了



if __name__=="__main__":
    main()
