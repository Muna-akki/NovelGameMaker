import cv2 as cv
import numpy as np
import mediapipe as mp


# 画像から手を認識するクラス
class HandDetection():
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mesh_drawing_spec = self.mp_drawing.DrawingSpec(thickness=2, color=(0,255,0))
        self.mark_drawing_spec = self.mp_drawing.DrawingSpec(thickness=3, circle_radius=3, color=(0,0,255))
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.finger_number = 0
        self.back_hand_flag = False
        print("HandDetection Initialization Finished")
    

    # 手の認識を実行
    def execute_hand_detection(self, cap_data, output_data):
        cap_data.input_frame = cv.flip(cap_data.input_frame, 1)
        cap_data.smallImg_colored = cv.flip(cap_data.smallImg_colored, 1)
        # To improve performance, optionally mark the image as not writeable to pass by reference.
        # ↑公式のドキュメントに書いてあった。ほんまか？
        cap_data.smallImg_colored.flags.writeable = False
        results = self.hands.process(cap_data.smallImg_colored)
        cap_data.smallImg_colored.flags.writeable = True
        self.finger_number = 0
        self.back_hand_flag = False
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks: # 一応ループだが、手は１つまでしか認識されない設定
                self.mp_drawing.draw_landmarks(
                    image=cap_data.input_frame,
                    landmark_list=hand_landmarks,
                    connections=self.mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=self.mark_drawing_spec,
                    connection_drawing_spec=self.mesh_drawing_spec
                )
                self.finger_number += self.count_finger(hand_landmarks.landmark)
                self.back_hand_flag = self.is_right_back_hand(hand_landmarks.landmark)
        cap_data.input_frame = cv.flip(cap_data.input_frame,1)
        cap_data.input_add_text("finger:"+str(self.finger_number), (0,0), 20, (0,0,255,0))
        output_data.update_when(self.finger_number)
        output_data.update_who(self.back_hand_flag)

    
    # 画像に映る手のうち、何本の指が立っているかを数える
    def count_finger(self, hand_landmark):
        count = 0
        base_distance = self.calc_distance(hand_landmark[0],hand_landmark[1])
        thumb = self.is_thumb_active(hand_landmark, base_distance)
        index_finger = self.is_index_finger_active(hand_landmark, base_distance)
        middle_finger = self.is_middle_finger_active(hand_landmark, base_distance)
        ring_finger = self.is_ring_finger_active(hand_landmark, base_distance)
        pinky_finger = self.is_pinky_finger_active(hand_landmark, base_distance)
        
        if thumb:
            count += 1
        if index_finger:
            count += 1
        if middle_finger:
            count += 1
        if ring_finger:
            count += 1
        if pinky_finger:
            count += 1
        return count


    # 2点間の距離を出す
    def calc_distance(self, p1, p2):
        ret = np.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2+(p1.z-p2.z)**2)
        return ret


    # 検出されたのが右手だとして、手の甲が見えているかの判定
    def is_right_back_hand(self, hand_landmark):
        x1 = hand_landmark[5].x
        x2 = hand_landmark[17].x
        return x1-x2>0


    # 親指が立っているか
    def is_thumb_active(self, hand_landmark, base_distance):
        distance = self.calc_distance(hand_landmark[4], hand_landmark[5])
        judge1 = distance>base_distance*1.2
        judge2 = ((hand_landmark[4].x-hand_landmark[5].x)*(hand_landmark[4].x-hand_landmark[17].x))>0
        return (judge1 and judge2)


    # 人差し指が立っているか
    def is_index_finger_active(self, hand_landmark, base_distance):
        distance = self.calc_distance(hand_landmark[0], hand_landmark[8])
        return (distance > base_distance*3)


    # 中指が立っているか
    def is_middle_finger_active(self, hand_landmark, base_distance):
        distance = self.calc_distance(hand_landmark[0], hand_landmark[12])
        return (distance > base_distance*3)


    # 薬指が立っているか
    def is_ring_finger_active(self, hand_landmark, base_distance):
        distance = self.calc_distance(hand_landmark[0], hand_landmark[16])
        return (distance > base_distance*3)


    # 小指が立っているか
    def is_pinky_finger_active(self, hand_landmark, base_distance):
        distance = self.calc_distance(hand_landmark[0], hand_landmark[20])
        return (distance > base_distance*3)

