import io
import sys
import contextlib
import os
from os.path import isfile, join
import time
import pickle
import shutil
import random
import tkinter as tk
import threading
import math
from copy import deepcopy
from collections import Counter
import json
import regex as re
from functools import lru_cache
from utilities.DeepLearningFoundationOperations import DownloadLogPopup, LogEmitter
from utilities.DLbyPyTorch import EarlyStop, DLbyPyTorch, PopupStream
from utilities.bpe import get_encoder, BPETokenizer
from utilities.ScrollableMessageBox import show_scrollable_message
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
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
    from PyQt6.QtGui import  QTextCursor   
    from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt, QUrl
    from PyQt6.QtWidgets import QMessageBox,QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QTextEdit,QScrollArea,QMainWindow,QApplication
except:
    print("You Should Install PyQt6 Library!")

# Define a class responsible for generating music in a mimicked style using the MuseGAN model.
# Inherits from QObject to integrate with Qt's signal-slot mechanism for UI interaction.
class GeneratingMimickedStyleMusicByMuseGAN(QObject):

    # Constructor method to initialize the class instance
    # Parameters:
    #   parent (QObject, optional): Parent object for Qt ownership hierarchy (default is None)
    def __init__(self, parent=None):     
        # Call the base class constructor to ensure proper QObject initialization
        super().__init__()

        # Set a fixed random seed for reproducibility of results across runs
        torch.manual_seed(0)

        # Create a log emitter instance to send log messages to the UI asynchronously
        self.log_emitter = LogEmitter()

        # Create a popup window to display logs during dataset loading, training, or generation
        self.DownloadLogPopup = DownloadLogPopup(
            # Connect the log emitter to the popup for real-time log updates
            self.log_emitter
        )

        # Placeholder for the dataset object (to be assigned later)
        self.dataset = None

        # Placeholder for the data loader (used to iterate over the dataset)
        self.loader = None

        # Determine the computation device: use GPU if available, otherwise fallback to CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Placeholder for the generator model (to be initialized later)
        self.generator = None

        # Placeholder for the critic (discriminator) model (to be initialized later)
        self.critic = None

    # Method to load the MIDI dataset from a predefined file path
    def LoadData(self):
        # Check if the dataset file exists at the specified path
        if os.path.exists("resources/Jsb16thSeparated.npz"):
            # If the file exists, initialize the dataset using the MidiDataset class
            self.dataset = MidiDataset('resources/Jsb16thSeparated.npz')

            # Show an informational message box to notify the user that the dataset was successfully loaded
            QMessageBox.information(
                None,                # No parent widget for the message box
                "Dataset Ready",     # Title of the message box
                "Dataset Loaded."    # Message content
            )
        else:
            # If the dataset file is not found, show a warning message box to inform the user
            QMessageBox.warning(
                None,                # No parent widget for the message box
                "No Dataset",        # Title of the warning box
                "Dataset not found." # Message content
            )

    # Method to prepare the data loader from the loaded dataset
    def PrepareData(self):
        # Check if the dataset has been loaded; if not, alert the user and exit the method
        if self.dataset is None:
            # Display a warning message box indicating that the dataset must be loaded first
            QMessageBox.warning(
                None,                  # No parent widget
                "No Dataset",          # Title of the warning dialog
                "First load the Dataset."  # Message content
            )
            return  # Exit the method early since there's no dataset to prepare

        # Create a DataLoader to iterate over the dataset in batches
        self.loader = DataLoader(
            self.dataset,     # The dataset to load from
            batch_size=64,    # Number of samples per batch
            shuffle=True,     # Shuffle the data at every epoch
            drop_last=True    # Drop the last incomplete batch if it's smaller than batch_size
        )

        # Display an informational message box confirming successful data preparation
        QMessageBox.information(
            None,                    # No parent widget
            "Data Prepared",         # Title of the message box
            "Data Prepared Successfully."  # Message content
        )

    # Method to convert the first sample from the dataset into a MIDI music file
    def ConvertDataToMusic(self):
        # Check if the data loader has been prepared; if not, alert the user and exit
        if self.loader is None:
            QMessageBox.warning(
                None,                         # No parent widget
                "Dataset not ready",          # Title of the warning dialog
                "First Prepare the Data."     # Message content
            )
            return  # Exit early since data is not ready

        # Create a temporary directory to store the output MIDI file (if it doesn't already exist)
        os.makedirs("temp", exist_ok=True)

        # Retrieve the first song (tensor) from the dataset
        first_song = self.dataset[0]

        # Create a new music21 Score object to hold all parts (instrument tracks)
        parts = stream.Score()

        # Add a metronome mark to set the tempo (66 BPM)
        parts.append(tempo.MetronomeMark(number=66))

        # Convert the multi-dimensional piano roll into note indices using argmax across pitch axis
        max_pitches = np.argmax(first_song, axis=-1)

        # Reshape the note matrix into (32 time steps, 4 tracks)
        midi_note_score = max_pitches.reshape([2 * 16, 4])

        # Iterate over each of the 4 instrument tracks
        for i in range(4):
            # Initialize the first note value for comparison
            last_x = int(midi_note_score[:, i][0])

            # Create a new Part (instrument line) for this track
            s = stream.Part()

            # Initialize duration accumulator
            dur = 0

            # Iterate over each time step in the track
            for idx, x in enumerate(midi_note_score[:, i]):
                x = int(x)  # Ensure note value is an integer

                # If the note changes or it's the start of a new beat group, finalize the previous note
                if (x != last_x or idx % 4 == 0) and idx > 0:
                    n = note.Note(last_x)                  # Create a note with the previous pitch
                    n.duration = duration.Duration(dur)    # Assign accumulated duration
                    s.append(n)                            # Add the note to the part
                    dur = 0                                # Reset duration counter

                # Update the last note and increment duration
                last_x = x
                dur += 0.25  # Each time step represents a sixteenth note (1/4 of a beat)

            # Add the final note after the loop ends
            n = note.Note(last_x)
            n.duration = duration.Duration(dur)
            s.append(n)

            # Append the completed part to the score
            parts.append(s)

        # Write the complete score to a MIDI file in the temp directory
        parts.write("midi", "temp/first_song.midi")

        # Notify the user that the conversion was successful and the file was saved
        QMessageBox.information(
            None, 
            "Data Converted", 
            "Data Converted to A Music file Saved in: temp/first_song.midi"
        )

    # Method to create and initialize the generator and critic models for MuseGAN
    def CreateModels(self):

        # Nested function to initialize weights of model layers
        # Parameters:
        #   layer (nn.Module): The layer to initialize
        #   mean (float): Mean of the normal distribution for weight initialization (default: 0.0)
        #   std (float): Standard deviation of the normal distribution (default: 0.02)
        def init_weights(layer, mean=0.0, std=0.02):
            # Initialize weights for 3D convolutional and transposed convolutional layers
            if isinstance(layer, (nn.Conv3d, nn.ConvTranspose2d)):
                nn.init.normal_(layer.weight, mean, std)

            # Initialize weights and biases for linear and batch normalization layers
            elif isinstance(layer, (nn.Linear, nn.BatchNorm2d)):
                nn.init.normal_(layer.weight, mean, std)
                nn.init.constant_(layer.bias, 0)

        # Check if the generator or critic models have not been created yet
        if self.generator is None or self.critic is None:
            # Instantiate the MuseGAN generator model with specified architecture parameters
            generator = MuseGenerator(
                z_dimension=32,       # Dimensionality of the input noise vector
                hid_channels=1024,    # Number of hidden channels in convolutional layers
                hid_features=1024,    # Number of hidden features in fully connected layers
                out_channels=1        # Number of output channels (e.g., for grayscale piano rolls)
            ).to(self.device)         # Move the model to the selected device (CPU or CUDA)

            # Instantiate the MuseGAN critic (discriminator) model with its architecture
            critic = MuseCritic(
                hid_channels=128,     # Number of hidden channels in convolutional layers
                hid_features=1024,    # Number of hidden features in fully connected layers
                out_features=1        # Output size (e.g., real/fake score)
            ).to(self.device)         # Move the model to the selected device

            # Apply the weight initialization function to the generator and assign it to the instance
            self.generator = generator.apply(init_weights)

            # Apply the weight initialization function to the critic and assign it to the instance
            self.critic = critic.apply(init_weights)

            # Notify the user that the models were successfully created
            QMessageBox.information(
                None,
                "Models Created",
                "Models created successfully."
            )
        else:
            # If models already exist, inform the user that no action is needed
            QMessageBox.information(
                None,
                "Models Created",
                "Models already created."
            )

    # Method to initiate the training process for the MuseGAN model
    def TrainModel(self):
        # Check if the data loader has been prepared
        if self.loader is None:
            # Display a warning message if the dataset has not been prepared
            QMessageBox.warning(
                None, 
                "Data Not Ready", 
                "First Prepare the Data."
            )

        # Check if the generator and critic models have been created
        elif self.critic is None or self.generator is None:
            # Display a warning message if the models are missing
            QMessageBox.warning(
                None, 
                "Models Not Found", 
                "Please create the models first."
            )

        # Proceed only if both the dataset and models are ready
        else:
            # Enable the cancel button in the log popup to allow user to interrupt training
            self.DownloadLogPopup.cancel_button.setEnabled(True)

            # Display the log popup window to show training progress
            self.DownloadLogPopup.show()

            # Append an initial log message indicating that training has started
            self.DownloadLogPopup.Append_Log("Training model...\nPlease wait.")

            # Create a new thread to run the training process asynchronously
            self.training_thread = TrainingMuseGANThread(
                self.DownloadLogPopup,  # Log popup for displaying training progress
                self.loader,            # DataLoader providing training batches
                self.generator,         # Generator model to be trained
                self.critic,            # Critic (discriminator) model to be trained
                self.device             # Device (CPU or CUDA) to perform training on
            )

            # Connect the training thread's log signal to the log popup's append method
            self.training_thread.log_signal.connect(self.DownloadLogPopup.Append_Log)

            # Connect the cancel button to the training thread's stop method for user interruption
            self.DownloadLogPopup.cancel_button.clicked.connect(self.training_thread.stop)

            # Start the training thread to begin the model training process
            self.training_thread.start()

    # Method to convert model output (e.g., piano roll) into a music21 Score object representing a MIDI composition
    # Parameters:
    #   output (np.ndarray): The model-generated output, typically a 4D array representing notes over time and tracks
    #   n_tracks (int): Number of instrument tracks (default: 4)
    #   n_bars (int): Number of bars in the composition (default: 2)
    #   n_steps_per_bar (int): Number of time steps per bar (default: 16)
    def convert_to_midi(self, output, n_tracks=4, n_bars=2, n_steps_per_bar=16):

        # Nested helper function to convert multi-dimensional output into discrete note indices
        def binarise_output(output):
            # Use argmax to select the most active pitch at each time step
            max_pitches = np.argmax(output, axis=-1)
            return max_pitches

        # Create a new music21 Score object to hold all instrument parts
        parts = stream.Score()

        # Add a tempo marking to the score (66 beats per minute)
        parts.append(tempo.MetronomeMark(number=66))

        # Convert the model output into a 2D array of note indices
        max_pitches = binarise_output(output)

        # Reshape each sample in the batch into a 2D piano roll and stack them vertically
        midi_note_score = np.vstack([
            max_pitches[i].reshape([n_bars * n_steps_per_bar, n_tracks]) for i in range(len(output))
        ])

        # Iterate over each track (instrument line)
        for i in range(n_tracks):
            # Initialize the first note value for comparison
            last_x = int(midi_note_score[:, i][0])

            # Create a new Part object for this track
            s = stream.Part()

            # Initialize duration accumulator
            dur = 0

            # Iterate over each time step in the track
            for idx, x in enumerate(midi_note_score[:, i]):
                x = int(x)  # Ensure note value is an integer

                # If the note changes or it's the start of a new beat group, finalize the previous note
                if (x != last_x or idx % 4 == 0) and idx > 0:
                    n = note.Note(last_x)                  # Create a note with the previous pitch
                    n.duration = duration.Duration(dur)    # Assign accumulated duration
                    s.append(n)                            # Add the note to the part
                    dur = 0                                # Reset duration counter

                # Update the last note and increment duration
                last_x = x
                dur += 0.25  # Each time step represents a sixteenth note (1/4 of a beat)

            # Add the final note after the loop ends
            n = note.Note(last_x)
            n.duration = duration.Duration(dur)
            s.append(n)

            # Append the completed part to the score
            parts.append(s)

        # Return the complete Score object representing the MIDI composition
        return parts

    # Method to generate a new song using the trained MuseGAN generator model
    def GenerateSong(self):
        # Check if the generator model has been created
        if self.generator is None:
            # Warn the user if the model has not been instantiated
            QMessageBox.warning(
                None,
                "Model Not Found",
                "Please create the model first."
            )
            return  # Exit early since the model is missing

        # Check if the trained generator model file exists
        if not os.path.exists('resources/models/MuseGAN_G.pth'):
            # Warn the user if the model has not been trained and saved
            QMessageBox.warning(
                None,
                "Model Not Trained",
                "Please Create, Train and Save the model first."
            )
            return  # Exit early since the model weights are unavailable

        # Create a temporary directory to store the generated MIDI file
        os.makedirs("temp", exist_ok=True)

        # Load the trained generator model weights from file
        self.generator.load_state_dict(
            torch.load('resources/models/MuseGAN_G.pth', map_location=torch.device('cpu'))
        )

        # Define the number of musical pieces (samples) to generate
        num_pieces = 5

        # Generate random latent vectors for each musical component
        chords = torch.rand(num_pieces, 32).to(self.device)       # Chord progression vector
        style = torch.rand(num_pieces, 32).to(self.device)        # Style vector
        melody = torch.rand(num_pieces, 4, 32).to(self.device)    # Melody vector (4 tracks)
        groove = torch.rand(num_pieces, 4, 32).to(self.device)    # Groove vector (4 tracks)

        # Pass the latent vectors through the generator to produce music predictions
        preds = self.generator(chords, style, melody, groove).detach()

        # Convert the generated output into a music21 Score object (MIDI representation)
        music_data = self.convert_to_midi(preds.cpu().numpy())

        # Define the output path for the generated MIDI file
        audio_path = 'temp/MuseGAN_song.midi'

        # Write the Score object to a MIDI file
        music_data.write('midi', audio_path)

        # Inform the user that the song has been successfully generated and saved
        QMessageBox.information(
            None,
            "Song Generated",
            "Song Generated and Saved in:\n" + audio_path
        )

