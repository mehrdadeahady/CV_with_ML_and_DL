import io
from io import BytesIO
import requests
import sys
import contextlib
import os
from os.path import isfile, join
import time
import shutil
import random
import tkinter as tk
import threading
import math
from copy import deepcopy
from collections import Counter
import json
import pickle
import regex as re
from functools import lru_cache
from utilities.DeepLearningFoundationOperations import DownloadLogPopup, LogEmitter
from utilities.DLbyPyTorch import EarlyStop, DLbyPyTorch, PopupStream
from utilities.bpe import get_encoder, BPETokenizer
from utilities.processor import (_control_preprocess,_note_preprocess,_divide_note,_make_time_sift_events,_snote2events,encode_midi, decode_midi)
from utilities.ScrollableMessageBox import show_scrollable_message
from utilities.diffusion_unet import (transforms,DDIMScheduler,Attention,UNet)
try:
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1' # '0' or '1' 1 activate intel speed support
    # print(tf.config.list_physical_devices('GPU'))
    import torch
    #import torch.nn as nn
    from torch import nn, einsum
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, Dataset
    import torchvision
    import torchvision.transforms as T
    from torchvision.utils import make_grid, save_image
    from torchvision.datasets import ImageFolder
except:
    print("Check instalation of torch for Compatibility with OS and HardWare!")
try:
    import numpy as np
except:
    print("You Should Install numpy Library")
try:
    import PIL
    from PIL import Image
except:
    print("You Should Install pillow Library")
try:
    import pandas as pd
except:
    print("You Should Install pandas Library")
try:
    from tqdm import tqdm
except:
    print("You Should Install tqdm Library")
try:
    from transformers import XLMTokenizer
except:
    print("You Should Install transformers Library")
try:
    from contextlib import nullcontext
except:
    print("You Should Install contextlib Library")
try:
    import cv2
    from cv2_enumerate_cameras import enumerate_cameras
except:
    print("You Should Install OpenCV-Python and cv2_enumerate_cameras Libraries")
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
except:
    print("You Should Install matplotlib Library!")
try:
    import albumentations
    from albumentations.pytorch import ToTensorV2
except:
    print("You Should Install albumentations Library with below flag to avoid installing opencv headless causing confilict.\npip install albumentations --no-deps\nthen install one of its dependencies:\npip install albucore==0.0.24  --no-deps")
try:
    from music21 import note, stream, duration, tempo
except:
     print("You Should Install music21 Library!")
try:
    import pretty_midi
except:
     print("You Should Install pretty_midi Library!")
try:
    from datasets import load_dataset
except:
     print("You Should Install datasets Library!")
try:
    from einops import rearrange
except:
     print("You Should Install einops Library!")
try:
    from diffusers.optimization import get_scheduler
except:
     print("You Should Install diffusers Library!")
try:
    # https://platform.openai.com/docs/models for a list of models
    from openai import OpenAI
except:
     print("You Should Install openai Library!")
try: 
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
    from PyQt6.QtGui import  QTextCursor   
    from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt, QUrl
    from PyQt6.QtWidgets import QMessageBox,QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QTextEdit,QScrollArea,QMainWindow,QApplication
except:
    print("You Should Install PyQt6 Library!")

# Define a class for handling text-to-image generation using diffusion models
# Inherits from QObject to integrate with PyQt signal-slot system
class OpenAIPromptEngineeringLangChain(QObject):

    # Constructor method to initialize the class instance
    # Parameters:
    #   parent - optional parent QObject (default is None)
    def __init__(self, parent=None):     
        # Call the base class constructor
        super().__init__()

        # Set a fixed random seed for reproducibility of results
        torch.manual_seed(0)

        # Create a log emitter instance for emitting log messages
        self.log_emitter = LogEmitter()

        # Create a popup window for displaying download logs
        # Pass the log emitter to enable real-time log updates
        self.DownloadLogPopup = DownloadLogPopup(
            self.log_emitter
        )

        # Determine the device to use for computation: GPU if available, otherwise CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")