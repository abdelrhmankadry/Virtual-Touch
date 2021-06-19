# -*- coding: utf-8 -*-

from event_handler import EventHandler

"""
@author: 
    
This class is resposible for listening for (detecting)
and informing about specific hand gestures

"""

class EventListenr:
    
    def __init__(self, hand_detector, pyautogui):
        self.pyautogui = pyautogui
        self.hand_detector = hand_detector
        self.gesture_action_table  = self.get_gesture_event_action_table()
        self.prev_arrow_x = 0
        self.prev_arrow_y = 0
        self.arrow_x = 0
        self.arrow_y = 0
        self.distance_x = None
        self.distance_y = None

    def listen(self):
        
        rotated_landmarks =  self.hand_detector.get_rotated_landmarks()
        box = self.hand_detector.get_hand_box(land_marks =rotated_landmarks)
        landmarks = self.hand_detector.get_landmarks_position()

        '''
        - This for loop is resposible for detecting standard hand gesture
        - standard hand gestures: are gesture detected when the hand is fixed
            (not moving)
        '''
        
        for gestures, event, action in self.gesture_action_table:
            if self.hand_detector.detect_gesture(gestures, None):
                return event,  action
        
        '''
        - This for loop is resposible for detecting transitional hand gesture
        - transitional hand gestures: are gesture only detected when the hand
            is making a specific hand gesture and moves in a specific direction
            with predifined distance .
        '''
        
        #detecting the hand gesture
        if self.hand_detector.detect_gesture(["arrow_key","arrow_key_2", "arrow_key_3"], None) and self.distance_x == None and self.distance_y == None:
                    self.prev_arrow_x = (landmarks[8][0] + landmarks[4][0])/((box[2] - box[0])*2)
                    self.distance_x = 0
                    self.prev_arrow_y = (landmarks[8][1] + landmarks[4][1])/((box[3] - box[1])*2)
                    self.distance_y = 0
                    return EventHandler.PRESS_ARROW_START, lambda : print("press arrow")
                
        elif self.hand_detector.detect_gesture(["arrow_key", "arrow_key_2", "arrow_key_3"], None):
            self.arrow_x = (landmarks[8][0] + landmarks[4][0])/((box[2] - box[0])*2)
            self.distance_x = self.arrow_x  - self.prev_arrow_x
            self.arrow_y = (landmarks[8][1] + landmarks[4][1])/((box[3] - box[1])*2)
            self.distance_y = self.arrow_y  - self.prev_arrow_y
            
            #checking if the hand moved left or right with specific distance
            if abs(self.distance_x) > (90/(box[2] - box[0])):

                self.prev_arrow_x = 0
                self.arrow_x = 0
                if self.distance_x < 0:
                    self.distance_x = None
                    self.distance_y = None
                    return EventHandler.PRESS_ARROW_END, self.pyautogui.press('left')
                else:

                    self.distance_x = None
                    self.distance_y = None
                    return EventHandler.PRESS_ARROW_END, self.pyautogui.press('right')
                
            #checking if the hand moved top or down with specific distance
            elif abs(self.distance_y) > (60/(box[3] - box[1])):

                self.prev_arrow_y = 0
                self.arrow_y = 0
                
                if self.distance_y < 0:
                    self.distance_y = None
                    self.distance_x = None
                    return EventHandler.PRESS_ARROW_END, self.pyautogui.press('up')
                else:

                    self.distance_y = None
                    self.distance_x = None
                    return EventHandler.PRESS_ARROW_END, self.pyautogui.press('down')
                    
        return None, None
    
    def set_hand_detector(self, hand_detector):
        self.hand_detector = hand_detector
        
    """
    - This function is resposible for returning a list with the following structure:
    every element of the list is a tuple, with first element is a list of gesture file name
    'as we store the feature of every gesture in our file system',
    second element is event, third element is an action.
    
   -  we use this structure se we can excute the following procedure:
        for every gesture in the list of the first element of the tuple
        if it matched with the input gesture
        return the corresponding event and action.
    """
    def get_gesture_event_action_table(self):
        return  [(["swich_app_open", "swich_app_open_2"], EventHandler.SWITCH_APP_OPEN ,lambda: print("gesture detected")),
          (["swich_app_close", "swich_app_close_2", "swich_app_close_3"], EventHandler.SWITCH_APP_CLOSE, lambda: self.pyautogui.hotkey('alt', 'tab')),
          (["close_app_start"], EventHandler.CLOSE_APP_START, lambda:print("gesture detected")),
          (["close_app_end"], EventHandler.CLOSE_APP_END, lambda:self.pyautogui.hotkey('alt', 'f4')),
          (["f_press_start","f_press_start2"], EventHandler.PRESS_F_START, lambda: print("gesture detected")),
          (["f_press_end", "f_press_end2"], EventHandler.PRESS_F_END, lambda: self.pyautogui.press('f'))]