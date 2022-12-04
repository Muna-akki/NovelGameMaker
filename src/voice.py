from vosk import Model, KaldiRecognizer
import queue
import json
import utils


# 音声を認識するクラス
class VoiceRecognition():
    def __init__(self):
        self.samplerate = 44100
        self.model = Model(lang="ja")
        self.q = queue.Queue()
        self.rec = KaldiRecognizer(self.model, self.samplerate)
        self.translate_flag = False
        self.message = ""
        print("VoiceRecognition Initialization Finished")


    # オーディオのコールバック関数
    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        # if status:
        #     print(status, file=sys.stderr)
        self.q.put(bytes(indata))
    

    # 音声認識の結果を取得する
    def get_message_data(self, output_data):
        data = self.q.get()
        self.translate_flag = self.rec.AcceptWaveform(data)
        if(self.translate_flag):
            json_dict = json.loads(self.rec.Result())
            self.message = utils.cut_text(json_dict["text"])
        else:
            json_dict = json.loads(self.rec.PartialResult())
            self.message = utils.cut_text(json_dict["partial"])
        output_data.update_message(self.message)
    

    # 音声による終了判定
    def goodbye_checker(self):
        if not self.translate_flag:
            return False
        if self.message=="さようなら" or self.message=="さよなら":
            #utils.break_key_setter(500)
            goodbye = "バイバイ。またね。"
            utils.text_to_speech_pyttsx3(goodbye)
            return True
    
    

