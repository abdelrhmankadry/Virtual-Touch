# -*- coding: utf-8 -*-
"""
@author: 
"""

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from app import App

my_app = App()

def start_fn():
    print ("start")
    my_app.start_app()


def stop_fn():
    my_app.stop_app()

    
a=QApplication(sys.argv)

t=QWidget()

t.setWindowTitle("Virtual Touch")



lab=QLabel(t)
t.resize(500,300)

start=QPushButton("Start ",t)
stop=QPushButton("Stop ",t)

start.setFont(QFont('Times', 15))
stop.setFont(QFont('Times', 15))


start.setGeometry(75, 130, 150, 40)
start.setStyleSheet(" border-radius : 9px;background-color :  #2e4053 ;color: white ;")
stop.setGeometry(275, 130, 150, 40)
stop.setStyleSheet(" border-radius : 9px;background-color :  #2e4053 ;color: white ;")

start.clicked.connect(start_fn)
stop.clicked.connect(stop_fn)


t.setStyleSheet("background-color:  #5d6d7e ;")

t.show()

sys.exit(a.exec())