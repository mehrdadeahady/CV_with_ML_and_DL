import io
import sys
import contextlib
import os
try:
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1' # '0' or '1' 1 activate intel speed support
    # print(tf.config.list_physical_devices('GPU'))
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, Dataset
    import torchvision
    import torchvision.transforms as T
    from torchvision.utils import make_grid, save_image
    from torchvision.datasets import ImageFolder
except:
    print("Check instalation of torch for Compatibility with OS and HardWare!")
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
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
    from PyQt6.QtGui import  QTextCursor   
    from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt, QUrl
    from PyQt6.QtWidgets import QMessageBox,QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QTextEdit,QScrollArea,QMainWindow,QApplication
except:
    print("You Should Install PyQt6 Library!")

# Define a class for generating music using a GPT-style Music Transformer model
# Inherits from QObject to integrate with Qt's signal-slot mechanism for GUI interaction
class GeneratingMusicByGPTStyleMusicTransformer(QObject):

    # Constructor method to initialize the class instance
    # :param parent: Optional parent object for QObject hierarchy
    def __init__(self, parent=None):     
        # Call the base class constructor to ensure proper QObject initialization
        super().__init__()

        # Set a fixed random seed for reproducibility of results across different runs
        torch.manual_seed(0)

        # Instantiate a log emitter to asynchronously send log messages to the UI
        self.log_emitter = LogEmitter()

        # Create a popup window to display logs during dataset loading, training, or generation
        self.DownloadLogPopup = DownloadLogPopup(
            # Pass the log emitter to the popup for real-time log updates
            self.log_emitter
        )

        # Determine the computation device: use GPU if available, otherwise fallback to CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load configuration settings for the model, training, and data handling
        self.config = Config()

        # Initialize the training data loader to None; will be set during data preparation
        self.trainloader = None

        # Initialize training dataset placeholder
        self.train = None

        # Initialize testing dataset placeholder
        self.test = None

        # Initialize validation dataset placeholder
        self.val = None

        # Initialize the model placeholder; will be assigned during model setup
        self.model = None

    # Define a method to prompt the user with instructions for downloading the dataset
    def DownloadDataset(self):
        # Display a warning message box with the dataset download link and instructions
        QMessageBox.warning(
            None,  # No parent widget for the message box
            "Download Link:",  # Title of the message box
            "Download the dataset from below link:\n" +  # Instructional message
            "https://storage.googleapis.com/magentadata/datasets/maestro/v2.0.0/maestro-v2.0.0-midi.zip\n" +  # Direct download URL for the dataset
            "move the internal maestro-v2.0.0 folder in resources filder in the root of the project."  # Additional instruction for placing the dataset
        )

    # Define a method to organize the Maestro dataset into train, validation, and test directories
    def ArrangeDataset(self):
        # Check if the dataset directory exists; if not, prompt the user to download it first
        if not os.path.exists("resources/maestro-v2.0.0"):
            # Show a warning message indicating the dataset is missing
            QMessageBox.warning(None, "No Dataset", "First download the Dataset.")
            return  # Exit the method early since dataset is not available

        # Create directories for train, validation, and test splits if they don't already exist
        os.makedirs("resources/maestro-v2.0.0/train", exist_ok=True)
        os.makedirs("resources/maestro-v2.0.0/val", exist_ok=True)
        os.makedirs("resources/maestro-v2.0.0/test", exist_ok=True)

        # Count the number of files currently present in each split directory
        train_size = len(os.listdir('resources/maestro-v2.0.0/train'))
        val_size = len(os.listdir('resources/maestro-v2.0.0/val'))
        test_size = len(os.listdir('resources/maestro-v2.0.0/test'))

        # Check if the dataset is incomplete and needs to be arranged
        if train_size < 960 or val_size < 130 or test_size < 170:
            # Show the log popup to inform the user that dataset arrangement is in progress
            self.DownloadLogPopup.show()
            self.DownloadLogPopup.Append_Log("Arranging Dataset...\nIt takes several minutes\nPlease wait.")

            # Define the path to the JSON metadata file containing dataset split information
            file = "resources/maestro-v2.0.0/maestro-v2.0.0.json"

            # Open and load the JSON file containing metadata for all MIDI files
            with open(file, "r") as fb:
                maestro_json = json.load(fb)

            # Iterate over each entry in the JSON metadata
            for i, x in enumerate(maestro_json):
                # Log the current index being processed
                self.DownloadLogPopup.Append_Log("Started Index " + str(i))

                # Construct the full path to the original MIDI file
                mid = rf'resources/maestro-v2.0.0/{x["midi_filename"]}'

                # Extract the dataset split type (train, validation, or test)
                split_type = x["split"]

                # Generate a filename for the processed file by appending .pickle
                f_name = mid.split("/")[-1] + ".pickle"

                # Determine the output path based on the split type
                if split_type == "train":
                    o_file = rf'resources/maestro-v2.0.0/train/{f_name}'
                elif split_type == "validation":
                    o_file = rf'resources/maestro-v2.0.0/val/{f_name}'
                elif split_type == "test":
                    o_file = rf'resources/maestro-v2.0.0/test/{f_name}'

                # Encode the MIDI file into a format suitable for training
                prepped = encode_midi(mid)

                # Save the encoded data as a pickle file in the appropriate split directory
                with open(o_file, "wb") as f:
                    pickle.dump(prepped, f)

            # Recalculate the number of files in each split after processing
            train_size = len(os.listdir('resources/maestro-v2.0.0/train'))
            val_size = len(os.listdir('resources/maestro-v2.0.0/val'))
            test_size = len(os.listdir('resources/maestro-v2.0.0/test'))

            # Log the final dataset statistics after successful arrangement
            self.DownloadLogPopup.Append_Log(
                "Dataset Arranged Successfully.\nStatistics of the Dataset:\n" +
                f"there are {val_size} files in the validation set\n" +
                f"there are {train_size} files in the train set\n" +
                f"there are {test_size} files in the test set"
            )
        else:
            # If dataset is already arranged, show an informational message with current statistics
            QMessageBox.information(
                None,
                "Dataset Arranged",
                "Dataset already Arranged.\n" +
                "Statistics of the Dataset:\n" +
                f"there are {val_size} files in the validation set\n" +
                f"there are {train_size} files in the train set\n" +
                f"there are {test_size} files in the test set"
            )

    # Define a method to tokenize a sample MIDI file from the dataset for inspection and debugging
    def TokenizeData(self):
        # Check if the 2018 subdirectory of the dataset exists; if not, prompt the user to download it
        if not os.path.exists("resources/maestro-v2.0.0/2018"):
            # Show a warning message indicating the dataset is missing
            QMessageBox.warning(None, "No Dataset", "First download the Dataset.")
            return  # Exit the method early since dataset is not available

        # Show the log popup to inform the user that tokenization is starting
        self.DownloadLogPopup.show()
        self.DownloadLogPopup.Append_Log(
            "Tokenizing a song in the Dataset.\nPlease wait...\n\nFirst 5 divided notes:\n"
        )

        # Define the filename of a specific MIDI file to tokenize
        file = 'MIDI-Unprocessed_Chamber1_MID--AUDIO_07_R3_2018_wav--2'

        # Construct the full path to the MIDI file
        name = rf'resources/maestro-v2.0.0/2018/{file}.midi'

        # Initialize a list to store encoded events
        events = []

        # Initialize a list to store processed notes
        notes = []

        # Load the MIDI file using PrettyMIDI for structured access to musical elements
        song = pretty_midi.PrettyMIDI(name)

        # Iterate over each instrument in the MIDI file
        for inst in song.instruments:
            # Extract the list of notes for the current instrument
            inst_notes = inst.notes

            # Filter and preprocess sustain pedal control changes (MIDI control number 64)
            ctrls = _control_preprocess([ctrl for ctrl in inst.control_changes if ctrl.number == 64])

            # Preprocess notes using control changes and append to the notes list
            notes += _note_preprocess(ctrls, inst_notes)

        # Divide the notes into smaller time-aligned segments (discrete note events)
        dnotes = _divide_note(notes)

        # Sort the divided notes by their onset time
        dnotes.sort(key=lambda x: x.time)

        # Log the first 5 divided notes for inspection
        for i in range(5):
            self.DownloadLogPopup.Append_Log("dnotes " + str(i) + " " + str(dnotes[i]))

        # Initialize variables to track current time and velocity for event generation
        cur_time = 0
        cur_vel = 0

        # Log the start of event generation
        self.DownloadLogPopup.Append_Log("\nFirst 15 events:\n")

        # Iterate over each structured note to generate time and note events
        for snote in dnotes:
            # Generate time-shift events between the current and previous note
            events += _make_time_sift_events(prev_time=cur_time, post_time=snote.time)

            # Generate note-on, note-off, and velocity events from the structured note
            events += _snote2events(snote=snote, prev_vel=cur_vel)

            # Update current time and velocity for the next iteration
            cur_time = snote.time
            cur_vel = snote.velocity

        # Convert all event objects to their integer token representations
        indexes = [e.to_int() for e in events]

        # Log the first 15 generated events for inspection
        for i in range(15):
            self.DownloadLogPopup.Append_Log("events " + str(i) + " " + str(events[i]))

    # Define a method to prepare the dataset for training by loading and formatting it into input-output pairs
    def PrepareData(self):
        # Check if the required dataset directories exist; if not, prompt the user to download the dataset
        if not os.path.exists("resources/maestro-v2.0.0/train") or \
           not os.path.exists("resources/maestro-v2.0.0/test") or \
           not os.path.exists("resources/maestro-v2.0.0/val"):
            QMessageBox.warning(None, "No Dataset", "First download the Dataset.")
            return  # Exit early if dataset folders are missing

        # Count the number of files in each dataset split
        train_size = len(os.listdir('resources/maestro-v2.0.0/train'))
        val_size = len(os.listdir('resources/maestro-v2.0.0/val'))
        test_size = len(os.listdir('resources/maestro-v2.0.0/test'))

        # Ensure the dataset has been arranged with sufficient files in each split
        if train_size < 960 or val_size < 130 or test_size < 170:
            QMessageBox.warning(None, "Dataset not Arranged", "First Arrange the Dataset.")
            return  # Exit if dataset is incomplete

        # If the trainloader is already initialized, assume data is already prepared
        if self.trainloader is not None:
            QMessageBox.warning(None, "Dataset Prepared", "Data already Prepared.")
            return  # Avoid reprocessing

        # Show the log popup to indicate data preparation is starting
        self.DownloadLogPopup.show()

        # Define the maximum sequence length for input/output tensors
        max_seq = 2048

        # Define a helper function to load and format data from a given folder
        def create_xys(folder):
            # Get full paths to all files in the folder
            files = [os.path.join(folder, f) for f in os.listdir(folder)]
            xys = []  # List to store input-output tensor pairs

            # Iterate over each file in the folder
            for i, f in enumerate(files):
                # Log the index of the file being processed
                self.DownloadLogPopup.Append_Log("File Index " + str(i) + "Prepararion.")

                # Load the pickled music token sequence
                with open(f, "rb") as fb:
                    music = pickle.load(fb)

                # Convert the music sequence to a PyTorch LongTensor
                music = torch.LongTensor(music)

                # Initialize input (x) and target (y) tensors filled with padding token (389)
                x = torch.full((max_seq,), 389, dtype=torch.long)
                y = torch.full((max_seq,), 389, dtype=torch.long)

                # Get the length of the music sequence
                length = len(music)

                # If the sequence is shorter than or equal to max_seq, pad the rest
                if length <= max_seq:
                    x[:length] = music
                    y[:length - 1] = music[1:]
                    y[length - 1] = 388  # End-of-sequence token
                else:
                    # If the sequence is longer, truncate to max_seq
                    x = music[:max_seq]
                    y = music[1:max_seq + 1]

                # Append the input-output pair to the list
                xys.append((x, y))

            # Return the list of (x, y) pairs
            return xys

        # Define paths to each dataset split
        trainfolder = 'resources/maestro-v2.0.0/train'
        valfolder = 'resources/maestro-v2.0.0/val'
        testfolder = 'resources/maestro-v2.0.0/test'

        # Log and process the training set
        self.DownloadLogPopup.Append_Log("Preparing Data.\nPlease wait...\nprocessing the training set:\n")
        self.train = create_xys(trainfolder)

        # Log and process the validation set
        self.DownloadLogPopup.Append_Log("processing the validation set:\n")
        self.val = create_xys(valfolder)

        # Log and process the test set
        self.DownloadLogPopup.Append_Log("processing the test set:\n")
        self.test = create_xys(testfolder)

        # Define the batch size for training
        batch_size = 2

        # Create a DataLoader for the training set with shuffling enabled
        self.trainloader = DataLoader(self.train, batch_size=batch_size, shuffle=True)

        # Log the completion of data preparation
        self.DownloadLogPopup.Append_Log("\nPreparing Data finished.\nData is ready for Training.")

    # Define a method to create the transformer-based music generation model
    def CreateModel(self):
        # Check if the model has already been created to avoid redundant instantiation
        if self.model is not None:
            # Show a warning message indicating the model already exists
            QMessageBox.warning(None, "Model Exist", "Model already Created.")
            return  # Exit early to prevent reinitializing the model

        # Instantiate the model using the provided configuration and device (CPU or GPU)
        self.model = Model(self.config, self.device).to(self.device)

        # Calculate the total number of trainable parameters in the transformer's layers
        num = sum(p.numel() for p in self.model.transformer.parameters())

        # Display a scrollable message showing the total number of parameters and model architecture
        show_scrollable_message(
            "Number of parameters: %.2fM" % (num / 1e6,),  # Format parameter count in millions
            str(self.model)  # Convert the model architecture to string for display
        )

    # Define a method to initiate the training process for the music transformer model
    def TrainModel(self):
        # Check if the training data has been prepared; if not, warn the user
        if self.trainloader is None:
            # Display a warning message if the dataset has not been prepared
            QMessageBox.warning(
                None,
                "Data Not Ready",
                "First Prepare the Data."
            )

        # Check if the model has been created; if not, prompt the user to create it
        elif self.model is None:
            # Display a warning message if the model is missing
            QMessageBox.warning(
                None,
                "Model Not Found",
                "Please create the model first."
            )

        else:
            # Enable the cancel button in the log popup to allow user to interrupt training
            self.DownloadLogPopup.cancel_button.setEnabled(True)

            # Display the log popup window to show training progress
            self.DownloadLogPopup.show()

            # Append an initial log message indicating that training has started
            self.DownloadLogPopup.Append_Log("Training model...\nPlease wait.")

            # Create a new thread to run the training process asynchronously
            self.training_thread = TrainingGPTStyleMusicTransformerThread(
                self.DownloadLogPopup,   # Log popup for real-time feedback
                self.trainloader,        # DataLoader containing training data
                self.model,              # The transformer model to be trained
                self.device              # Device (CPU or CUDA) to perform training on
            )

            # Connect the training thread's log signal to the log popup's append method
            self.training_thread.log_signal.connect(self.DownloadLogPopup.Append_Log)

            # Connect the cancel button to the training thread's stop method for user interruption
            self.DownloadLogPopup.cancel_button.clicked.connect(self.training_thread.stop)

            # Start the training thread to begin the model training process
            self.training_thread.start()

    # Define a method to generate a sequence of tokens from a given prompt using the trained model
    # :param prompt: A tensor containing the initial sequence of tokens to condition the generation
    # :param seq_length: Total desired length of the generated sequence (default is 1000)
    # :param temperature: Sampling temperature to control randomness (higher = more random)
    def sample(self, prompt, seq_length=1000, temperature=1):
        # Create a softmax function to convert logits into probabilities
        softmax = torch.nn.Softmax(dim=-1)

        # Initialize a tensor to hold the generated sequence, filled with padding token (389)
        gen_seq = torch.full((1, seq_length), 389, dtype=torch.long).to(self.device)

        # Determine the length of the prompt to know where to start generating
        idx = len(prompt)

        # Copy the prompt tokens into the beginning of the generated sequence
        gen_seq[..., :idx] = prompt.type(torch.long).to(self.device)

        # Begin generating tokens until the desired sequence length is reached
        while idx < seq_length:
            # Log the current progress of generation
            self.DownloadLogPopup.Append_Log("Working on index " + str(idx) + " from " + str(seq_length))

            # Pass the current sequence to the model and apply temperature scaling before softmax
            y = softmax(self.model(gen_seq[..., :idx]) / temperature)[..., :388]  # Exclude special tokens

            # Extract the probability distribution for the next token
            probs = y[:, idx - 1, :]

            # Create a categorical distribution from the probabilities
            distrib = torch.distributions.categorical.Categorical(probs=probs)

            # Sample the next token from the distribution
            next_token = distrib.sample()

            # Assign the sampled token to the current index in the generated sequence
            gen_seq[:, idx] = next_token

            # Move to the next index
            idx += 1

        # Return the generated sequence up to the final index
        return gen_seq[:, :idx]

    # Define a method to generate music using the trained model and save the output as MIDI files
    def GenerateMusic(self):
        # Check if the dataset has been prepared; if not, warn the user
        if self.trainloader is None or self.test is None:
            # Display a warning message if the dataset has not been prepared
            QMessageBox.warning(
                None,
                "Data Not Ready",
                "First Prepare the Data."
            )
            return  # Exit early if data is not ready

        # Check if the model has been created; if not, prompt the user to create it
        if self.model is None:
            QMessageBox.warning(
                None,
                "Model Not Found",
                "Please create the model first."
            )
            return  # Exit early if model is missing

        # Check if the trained model weights file exists; if not, prompt the user to train and save it
        if not os.path.exists("resources/models/musicTransformer.pth"):
            QMessageBox.warning(
                None,
                "No trained model",
                "Please create, train and save the model first."
            )
            return  # Exit early if trained model is not found

        # Show the log popup to indicate music generation is starting
        self.DownloadLogPopup.show()
        self.DownloadLogPopup.Append_Log("Generating Music started.\nPlease wait...")

        # Generate and save the first prompt MIDI file from test sample 42
        prompt, _ = self.test[42]
        prompt = prompt.to(self.device)
        len_prompt = 250
        file_path = "resources/maestro-v2.0.0/prompt.midi"
        decode_midi(prompt[:len_prompt].cpu().numpy(), file_path=file_path)
        self.DownloadLogPopup.Append_Log("First Sample prompt midi file created.\nWait...")

        # Generate and save the second prompt MIDI file from test sample 1
        prompt, _ = self.test[1]
        prompt = prompt.to(self.device)
        len_prompt = 250
        file_path = "resources/maestro-v2.0.0/prompt2.midi"
        decode_midi(prompt[:len_prompt].cpu().numpy(), file_path=file_path)
        self.DownloadLogPopup.Append_Log("Second Sample prompt midi file created.\nWait...")

        # Load the trained model weights into the model
        self.model.load_state_dict(torch.load("resources/models/musicTransformer.pth", map_location=self.device))
        self.model.eval()  # Set the model to evaluation mode

        # Identify which button triggered the generation to determine the case
        sender = self.sender().objectName()

        # Match the sender to one of the predefined generation cases
        match sender:
            # Case 1: Generate music with default temperature using prompt1
            case "pushButton_GnerateMusicCase1_GeneratingMusicByGPTStyleMusicTransformer":
                file_path = "resources/maestro-v2.0.0/prompt.midi"
                prompt = torch.tensor(encode_midi(file_path))
                generated_music = self.sample(prompt, seq_length=1000)
                music_data = generated_music[0].cpu().numpy()
                file_path = 'resources/maestro-v2.0.0/generatedMusicCase1.midi'
                decode_midi(music_data, file_path=file_path)

            # Case 2: Generate music with higher temperature (more randomness)
            case "pushButton_GnerateMusicCase2_GeneratingMusicByGPTStyleMusicTransformer":
                file_path = "resources/maestro-v2.0.0/prompt.midi"
                prompt = torch.tensor(encode_midi(file_path))
                generated_music = self.sample(prompt, seq_length=1000, temperature=1.5)
                music_data = generated_music[0].cpu().numpy()
                file_path = 'resources/maestro-v2.0.0/generatedMusicCase2.midi'
                decode_midi(music_data, file_path=file_path)

            # Case 3: Generate music with lower temperature (more deterministic)
            case "pushButton_GnerateMusicCase3_GeneratingMusicByGPTStyleMusicTransformer":
                file_path = "resources/maestro-v2.0.0/prompt.midi"
                prompt = torch.tensor(encode_midi(file_path))
                generated_music = self.sample(prompt, seq_length=1000, temperature=0.7)
                music_data = generated_music[0].cpu().numpy()
                file_path = 'resources/maestro-v2.0.0/generatedMusicCase3.midi'
                decode_midi(music_data, file_path=file_path)

            # Case 4: Generate music using second prompt with longer sequence
            case "pushButton_GnerateMusicCase4_GeneratingMusicByGPTStyleMusicTransformer":
                file_path = "resources/maestro-v2.0.0/prompt2.midi"
                prompt = torch.tensor(encode_midi(file_path))
                generated_music = self.sample(prompt, seq_length=1200, temperature=1)
                music_data = generated_music[0].cpu().numpy()
                file_path = 'resources/maestro-v2.0.0/generatedMusicCase4.midi'
                decode_midi(music_data, file_path=file_path)

        # Log the final output file path of the generated music
        self.DownloadLogPopup.Append_Log("Generated Music saved in:\n" + file_path)