# Define a QThread subclass to handle MuseGAN training in a separate thread
class TrainingMuseGANThread(QThread):

    # Signal to emit log messages to the UI (e.g., training progress updates)
    log_signal = pyqtSignal(str)

    # Signal to trigger visualization updates (e.g., after each epoch)
    display_signal = pyqtSignal(int)

    # Initialize the training thread with UI popup, data loader, model, and device
    def __init__(self, DownloadLogPopup, loader, generator, critic, device):
        # Call the parent QThread constructor
        super().__init__()

        # Reference to the popup window used for displaying logs
        self.DownloadLogPopup = DownloadLogPopup

        # DataLoader providing batches of training data
        self.loader = loader

        # Generator model to be trained
        self.generator = generator

        # Critic (discriminator) model to be trained
        self.critic = critic

        # Device on which training will run (e.g., 'cpu' or 'cuda')
        self.device = device

        # Learning rate for both optimizers
        self.lr = 0.001

        # Optimizer for the generator using Adam optimizer
        self.g_optimizer = torch.optim.Adam(generator.parameters(), lr=self.lr, betas=(0.5, 0.9))

        # Optimizer for the critic using Adam optimizer
        self.c_optimizer = torch.optim.Adam(critic.parameters(), lr=self.lr, betas=(0.5, 0.9))

        # Batch size for training
        self.batch_size = 64

        # Number of critic updates per generator update
        self.repeat = 5

        # Frequency (in epochs) to emit display updates
        self.display_step = 2

        # Total number of training epochs
        self.epochs = 500

        # Interpolation factor for gradient penalty calculation
        self.alpha = torch.rand((self.batch_size, 1, 1, 1, 1)).requires_grad_().to(device)

        # Gradient penalty module for WGAN-GP
        self.gp = GradientPenalty()

        # Flag to allow user to interrupt training manually
        self._stop_requested = False

    # Generate random latent vectors for chords, style, melody, and groove
    def noise(self):
        # Random latent vector for chords
        chords = torch.randn(self.batch_size, 32).to(self.device)

        # Random latent vector for style
        style = torch.randn(self.batch_size, 32).to(self.device)

        # Random latent vector for melody (4 tracks)
        melody = torch.randn(self.batch_size, 4, 32).to(self.device)

        # Random latent vector for groove (4 tracks)
        groove = torch.randn(self.batch_size, 4, 32).to(self.device)

        # Return all latent vectors
        return chords, style, melody, groove

    # Define the loss function for adversarial training (Wasserstein loss)
    def loss_fn(self, pred, target):
        # Return the negative mean of the element-wise product
        return -torch.mean(pred * target)

    # Train the model for one full epoch
    def train_epoch(self):
        # Initialize epoch-level generator and critic loss accumulators
        e_gloss = 0
        e_closs = 0

        # Iterate over each batch of real data
        for real in self.loader:
            # Exit early if stop was requested
            if self._stop_requested:
                break

            # Move real data to the selected device
            real = real.to(self.device)

            # Train the critic multiple times per generator update
            for _ in range(self.repeat):
                # Check again for stop request
                if self._stop_requested:
                    # Emit log message and break inner loop
                    self.log_signal.emit("Training stopped by user.")
                    break

                # Generate random latent vectors
                chords, style, melody, groove = self.noise()

                # Zero out gradients for the critic
                self.c_optimizer.zero_grad()

                # Generate fake samples without tracking gradients
                with torch.no_grad():
                    fake = self.generator(chords, style, melody, groove).detach()

                # Interpolate between real and fake samples for gradient penalty
                realfake = self.alpha * real + (1 - self.alpha) * fake

                # Compute critic predictions for fake, real, and interpolated samples
                fake_pred = self.critic(fake)
                real_pred = self.critic(real)
                realfake_pred = self.critic(realfake)

                # Compute loss for fake samples (should be classified as -1)
                fake_loss = self.loss_fn(fake_pred, -torch.ones_like(fake_pred))

                # Compute loss for real samples (should be classified as +1)
                real_loss = self.loss_fn(real_pred, torch.ones_like(real_pred))

                # Compute gradient penalty for interpolated samples
                penalty = self.gp(realfake, realfake_pred)

                # Total critic loss with gradient penalty
                closs = fake_loss + real_loss + 10 * penalty

                # Backpropagate critic loss
                closs.backward(retain_graph=True)

                # Update critic weights
                self.c_optimizer.step()

                # Accumulate average critic loss
                e_closs += closs.item() / (self.repeat * len(self.loader))

            # Train the generator once per batch
            self.g_optimizer.zero_grad()  # Reset gradients for generator

            # Generate new random latent vectors
            chords, style, melody, groove = self.noise()

            # Generate fake samples from the generator
            fake = self.generator(chords, style, melody, groove)

            # Get critic's prediction on the fake samples
            fake_pred = self.critic(fake)

            # Compute generator loss (wants critic to classify fake as real)
            gloss = self.loss_fn(fake_pred, torch.ones_like(fake_pred))

            # Backpropagate generator loss
            gloss.backward()

            # Update generator weights
            self.g_optimizer.step()

            # Accumulate average generator loss
            e_gloss += gloss.item() / len(self.loader)

        # Return average generator and critic losses for the epoch
        return e_gloss, e_closs

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
            self.log_signal.emit(f"Train loader has {len(self.loader)} batches.")

            # Loop through all training epochs
            for epoch in range(1, self.epochs + 1):
                # Exit early if stop was requested
                if self._stop_requested:
                    break

                # Train for one epoch and get generator and critic losses
                e_gloss, e_closs = self.train_epoch()

                # Emit log message every few epochs
                if epoch % self.display_step == 0:
                    self.log_signal.emit(f"Epoch {epoch}, G loss {e_gloss} C loss {e_closs}")

            # Save the trained generator model to disk
            torch.save(self.generator.state_dict(), 'resources/models/MuseGAN_G_.pth')

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

