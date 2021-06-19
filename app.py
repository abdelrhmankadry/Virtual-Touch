from hand_tracking_module import HandFeatureDetector
from mouse_controller import MouseController
from event_handler import EventHandler
from event_listenr import EventListenr

import time

import mouse
from cv2 import VideoCapture, flip, rectangle, waitKey
from wx import GetDisplaySize, App
import math
import pyautogui
import os
import psutil    


app = App(False)
sWidth, sHeight = GetDisplaySize()


hand_detector = HandFeatureDetector(1)
d_controller = MouseController()
e_handler = EventHandler()
e_listener = EventListenr(hand_detector, pyautogui)

is_mouse_move= [True]
def set_mouse_is_not_moving():
    is_mouse_move[0] =  False
    
#open on screen keyboard
def open_osk():
    if not "osk.exe" in (p.name() for p in psutil.process_iter()):
        os.popen("C:\WINDOWS\system32\osk.exe")
        print("Keyboard")
        
class App:    
    
    def __init__(self):
        self.is_running =True
    def stop_app(self):
        self.is_running = False
        
    def start_app(self):
        
        cap = VideoCapture(0)
        cap.set(3, sWidth)
        cap.set(4, sHeight)
        pTime = 0
        cTime = 0
        padding = 100
    
        cursorX =0
        cursorY = 0

        while cap.isOpened():
            if not self.is_running:
                cap.release()
                break
            success, img = cap.read()
            cHeight, cWidth, _ = img.shape
            img = flip(img, 1)
            img = hand_detector.detect_hands(img)
            landmarks = hand_detector.get_landmarks_position()
            
            # This part is resposible for controlling the mouse
            if not len(landmarks) == 0:
                cursorX = (landmarks[8][0] + landmarks[12][0]) // 2
                cursorY = (landmarks[8][1] + landmarks[12][1]) // 2
        
                rotated_landmarks =  hand_detector.get_rotated_landmarks()
                box = hand_detector.get_hand_box(land_marks =rotated_landmarks)
         
                x_diff = (landmarks[5][0] - landmarks[3][0])/(box[2] - box[0])
                y_diff = (landmarks[5][1] - landmarks[3][1])/(box[3] - box[1])
                
                length = math.hypot(x_diff, y_diff) 
                time.sleep(0.001)
                if is_mouse_move[0]:
                    d_controller.perform_action("move_mouse", cursorX, cursorY, img.shape)
                    if length <= 0.25:
                        mouse.press(button='left')
                        time.sleep(0.1)
                    else:
                        mouse.release(button='left')
                else:
                    d_controller.perform_action("scroll", cursorX, cursorY, img.shape)
                hand_detector.save_gesture("arrow_key_3")
                
                if not hand_detector.detect_gesture(["scrolling2", "scrolling"], set_mouse_is_not_moving):
                    is_mouse_move[0] = True
                    
                # This part is reposible for detecting gestures
                hand_detector.detect_gesture(["open_osk"], open_osk)
                e_listener.set_hand_detector(hand_detector)
                event, action  = e_listener.listen()

                if action:
                    e_handler.handle(event, action)
                
            rectangle(img,(padding, padding),(cWidth - padding, cHeight - padding - padding -30) , (0, 255, 0), 2)

            # cv2.imshow("Image", img)
            if waitKey(1) & 0xFF == ord('q'):
                break
             