# Define a QThread subclass to handle model training asynchronously without freezing the UI
class TrainingGPTStyleMusicTransformerThread(QThread):

    # Signal to emit log messages to the UI (e.g., training progress updates)
    log_signal = pyqtSignal(str)

    # Signal to trigger visualization updates (e.g., after each epoch)
    display_signal = pyqtSignal(int)

    # Initialize the training thread with UI popup, data loader, model, and device
    def __init__(self, DownloadLogPopup, trainloader, model, device):
        # Call the parent QThread constructor
        super().__init__()

        # Reference to the popup window used for displaying logs
        self.DownloadLogPopup = DownloadLogPopup

        # DataLoader containing training data
        self.trainloader = trainloader

        # The transformer model to be trained
        self.model = model

        # Device on which training will run (e.g., 'cpu' or 'cuda')
        self.device = device

        # Learning rate for the optimizer
        self.lr = 0.0001

        # Adam optimizer for training the model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=self.lr)

        # Cross-entropy loss function, ignoring padding token (index 389)
        self.loss_func = torch.nn.CrossEntropyLoss(ignore_index=389)

        # Flag to allow user to interrupt training manually
        self._stop_requested = False

    # Method to request stopping the training loop
    def stop(self):
        # Set the stop flag to True
        self._stop_requested = True

        # Disable the cancel button in the UI to prevent further interaction
        self.DownloadLogPopup.cancel_button.setEnabled(False)

    # Main method that runs when the thread is started
    def run(self):
        try:
            # Emit initial log messages to indicate training has started
            self.log_signal.emit("Training thread started.")
            self.log_signal.emit(f"Train loader has {len(self.trainloader)} batches.")

            # Set the model to training mode
            self.model.train()

            # Loop over training epochs
            for i in range(1, 101):
                # Exit early if stop was requested
                if self._stop_requested:
                    break

                # Initialize total loss for the epoch
                tloss = 0.

                # Iterate over each batch in the training DataLoader
                for idx, (x, y) in enumerate(self.trainloader):
                    # Check again for stop request
                    if self._stop_requested:
                        # Emit log message and break inner loop
                        self.log_signal.emit("Training stopped by user.")
                        break

                    # Move input and target tensors to the appropriate device
                    x, y = x.to(self.device), y.to(self.device)

                    # Forward pass through the model
                    output = self.model(x)

                    # Compute cross-entropy loss between predicted logits and targets
                    loss = self.loss_func(output.view(-1, output.size(-1)), y.view(-1))

                    # Zero out gradients from previous step
                    self.optimizer.zero_grad()

                    # Backpropagate the loss
                    loss.backward()

                    # Clip gradients to prevent exploding gradients
                    nn.utils.clip_grad_norm_(self.model.parameters(), 1)

                    # Update model parameters
                    self.optimizer.step()

                    # Accumulate loss for reporting
                    tloss += loss.item()

                    # Emit log message for each batch
                    if (idx + 1) % 1 == 0:
                        self.log_signal.emit(f"Epoch {i}, Batch {idx + 1}: Loss = {loss.item():.4f}")

                # Emit average loss for the epoch
                self.log_signal.emit(f'Epoch {i} loss {tloss / (idx + 1)}')

            # Save the trained model's state dictionary to disk
            torch.save(self.model.state_dict(), f'resources/models/musicTransformer_.pth')

            # Emit a message indicating training is complete
            self.log_signal.emit("Training Finished.\nModel Saved.")

            # Scroll the log output to the bottom to show final messages
            self.DownloadLogPopup.log_output.moveCursor(QTextCursor.MoveOperation.End)
            self.DownloadLogPopup.log_output.ensureCursorVisible()

            # Process any pending UI events to refresh the interface
            QApplication.processEvents()

        except Exception as e:
            # Emit an error message if training fails
            self.log_signal.emit(f"Error during training: {str(e)}")