# Define a custom PyTorch module to reshape tensors within a neural network
class Reshape(nn.Module):

    # Constructor to initialize the target shape
    # Parameters:
    #   shape (tuple): The desired shape (excluding batch size) to reshape input tensors into
    def __init__(self, shape):
        # Call the base class constructor
        super().__init__()

        # Store the target shape as an instance variable
        self.shape = shape

    # Forward method to apply the reshape operation during the forward pass
    # Parameters:
    #   x (Tensor): Input tensor of shape (batch_size, ...)
    def forward(self, x):
        # Reshape the input tensor to (batch_size, *self.shape)
        return x.view(x.size(0), *self.shape)

# Define a neural network module to model temporal structure in latent space for MuseGAN
class TemporalNetwork(nn.Module):

    # Constructor to initialize the temporal network architecture
    # Parameters:
    #   z_dimension (int): Dimensionality of the input latent vector
    #   hid_channels (int): Number of hidden channels used in intermediate convolution layers
    #   n_bars (int): Number of musical bars to generate (affects output shape)
    def __init__(self, z_dimension=32, hid_channels=1024, n_bars=2):
        # Call the base class constructor
        super().__init__()

        # Store the number of bars as an instance variable
        self.n_bars = n_bars

        # Define the sequential network architecture
        self.net = nn.Sequential(
            # Reshape input from (batch_size, z_dimension) to (batch_size, z_dimension, 1, 1)
            Reshape(shape=[z_dimension, 1, 1]),

            # First transposed convolution to expand temporal dimension to 2
            nn.ConvTranspose2d(
                in_channels=z_dimension,     # Input channels from latent vector
                out_channels=hid_channels,   # Output channels for hidden representation
                kernel_size=(2, 1),          # Expand height to 2 (temporal axis)
                stride=(1, 1),               # No stride
                padding=0                    # No padding
            ),

            # Normalize the hidden channels
            nn.BatchNorm2d(hid_channels),

            # Apply ReLU activation
            nn.ReLU(inplace=True),

            # Second transposed convolution to expand temporal dimension to n_bars
            nn.ConvTranspose2d(
                in_channels=hid_channels,    # Input from previous layer
                out_channels=z_dimension,    # Output back to latent dimension
                kernel_size=(self.n_bars - 1, 1),  # Expand height to n_bars
                stride=(1, 1),               # No stride
                padding=0                    # No padding
            ),

            # Normalize the output channels
            nn.BatchNorm2d(z_dimension),

            # Apply ReLU activation
            nn.ReLU(inplace=True),

            # Reshape output from (batch_size, z_dimension, n_bars, 1) to (batch_size, z_dimension, n_bars)
            Reshape(shape=[z_dimension, self.n_bars])
        )

    # Forward pass through the temporal network
    # Parameters:
    #   x (Tensor): Input tensor of shape (batch_size, z_dimension)
    # Returns:
    #   Tensor of shape (batch_size, z_dimension, n_bars)
    def forward(self, x):
        return self.net(x)

