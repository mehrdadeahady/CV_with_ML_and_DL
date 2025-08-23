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
        self.image = None
        self.imageName = None
        self.tempImage = None
        self.tempImageName = None
        self.video = None
        self.videoCapturer = None
        self.camera = None

    # Consider|Attention: 
    