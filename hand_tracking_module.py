# -*- coding: utf-8 -*-




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
                        # print(id, cx, cy)
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
    

    def get_rotated_landmarks(self, hand_number=0):
        landmarks = self.get_landmarks_position(hand_number)
        rotated_landmarks = []
        if not len(landmarks) == 0:
            midp_x = int((landmarks[13][0] + landmarks[9][0])/2)
            midp_y = int((landmarks[13][1] + landmarks[9][1])/2)
            palm_x, palm_y = int(landmarks[0][0]), int(landmarks[0][1])
            refrence_angle = self.calculate_angle(midp_x, midp_y, palm_x, palm_y)
            shift_angle = 90 - refrence_angle
            rotated_landmarks =\
            [self.rotate_point(i[0], i[1],shift_angle ) for i in landmarks]
            return rotated_landmarks
        
    def calculate_angle(self, x1, y1, x2, y2):
        deltaY = y2 - y1
        deltaX = x2 - x1
        
        if (deltaX == 0 and deltaY == 0):
            return 0
        angle = arctan2(array([deltaY]), array([deltaX]))
        result = math.degrees(angle)
        
        if result < 0:
            return result + 360
        else:
            return result
    
    """
    we use this funtion to rotate the land marks of the hand to be 
    in a vertical position so we can detect gestures easly.
    
    In other words if the hand is rotated to the right or the left 
    we will rotate it to be in vertical position, so we can compare the 
    run time vertical hand gesture to the stored vertical hand gesture 
    so we don't need to store many gesture positions.
    """
    def rotate_point(self, x, y, angle):

        angle = radians(angle)
        rotation_matrix = array([[cos(angle), - sin(angle)],\
                                    [sin(angle), cos(angle)]])
            
        result = rotation_matrix @ array([x,y])
        return result[0], result[1]
    
    #return the the hand landmarks relative to the the top left corner of the hand box
    def get_hand_features(self):
        rotated_landmarks = self.get_rotated_landmarks()
        box = self.get_hand_box(land_marks=rotated_landmarks)
        refernce_point = box[0]-20, box[1]-20
        landmarks  = rotated_landmarks
        features = [(refernce_point[0] - i[0], refernce_point[1] - i[1]) for i in landmarks]
        return features
    
    # store hand features as pkl file so we can use it later to detect similar gestures
    def save_gesture(self, name):
        if keyboard.is_pressed('s'):
            rotated_landmarks = self.get_rotated_landmarks()
            gesture = self.get_hand_features()
            box = self.get_hand_box(land_marks=rotated_landmarks)
            with open(name +".pkl", 'wb') as output:
                pickle.dump((gesture, box), output, pickle.HIGHEST_PROTOCOL)
            
    
    # This function is resposible for detecting a certain gesture
    # using gesture file name as input
    def detect_gesture(self, names, action):
        for name in names:
            try:
                with open("./gestures/"+name+'.pkl', 'rb') as input:
                    ges_box = pickle.load(input)
            except(OSError, IOError) as e:
                return 
            
            gesture, refrence_box = ges_box
            
            new_gesture = self.get_hand_features()
            new_gesture = self.__rescale_features(new_gesture, refrence_box)
            
            if self.__compare_features(gesture, new_gesture):
                if action:
                    action()
                return True
            else:
                return False
    
    # This function is resposible for comparing two hand features 
    # if the error between two features is beneath certain value then they are similar
    def __compare_features(self, refrence_features, detected_features):
        error_threshold = 12000
        error = sum([(refrence_feature[0] - detected_features[0])**2 +\
                     (refrence_feature[1] - detected_features[1])**2\
                     for refrence_feature, detected_features in\
                         zip(refrence_features, detected_features) ])
        # print(error)
        return error < error_threshold
    
    
    # These functions are resposible for rescaling hand feature depending on
    # it's distance form the camera
    def __rescale(self, refrence_l, new_l, value):
            return (refrence_l/ new_l) * value
    def __rescale_features(self, gesture, refrence_box):
        
        new_box = self.get_hand_box(land_marks=self.get_rotated_landmarks())
        refrence_l_x = refrence_box[2] - refrence_box[0]
        refrence_l_y = refrence_box[3] - refrence_box[1]
        new_l_x = new_box[2] - new_box[0]
        new_l_y = new_box[3] - new_box[1]
        new_gesture = [(self.__rescale(refrence_l_x,new_l_x,i[0]),\
                        self.__rescale(refrence_l_y,new_l_y,i[1])) for i in gesture]
        return new_gesture
    