# Define a configuration class to store hyperparameters for the transformer model
class Config():
    # Constructor to initialize all configuration parameters
    def __init__(self):
        # Number of transformer blocks (layers) in the model
        self.n_layer = 6

        # Number of attention heads in each multi-head attention layer
        self.n_head = 8

        # Dimensionality of the embedding vectors and hidden states
        self.n_embd = 512

        # Size of the vocabulary (number of unique tokens)
        self.vocab_size = 390

        # Maximum sequence length (context window) the model can process
        self.block_size = 2048

        # Dropout probability applied to token and positional embeddings
        self.embd_pdrop = 0.1

        # Dropout probability applied to residual connections
        self.resid_pdrop = 0.1

        # Dropout probability applied to attention weights
        self.attn_pdrop = 0.1

# Define the Gaussian Error Linear Unit (GELU) activation function as a custom PyTorch module
class GELU(nn.Module):
    # Define the forward pass for the GELU activation
    # :param x: Input tensor to apply the activation function
    def forward(self, x):
        # Apply the GELU activation using the approximate formulation:
        # GELU(x) ≈ 0.5 * x * (1 + tanh(√(2/π) * (x + 0.044715 * x³)))
        return 0.5 * x * (
            1.0 + torch.tanh(
                math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0))
            )
        )

