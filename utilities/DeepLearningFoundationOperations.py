# Import Essential Libraries
import os
import numpy as np
try:
   os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
   from keras.models import load_model
except:
    print("Check instalation of Tensorflow and Keras for Compatibility with OS and HardWare!")
import cv2
import time
from os.path import isfile, join
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QFileDialog
import re

class DeepLearningFoundationOperations(QObject):
    def __init__(self,parent=None):
        super().__init__()
        # Internal Variable to Access Images and Videos inside All Functions in the Class      
        self.camera = None

    # Consider|Attention: 

    def SelectDLOperations(sef,text):
        print(text)

    def PrepareSelectDLCamera(self,text):
        print(text)
        self.camera = text

     