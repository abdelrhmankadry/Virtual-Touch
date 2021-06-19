
from cv2 import cvtColor, COLOR_BGR2RGB, circle, FILLED
from mediapipe import solutions
import time
from numpy import radians, array, arctan2, cos, sin
import math
import keyboard
import pickle

"""
@author: 

This class is resposible for detecting the hand 
and detecting hand gestures
"""
class HandFeatureDetector():
    def __init__(self,number_of_hands):
        self.mpHands = solutions.hands
        self.hands = self.mpHands.Hands( max_num_hands=number_of_hands, min_detection_confidence=0.7)
        self.mpDraw = solutions.drawing_utils
        self.img_shape = None
        self.gesture = None
        self.box = None
        
    def detect_hands(self, img):
        self.img_shape = img.shape
        imgRGB = cvtColor(img, COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        self.results = self.hands.process(imgRGB)
        imgRGB.flags.writeable = True
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y * h)
    
                    if(id == 8):
                       
                        circle(img, (cx, cy), 10, (255,0,255), FILLED)
                self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def get_landmarks_position(self, hand_number = 0):
        landmarks_l = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_number]
            for id, lm in enumerate(hand.landmark):
                h, w, c = self.img_shape
                cx, cy = int(lm.x*w), int(lm.y * h)
                landmarks_l.append((cx, cy))
        return landmarks_l
    
    # returns top left point and bottom right point for a box that surronding the hand
    def get_hand_box(self, hand_number = 0, land_marks = None):
        if  land_marks == None:
            land_marks = self.get_landmarks_position(hand_number)
        xs, ys = [i[0] for i in land_marks], [i[1] for i in land_marks]
        x_min, x_max = 0,0
        y_min,y_max = 0,0
        if (not len(xs)  == 0) and (not len(ys)  == 0):
            x_min, x_max = min(xs), max(xs)
            y_min,y_max = min(ys), max(ys)

        return int(x_min), int(y_min), int(x_max), int(y_max)
    

    