# Define a causal self-attention module for autoregressive sequence modeling
class CausalSelfAttention(nn.Module):
    # Constructor to initialize attention layers and configuration
    # :param config: Configuration object containing model hyperparameters
    def __init__(self, config):
        # Call the base class constructor to initialize nn.Module
        super().__init__()

        # Linear layer to compute concatenated queries, keys, and values from input embeddings
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)

        # Linear projection layer to transform attention output back to embedding space
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)

        # Dropout applied to attention weights for regularization
        self.attn_dropout = nn.Dropout(config.attn_pdrop)

        # Dropout applied to the final output of the attention block
        self.resid_dropout = nn.Dropout(config.resid_pdrop)

        # Register a lower-triangular causal mask to prevent attention to future tokens
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(config.block_size, config.block_size))
            .view(1, 1, config.block_size, config.block_size)
        )

        # Number of attention heads
        self.n_head = config.n_head

        # Embedding dimension
        self.n_embd = config.n_embd

    # Define the forward pass for causal self-attention
    # :param x: Input tensor of shape (batch_size, sequence_length, embedding_dim)
    def forward(self, x):
        # Extract batch size (B), sequence length (T), and embedding dimension (C)
        B, T, C = x.size()

        # Compute queries (q), keys (k), and values (v) by splitting the output of the linear layer
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)

        # Compute the head size (embedding dimension per head)
        hs = C // self.n_head

        # Reshape and transpose keys to shape (B, n_head, T, hs)
        k = k.view(B, T, self.n_head, hs).transpose(1, 2)

        # Reshape and transpose queries to shape (B, n_head, T, hs)
        q = q.view(B, T, self.n_head, hs).transpose(1, 2)

        # Reshape and transpose values to shape (B, n_head, T, hs)
        v = v.view(B, T, self.n_head, hs).transpose(1, 2)

        # Compute scaled dot-product attention scores
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))

        # Apply causal mask to prevent attending to future positions
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float('-inf'))

        # Apply softmax to obtain attention weights
        att = F.softmax(att, dim=-1)

        # Apply dropout to attention weights
        att = self.attn_dropout(att)

        # Compute the weighted sum of values using attention weights
        y = att @ v

        # Reshape and transpose the output back to (B, T, C)
        y = y.transpose(1, 2).contiguous().view(B, T, C)

        # Apply final projection and dropout
        y = self.resid_dropout(self.c_proj(y))

        # Return the attention output
        return y

