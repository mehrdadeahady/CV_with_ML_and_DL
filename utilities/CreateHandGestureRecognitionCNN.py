import os
from os.path import isfile, join
import time
try:
    os.environ["KERAS_BACKEND"] = "tensorflow"  # or "jax", "torch"
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1' # '0' or '1' 1 activate intel speed support
    # print(tf.config.list_physical_devices('GPU'))
    import keras
    from keras import callbacks
    from keras.callbacks import Callback
    from keras.datasets import mnist 
    from keras.utils import to_categorical
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
    from keras import backend as K
    from keras.optimizers import SGD 
except:
    print("Check instalation of Tensorflow and Keras for Compatibility with OS and HardWare!")
try:
    import numpy as np
except:
    print("You Should Install numpy Library")
try:
    import cv2
    from cv2_enumerate_cameras import enumerate_cameras
except:
    print("You Should Install OpenCV-Python and cv2_enumerate_cameras Libraries")
try:
    import matplotlib.pyplot as plt
except:
    print("You Should Install matplotlib Library!")
try:
    from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt
    from PyQt6.QtWidgets import QMessageBox,QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QTextEdit,QScrollArea
except:
    print("You Should Install PyQt6 Library!")

class CreateHandGestureRecognitionCNN(QObject):
    LoadMNISTRawDataOrPreparedData = pyqtSignal(int)
    def __init__(self,ImagesAndColorsHandler,CreateSimpleCNNHandler,parent=None):
        super().__init__()
        # Internal Variable to Access Data inside All Functions in the Class 
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.input_shape = ()
        self.numberOfClasses = 0
        self.numberOfPixels = 0
        self.model = None
        self.modelSummary = ""
        self.modelHistory = None
        self.TrainedModel  = None
        self.training_thread = None
        self._is_running = False
        self.steps_per_epoch = None 
          
    # There are functions here for Creating a Simple CNN Model for Hand Gesture Recognition for Master Degree Level
    # Find Comments and Explanation for each function related to ML and CV
    # UI functions do not have Comments because this is not a QT Training but they are Clear to Understand by its names and contents
