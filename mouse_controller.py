# -*- coding: utf-8 -*-


import mouse 
import numpy as np
import wx


# the functions smooths the value of the (x,y) coordinates of mouse position 
def low_pass(x_new, y_old, cutoff=4):
    dt = 30
    alpha = dt / (dt + 1 / (2 * np.pi * cutoff))
    y_new = x_new * alpha + (1 - alpha) * y_old
    return y_new

"""
@author: 

This class is reposible for controlling the mouse like 
moving the the mouse or scrolling
"""
class MouseController:
    
    def __init__(self):
        self.previousX = 0
        self.previousY = 0
        self.x_points = np.array([0,0,0,0,0,0])
        self.y_points = np.array([0,0,0,0,0,0])
        app = wx.App(False)
        self.sWidth, self.sHeight = wx.GetDisplaySize()
        self.padding = 100
        self.counter = 0
        self.previousMX = 0
        
    def perform_action(self, action, x, y, img_shape):
        
        mouseX, mouseY = self.__adjust_x_y(x,y, img_shape)
        
        if action == "move_mouse":
            self.move_mouse(mouseX,mouseY)
        elif action == "scroll":
            self.scroll(y, img_shape)
    
    
    
    def move_mouse(self, x, y):
        mouse.move(x,  y, absolute=True)
        
    def scroll(self, y, img_shape):
        sensitivity = 0.1
        cHeight, cWidth, _ = img_shape
        if y < cHeight // 2:
            mouse.wheel(sensitivity)
        else:
            mouse.wheel(-sensitivity)
        
    # smooths the value of the (x,y) coordinates of mouse position
    def __adjust_x_y(self, x, y, img_shape):
        
        cHeight, cWidth, _ = img_shape
        
        self.previousX = x
        self.previousY = y
        
        cursorX = int(low_pass(x, self.previousX))
        cursorY = int(low_pass(y, self. previousY))
        
        self.x_points[self.counter] = cursorX
        self.y_points[self.counter] = cursorY
        self.counter = (self.counter + 1) % len(self.x_points) 
        
        cursorX = np.mean(self.x_points)
        cursorY = np.mean(self.y_points)
        
        
        mouseX = int(np.interp(cursorX, (self.padding, cWidth - self.padding), (0, self.sWidth)))
        mouseY = int (np.interp(cursorY, (self.padding, cHeight - self.padding - self.padding - 30), (0, self.sHeight)))
        
        return mouseX, mouseY