# Define a single transformer block consisting of self-attention and feedforward sublayers
class Block(nn.Module):
    # Constructor to initialize the transformer block
    # :param config: Configuration object containing model hyperparameters
    def __init__(self, config):
        # Call the base class constructor to initialize nn.Module
        super().__init__()

        # First layer normalization before the self-attention sublayer
        self.ln_1 = nn.LayerNorm(config.n_embd)

        # Causal self-attention mechanism to capture temporal dependencies
        self.attn = CausalSelfAttention(config)

        # Second layer normalization before the feedforward sublayer
        self.ln_2 = nn.LayerNorm(config.n_embd)

        # Define the feedforward network using a ModuleDict for modularity
        self.mlp = nn.ModuleDict(dict(
            # Fully connected layer to expand dimensionality (typically 4x the embedding size)
            c_fc = nn.Linear(config.n_embd, 4 * config.n_embd),

            # Projection layer to reduce dimensionality back to embedding size
            c_proj = nn.Linear(4 * config.n_embd, config.n_embd),

            # Activation function (Gaussian Error Linear Unit)
            act = GELU(),

            # Dropout layer for regularization
            dropout = nn.Dropout(config.resid_pdrop),
        ))

        # Define the feedforward computation as a lambda function for cleaner forward pass
        m = self.mlp
        self.mlpf = lambda x: m.dropout(m.c_proj(m.act(m.c_fc(x))))

    # Define the forward pass through the transformer block
    # :param x: Input tensor of shape (batch_size, sequence_length, embedding_dim)
    def forward(self, x):
        # Apply layer normalization, followed by self-attention, and add residual connection
        x = x + self.attn(self.ln_1(x))

        # Apply second layer normalization, followed by feedforward network, and add residual connection
        x = x + self.mlpf(self.ln_2(x))

        # Return the output tensor
        return x