# Define the MuseCritic class, a 3D convolutional discriminator used in MuseGAN
class MuseCritic(nn.Module):

    # Constructor to initialize the critic architecture
    def __init__(self, hid_channels=128, hid_features=1024,
                 out_features=1, n_tracks=4, n_bars=2, n_steps_per_bar=16,
                 n_pitches=84):
        # Call the base class constructor
        super().__init__()

        # Store the number of tracks (input channels)
        self.n_tracks = n_tracks

        # Store the number of bars in the input
        self.n_bars = n_bars

        # Store the number of time steps per bar
        self.n_steps_per_bar = n_steps_per_bar

        # Store the number of pitch bins (height of piano roll)
        self.n_pitches = n_pitches

        # Determine the number of input features for the first linear layer after flattening
        in_features = 4 * hid_channels if n_bars == 2 else 12 * hid_channels

        # Define the sequential model architecture
        self.seq = nn.Sequential(

            # 1st Conv3D layer: reduce bar dimension from 2 to 1
            nn.Conv3d(
                in_channels=self.n_tracks,     # Input channels = number of tracks
                out_channels=hid_channels,     # Output channels = hidden channels
                kernel_size=(2, 1, 1),          # Kernel spans 2 bars
                stride=(1, 1, 1),               # No stride
                padding=0                       # No padding
            ),

            # LeakyReLU activation with negative slope 0.3
            nn.LeakyReLU(0.3, inplace=True),

            # 2nd Conv3D layer: further reduce bar dimension to 1
            nn.Conv3d(
                in_channels=hid_channels,
                out_channels=hid_channels,
                kernel_size=(self.n_bars - 1, 1, 1),  # Kernel spans remaining bar dimension
                stride=(1, 1, 1),
                padding=0
            ),

            # LeakyReLU activation
            nn.LeakyReLU(0.3, inplace=True),

            # 3rd Conv3D layer: reduce pitch dimension from 84 to 7 (via 12-step stride)
            nn.Conv3d(
                in_channels=hid_channels,
                out_channels=hid_channels,
                kernel_size=(1, 1, 12),         # Kernel spans 12 pitches
                stride=(1, 1, 12),              # Stride matches kernel to downsample
                padding=0
            ),

            # LeakyReLU activation
            nn.LeakyReLU(0.3, inplace=True),

            # 4th Conv3D layer: reduce pitch dimension from 7 to 1
            nn.Conv3d(
                in_channels=hid_channels,
                out_channels=hid_channels,
                kernel_size=(1, 1, 7),          # Kernel spans remaining pitch dimension
                stride=(1, 1, 7),               # Stride matches kernel
                padding=0
            ),

            # LeakyReLU activation
            nn.LeakyReLU(0.3, inplace=True),

            # 5th Conv3D layer: reduce time dimension from 16 to 8
            nn.Conv3d(
                in_channels=hid_channels,
                out_channels=hid_channels,
                kernel_size=(1, 2, 1),          # Kernel spans 2 time steps
                stride=(1, 2, 1),               # Stride of 2 halves the time dimension
                padding=0
            ),

            # LeakyReLU activation
            nn.LeakyReLU(0.3, inplace=True),

            # 6th Conv3D layer: reduce time dimension from 8 to 4
            nn.Conv3d(
                in_channels=hid_channels,
                out_channels=hid_channels,
                kernel_size=(1, 2, 1),          # Same as previous layer
                stride=(1, 2, 1),
                padding=0
            ),

            # LeakyReLU activation
            nn.LeakyReLU(0.3, inplace=True),

            # 7th Conv3D layer: reduce time dimension from 4 to 2
            nn.Conv3d(
                in_channels=hid_channels,
                out_channels=2 * hid_channels,  # Double the number of channels
                kernel_size=(1, 4, 1),          # Kernel spans 4 time steps
                stride=(1, 2, 1),               # Stride of 2
                padding=(0, 1, 0)               # Padding to preserve shape
            ),

            # LeakyReLU activation
            nn.LeakyReLU(0.3, inplace=True),

            # 8th Conv3D layer: reduce time dimension from 2 to 1
            nn.Conv3d(
                in_channels=2 * hid_channels,
                out_channels=4 * hid_channels,  # Expand channels again
                kernel_size=(1, 3, 1),          # Kernel spans 3 time steps
                stride=(1, 2, 1),               # Stride of 2
                padding=(0, 1, 0)               # Padding to preserve shape
            ),

            # LeakyReLU activation
            nn.LeakyReLU(0.3, inplace=True),

            # Flatten the 5D tensor to 2D for fully connected layers
            nn.Flatten(),

            # Fully connected layer to project to hidden feature space
            nn.Linear(
                in_features=in_features,        # Input features from flattened conv output
                out_features=hid_features       # Hidden layer size
            ),

            # LeakyReLU activation
            nn.LeakyReLU(0.3, inplace=True),

            # Final linear layer to produce a single scalar output (real/fake score)
            nn.Linear(
                in_features=hid_features,
                out_features=out_features       # Output size (typically 1)
            )
        )

    # Forward pass through the critic network
    def forward(self, x):
        # Pass input through the sequential model
        return self.seq(x)

