# NovelGameMaker

## 使用方法
素材・モデルの用意

まずは、画像素材を用意する。README.mdの末尾のクレジットに記載しているようなサイトからでも良いし、自作でも良い。ただし、.pngか.jpgかの違いや画像サイズでエラーを吐くことがある。背景は小さすぎないように。
フォルダ構成は例えば以下のようにし、createoutput.pyのOutputImageクラス内冒頭で宣言されている定数やtextbox_setter()に適切にパスを記述する。

imgフォルダ
<ul>
    <li>
        background
        <ul>
            <li>背景素材1</li>
            <li>背景素材2</li>
            <li>(以下略)</li>
        </ul>
    </li>
    <li>
        humans
        <ul>
            <li>
                human_0
                <ul>
                    <li>人0表情0</li>
                    <li>人0表情1</li>
                    <li>(以下略)</li>
                </ul>
            </li>
            <li>
                human_1
                <ul>
                    <li>人1表情0</li>
                    <li>人1表情1</li>
                    <li>(以下略)</li>
                </ul>
            </li> 
        </ul>
    </li>
    <li>
        Messageframe
        <ul>
            <li>
                messageframe
                <ul>
                    <li>メッセージウインドウ素材</li>
                </ul>
            </li>
            <li>
                systembuttom
                <ul>
                    <li>システムボタン素材0</li>
                    <li>システムボタン素材1</li>
                    <li>(以下略)</li>
                </ul>
            </li>
        </ul>
    </li>
</ul>

<br>
<br>
次に、フォントデータを用意する。これもクレジットに記載したようなフリーフォントでも良いし、PCの中のフォントデータをコピーしてきても良い。fontフォルダに.otfファイルを配置し、utils.pyのput_text引数部分のfont-face部分にパスを入力する。
<br>
<br>
最後に、haarカスケード分類器のモデルを用意する。face.pyのFaceDetectionの初期化時にcascade_setter()を呼び出している引数のようにファイルを配置。ファイル名を検索したら拾える。






<br><br>
必要なライブラリの導入
```bash
pip install -r requirements.txt
```
導入が必要なライブラリは主に以下。上記コマンドでエラーが出た場合は一つずつ直接入れる。テスト環境はMacOS。
<ul>
    <li>opencv-python</li>
    <li>vosk</li>
    <li>pillow</li>
    <li>pyttsx3</li>
    <li>sounddevice</li>
    <li>deepface</li>
    <li>mediapipe</li>
</ul>

起動
```bash
python3 src/main.py
```

エラーが出る場合、以下により改善する可能性がある。
<ul>
    <li>capture.pyのCameraCaptureで設定されているカメラ幅、高さ、フレームレートを変更する。</li>
    <li>main.pyで音声を取得する際にdevice=Noneとなっている部分を変更する。</li>
    <li>再度実行する。</li>
</ul>


終了

<ul>
    <li>Ctrl+C</li>
    <li>Q,q,escのいずれかを入力</li>
    <li>「さようなら」「さよなら」を音声認識させる。</li>
</ul>




## 概要
カメラ・マイクの入力をもとに、リアルタイムでノベルゲーム風の画面を生成する。それぞれ、以下のような対応関係で画面が生成される。
<ul>
    <li>カメラに映る顔の位置によって、生成された画面内のキャラクターの立ち位置が変化する。</li>   
    <li>顔の表情によって、キャラクターの表情が変わる。</li>
    <li>カメラに映る手が立てている指の本数によって背景が変わる。</li>
    <li>カメラに映るのが右手の場合、手の甲を映すとキャラクターが変わる。左手の場合、手のひらを映すと変わる。</li>
    <li>マイクに入力された音声が台詞として表示される。</li>
    <li>「さようなら」「さよなら」を音声認識すると別れの挨拶を喋る。</li>
</ul>
なお、終了時の挨拶はLinuxではうまく動かないことが確認されている。

# クレジット

## メッセージウインドウ素材
サイト｜空想曲線

ＵＲＬ｜https://kopacurve.blog.fc2.com/

## 立ち絵素材
URL：http://ranuking.ko-me.com/

サイト：らぬきの立ち絵保管庫

## 背景素材
KNT graphics：矢神ニーソ

http://kntgraphics.web.fc2.com

## フォント
ふぉんときゅーとがーる。

http://font.cutegirl.jp/

lisence: SIL Open Font Lisense