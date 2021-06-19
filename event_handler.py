# -*- coding: utf-8 -*-



import threading
"""
@author: 

This class is resposible for excute some action when a sequence 
of 2 events is triggered    
"""
        
class EventHandler:
    
    SWITCH_APP_OPEN = 0
    SWITCH_APP_CLOSE = 1
    CLOSE_APP_START = 2
    CLOSE_APP_END = 3
    PRESS_ARROW_START = 4
    PRESS_ARROW_END = 5
    PRESS_F_START = 6
    PRESS_F_END = 7
    
    def __init__(self):
        
        self.events_intervals = self.get_events_intervels()
        self.events_pairs =  self.get_events_pair()
        self.first_events = self.get_starting_events()
        self.second_events =  self.get_closing_events()
        self.timer_flag = [False]
        self.current_event = None
        self.timer = None
        
    """
    - This function handles two types of event, starting event and ending event.
    
    - if the input event is starting event a timer will issued with intervel time
      coresponding to the input event.
    
    - if the timer is timed out we reinitialize the state of the class
      but if a closing event is triggered before timeing out the function
      will excute an action coresponding to the event
    """
    def handle(self, event, action):
        if event in self.first_events:
             if not self.current_event:
                self.current_event = event
                self.timer_flag[0] = True
                self.timer = threading.Timer(self.events_intervals[event], self.timer_timeout)
                self.timer.start()
        elif event in self.second_events:
            if self.current_event == self.events_pairs[event] and self.timer_flag[0]:
                action()
            self.timer.cancel()
            self.current_event = None
            
    # reinitalize class state when time out        
    def timer_timeout(self):
        self.timer_flag[0] = False
        self.current_event = None
    
    # returns the waiting intervel time for every event
    def get_events_intervels(self):
        return  {self.SWITCH_APP_OPEN : 12.0,
            self.CLOSE_APP_START: 5.0,
            self.PRESS_ARROW_START : 10.0,
            self.PRESS_F_START:20.0 }
    
    # returns a map for every ending event to it's starting event
    def get_events_pair(self):
        return {
            self.SWITCH_APP_CLOSE: self.SWITCH_APP_OPEN,
            self.CLOSE_APP_END: self.CLOSE_APP_START,
            self.PRESS_ARROW_END: self.PRESS_ARROW_START,
            self.PRESS_F_END: self.PRESS_F_START
            }
    
    # returns a list of Starting events
    def get_starting_events(self):
        return [self.SWITCH_APP_OPEN, self.CLOSE_APP_START,\
            self.PRESS_ARROW_START, self.PRESS_F_START]
        
    # returns a list of Ending events
    def get_closing_events(self):
        return [self.SWITCH_APP_CLOSE, self.CLOSE_APP_END,\
            self.PRESS_ARROW_END, self.PRESS_F_END]