# Define the BarGenerator class, responsible for generating a single bar of music in MuseGAN
class BarGenerator(nn.Module):

    # Constructor to initialize the bar generator architecture
    def __init__(self, z_dimension=32, hid_features=1024, hid_channels=512,
                 out_channels=1, n_steps_per_bar=16, n_pitches=84):
        # Call the base class constructor
        super().__init__()

        # Store the number of time steps per bar
        self.n_steps_per_bar = n_steps_per_bar

        # Store the number of pitch bins
        self.n_pitches = n_pitches

        # Define the sequential network architecture
        self.net = nn.Sequential(

            # Fully connected layer to project concatenated latent vectors into hidden feature space
            nn.Linear(
                in_features=4 * z_dimension,  # Input: concatenated latent vectors (chords, style, melody, groove)
                out_features=hid_features     # Output: flattened feature vector
            ),

            # Batch normalization for 1D features
            nn.BatchNorm1d(
                num_features=hid_features     # Normalize across the hidden feature dimension
            ),

            # ReLU activation function
            nn.ReLU(inplace=True),

            # Reshape to 4D tensor for ConvTranspose2D: (batch_size, channels, height, width)
            Reshape(shape=[hid_channels, hid_features // hid_channels, 1]),

            # 1st transposed convolution to double the height (time dimension)
            nn.ConvTranspose2d(
                in_channels=hid_channels,     # Input channels
                out_channels=hid_channels,    # Output channels remain the same
                kernel_size=(2, 1),           # Expand height by 2
                stride=(2, 1),                # Stride of 2 in height, 1 in width
                padding=0                     # No padding
            ),

            # Batch normalization for 2D features
            nn.BatchNorm2d(
                num_features=hid_channels     # Normalize across output channels
            ),

            # ReLU activation
            nn.ReLU(inplace=True),

            # 2nd transposed convolution to double the height again
            nn.ConvTranspose2d(
                in_channels=hid_channels,         # Input channels
                out_channels=hid_channels // 2,   # Reduce channels by half
                kernel_size=(2, 1),               # Expand height by 2
                stride=(2, 1),                    # Stride of 2 in height
                padding=0                         # No padding
            ),

            # Batch normalization
            nn.BatchNorm2d(
                num_features=hid_channels // 2    # Normalize across reduced channels
            ),

            # ReLU activation
            nn.ReLU(inplace=True),

            # 3rd transposed convolution to double the height again
            nn.ConvTranspose2d(
                in_channels=hid_channels // 2,    # Input channels
                out_channels=hid_channels // 2,   # Keep channels the same
                kernel_size=(2, 1),               # Expand height by 2
                stride=(2, 1),                    # Stride of 2 in height
                padding=0                         # No padding
            ),

            # Batch normalization
            nn.BatchNorm2d(
                num_features=hid_channels // 2
            ),

            # ReLU activation
            nn.ReLU(inplace=True),

            # 4th transposed convolution to expand width (pitch dimension) from 1 to 7
            nn.ConvTranspose2d(
                in_channels=hid_channels // 2,    # Input channels
                out_channels=hid_channels // 2,   # Keep channels the same
                kernel_size=(1, 7),               # Expand width by 7
                stride=(1, 7),                    # Stride of 7 in width
                padding=0                         # No padding
            ),

            # Batch normalization
            nn.BatchNorm2d(
                num_features=hid_channels // 2
            ),

            # ReLU activation
            nn.ReLU(inplace=True),

            # 5th transposed convolution to expand width from 7 to 84 (final pitch dimension)
            nn.ConvTranspose2d(
                in_channels=hid_channels // 2,    # Input channels
                out_channels=out_channels,        # Final output channels (e.g., 1 for grayscale)
                kernel_size=(1, 12),              # Expand width by 12
                stride=(1, 12),                   # Stride of 12 in width
                padding=0                         # No padding
            ),

            # Final reshape to match piano roll format: (batch_size, 1, 1, time, pitch)
            Reshape([
                1,                                # Single track/channel
                1,                                # Single bar
                self.n_steps_per_bar,             # Time steps per bar
                self.n_pitches                    # Number of pitches
            ])
        )

    # Forward pass through the bar generator
    def forward(self, x):
        # Pass input through the sequential network
        return self.net(x)

# Define a custom PyTorch module to compute the gradient penalty for WGAN-GP
class GradientPenalty(nn.Module):

    # Constructor for the GradientPenalty module
    def __init__(self):
        # Call the base class constructor
        super().__init__()

    # Forward method to compute the gradient penalty
    # Parameters:
    #   inputs (Tensor): Interpolated samples between real and fake data
    #   outputs (Tensor): Critic's predictions for the interpolated samples
    def forward(self, inputs, outputs):
        # Compute gradients of outputs with respect to inputs
        grad = torch.autograd.grad(
            inputs=inputs,                          # Inputs to differentiate with respect to
            outputs=outputs,                        # Outputs to compute gradients of
            grad_outputs=torch.ones_like(outputs),  # Gradient of outputs (dL/doutputs = 1)
            create_graph=True,                      # Retain graph for higher-order gradients
            retain_graph=True                       # Retain computation graph for reuse
        )[0]  # Extract the gradient tensor from the returned tuple

        # Flatten the gradients per sample and compute L2 norm across features
        grad_ = torch.norm(
            grad.view(grad.size(0), -1),  # Reshape to (batch_size, -1)
            p=2,                          # Use L2 norm
            dim=1                         # Compute norm across features
        )

        # Compute the gradient penalty: mean squared deviation from unit norm
        penalty = torch.mean((1. - grad_) ** 2)

        # Return the scalar penalty value
        return penalty

# Define the MuseGenerator class, the main generator model in MuseGAN
class MuseGenerator(nn.Module):

    # Constructor to initialize the generator architecture
    def __init__(self, z_dimension=32, hid_channels=1024,
                 hid_features=1024, out_channels=1, n_tracks=4,
                 n_bars=2, n_steps_per_bar=16, n_pitches=84):
        # Call the base class constructor
        super().__init__()

        # Store number of instrument tracks
        self.n_tracks = n_tracks

        # Store number of bars to generate
        self.n_bars = n_bars

        # Store number of time steps per bar
        self.n_steps_per_bar = n_steps_per_bar

        # Store number of pitch bins
        self.n_pitches = n_pitches

        # Temporal network to process chord latent vector across bars
        self.chords_network = TemporalNetwork(
            z_dimension=z_dimension,        # Input latent dimension
            hid_channels=hid_channels,      # Hidden channels for transposed conv layers
            n_bars=n_bars                   # Number of bars to generate
        )

        # Dictionary of temporal networks for each track's melody input
        self.melody_networks = nn.ModuleDict({})
        for n in range(self.n_tracks):
            # Add a TemporalNetwork for each track's melody vector
            self.melody_networks.add_module(
                "melodygen_" + str(n),
                TemporalNetwork(
                    z_dimension=z_dimension,
                    hid_channels=hid_channels,
                    n_bars=n_bars
                )
            )

        # Dictionary of bar generators for each track
        self.bar_generators = nn.ModuleDict({})
        for n in range(self.n_tracks):
            # Add a BarGenerator for each track
            self.bar_generators.add_module(
                "bargen_" + str(n),
                BarGenerator(
                    z_dimension=z_dimension,               # Input latent dimension
                    hid_features=hid_features,             # Hidden features in FC layer
                    hid_channels=hid_channels // 2,        # Reduced hidden channels
                    out_channels=out_channels,             # Output channels (e.g., 1)
                    n_steps_per_bar=n_steps_per_bar,       # Time resolution
                    n_pitches=n_pitches                    # Pitch resolution
                )
            )

    # Forward pass to generate a multi-track, multi-bar piano roll
    # Parameters:
    #   chords (Tensor): Latent vectors for chord progression (batch_size, z_dim)
    #   style (Tensor): Latent vectors for style (batch_size, z_dim)
    #   melody (Tensor): Latent vectors for melody (batch_size, n_tracks, z_dim)
    #   groove (Tensor): Latent vectors for groove (batch_size, n_tracks, z_dim)
    def forward(self, chords, style, melody, groove):
        # Process chord latent vector through temporal network → (batch_size, z_dim, n_bars)
        chord_outs = self.chords_network(chords)

        # List to collect generated bars
        bar_outs = []

        # Loop over each bar
        for bar in range(self.n_bars):
            # List to collect generated tracks for this bar
            track_outs = []

            # Extract chord vector for current bar → (batch_size, z_dim)
            chord_out = chord_outs[:, :, bar]

            # Style vector is shared across tracks
            style_out = style

            # Loop over each track
            for track in range(self.n_tracks):
                # Extract melody vector for this track → (batch_size, z_dim)
                melody_in = melody[:, track, :]

                # Process melody through its temporal network and extract current bar
                melody_out = self.melody_networks["melodygen_" + str(track)](melody_in)[:, :, bar]

                # Extract groove vector for this track → (batch_size, z_dim)
                groove_out = groove[:, track, :]

                # Concatenate all latent components → (batch_size, 4 * z_dim)
                z = torch.cat([chord_out, style_out, melody_out, groove_out], dim=1)

                # Generate piano roll for this track and bar → (batch_size, 1, 1, time, pitch)
                track_outs.append(self.bar_generators["bargen_" + str(track)](z))

            # Concatenate all tracks along track dimension → (batch_size, n_tracks, 1, time, pitch)
            track_out = torch.cat(track_outs, dim=1)

            # Append this bar's output to the bar list
            bar_outs.append(track_out)

        # Concatenate all bars along bar dimension → (batch_size, n_tracks, n_bars, time, pitch)
        out = torch.cat(bar_outs, dim=2)

        # Return the full piano roll tensor
        return out

# Define a custom PyTorch Dataset for loading LPD (Lakh Pianoroll Dataset) data
class LPDDataset(Dataset):

    # Constructor to initialize the dataset from a .npz file
    # Parameters:
    #   path (str): Path to the .npz file containing the dataset
    def __init__(self, path):
        # Load the .npz file using NumPy, allowing pickled objects and byte encoding
        dataset = np.load(path, allow_pickle=True, encoding="bytes")

        # Extract the binary array from the loaded dataset (assumes key is 'arr_0')
        self.data_binary = dataset["arr_0"]

    # Return the total number of samples in the dataset
    def __len__(self):
        return len(self.data_binary)

    # Retrieve a single sample by index
    # Parameters:
    #   index (int): Index of the sample to retrieve
    # Returns:
    #   Tensor: A float32 PyTorch tensor converted from the NumPy array
    def __getitem__(self, index):
        return torch.from_numpy(self.data_binary[index]).float()

# Define a custom PyTorch Dataset for loading and preprocessing MIDI data
class MidiDataset(Dataset):

    # Constructor to initialize the dataset
    # Parameters:
    #   path (str): Path to the .npz file containing MIDI data
    #   split (str): Dataset split to load ('train', 'test', etc.)
    #   n_bars (int): Number of bars to extract per sample
    #   n_steps_per_bar (int): Number of time steps per bar
    def __init__(self, path, split="train", n_bars=2, n_steps_per_bar=16):
        # Store number of bars and steps per bar
        self.n_bars = n_bars
        self.n_steps_per_bar = n_steps_per_bar

        # Load the specified split from the .npz file
        dataset = np.load(path, allow_pickle=True, encoding="bytes")[split]

        # Preprocess the raw data into binary and integer formats
        self.data_binary, self.data_ints, self.data = self.__preprocess__(dataset)

    # Return the number of samples in the dataset
    def __len__(self):
        return len(self.data_binary)

    # Retrieve a single sample as a float32 tensor
    def __getitem__(self, index):
        return torch.from_numpy(self.data_binary[index]).float()

    # Internal method to preprocess the raw MIDI data
    # Parameters:
    #   data (np.ndarray): Raw array of MIDI piano rolls
    # Returns:
    #   data_binary (np.ndarray): One-hot encoded binary representation
    #   data_ints (np.ndarray): Integer-encoded pitch values
    #   data (np.ndarray): Original raw data
    def __preprocess__(self, data):
        # List to store cleaned integer-encoded sequences
        data_ints = []

        # Iterate over each song in the dataset
        for x in data:
            skip = True           # Flag to skip NaN rows
            skip_rows = 0         # Counter for rows to skip

            # Skip initial rows with NaN values
            while skip:
                if not np.any(np.isnan(x[skip_rows: skip_rows + 4])):
                    skip = False
                else:
                    skip_rows += 4

            # Only include samples with enough time steps
            if self.n_bars * self.n_steps_per_bar < x.shape[0]:
                # Extract a fixed-length segment of shape (n_bars * n_steps_per_bar, n_tracks)
                data_ints.append(x[skip_rows: self.n_bars * self.n_steps_per_bar + skip_rows, :])

        # Convert list to NumPy array
        data_ints = np.array(data_ints)

        # Store number of songs and tracks
        self.n_songs = data_ints.shape[0]
        self.n_tracks = data_ints.shape[2]

        # Reshape to (n_songs, n_bars, n_steps_per_bar, n_tracks)
        data_ints = data_ints.reshape([self.n_songs, self.n_bars, self.n_steps_per_bar, self.n_tracks])

        # Define maximum MIDI note value (0–83 used, 84 as placeholder for NaNs)
        max_note = 83

        # Create a mask for NaN values
        mask = np.isnan(data_ints)

        # Replace NaNs with placeholder value (max_note + 1)
        data_ints[mask] = max_note + 1
        max_note = max_note + 1

        # Convert to integer type
        data_ints = data_ints.astype(int)

        # Define number of one-hot classes (including placeholder)
        num_classes = max_note + 1

        # One-hot encode the integer data → shape: (n_songs, n_bars, n_steps, n_tracks, num_classes)
        data_binary = np.eye(num_classes)[data_ints]

        # Replace 0s with -1 to match GAN input expectations
        data_binary[data_binary == 0] = -1

        # Remove the placeholder class (last index) from one-hot encoding
        data_binary = np.delete(data_binary, max_note, -1)

        # Rearrange axes to (n_songs, n_tracks, n_bars, n_steps, n_pitches)
        data_binary = data_binary.transpose([0, 3, 1, 2, 4])

        # Return binary data, integer data, and original raw data
        return data_binary, data_ints, data