# Define the transformer-based language model class for music generation
class Model(nn.Module):
    # Constructor to initialize the model architecture
    # :param config: Configuration object containing model hyperparameters
    # :param device: Device on which the model will run (CPU or CUDA)
    def __init__(self, config, device):
        # Call the base class constructor to initialize nn.Module
        super().__init__()

        # Store the device for later use in forward pass
        self.device = device

        # Store the maximum sequence length (block size) from config
        self.block_size = config.block_size

        # Define the transformer architecture using a ModuleDict for modularity
        self.transformer = nn.ModuleDict(dict(
            # Token embedding layer: maps token indices to embedding vectors
            wte = nn.Embedding(config.vocab_size, config.n_embd),

            # Positional embedding layer: encodes position information
            wpe = nn.Embedding(config.block_size, config.n_embd),

            # Dropout layer for regularization on embeddings
            drop = nn.Dropout(config.embd_pdrop),

            # Stack of transformer blocks (multi-head attention + feedforward)
            h = nn.ModuleList([Block(config) for _ in range(config.n_layer)]),

            # Final layer normalization after all transformer blocks
            ln_f = nn.LayerNorm(config.n_embd),
        ))

        # Linear layer to project transformer output to vocabulary logits
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

        # Initialize projection weights in transformer blocks with scaled normal distribution
        for pn, p in self.named_parameters():
            if pn.endswith('c_proj.weight'):
                torch.nn.init.normal_(
                    p,
                    mean=0.0,
                    std=0.02 / math.sqrt(2 * config.n_layer)
                )

    # Define the forward pass of the model
    # :param idx: Input tensor of token indices with shape (batch_size, sequence_length)
    # :param targets: Optional target tensor for training (not used here)
    def forward(self, idx, targets=None):
        # Extract batch size (b) and sequence length (t) from input shape
        b, t = idx.size()

        # Create position indices for each token in the sequence
        pos = torch.arange(0, t, dtype=torch.long).unsqueeze(0).to(self.device)

        # Get token embeddings for input indices
        tok_emb = self.transformer.wte(idx)

        # Get positional embeddings for each position
        pos_emb = self.transformer.wpe(pos)

        # Add token and positional embeddings, then apply dropout
        x = self.transformer.drop(tok_emb + pos_emb)

        # Pass the input through each transformer block sequentially
        for block in self.transformer.h:
            x = block(x)

        # Apply final layer normalization
        x = self.transformer.ln_f(x)

        # Project the output to vocabulary logits using the language modeling head
        logits = self.lm_head(x)

        # Return the logits for each token position
        return logits
    

