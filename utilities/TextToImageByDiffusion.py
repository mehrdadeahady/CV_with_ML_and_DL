import io
from io import BytesIO
import requests
import sys
import contextlib
import os
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
class TextToImageByDiffusion(QObject):

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

        # Set the default batch size for training or inference
        self.batch_size = 2

        # Initialize dataset reference (to be assigned later)
        self.dataset = None

        # (Redundant) Re-initialization of dataset — can be removed
        self.dataset = None

        # Initialize the training data loader (to be assigned later)
        self.train_dataloader = None

        # Placeholder for the diffusion model (to be created or loaded later)
        self.model = None

        # Placeholder for the noise scheduler used in the diffusion process
        self.noise_scheduler = None

        # Placeholder for storing generated or intermediate images
        self.imgs = None

    # Method to download and visualize a sample of the training dataset
    def DownloadDataset(self):
        # Show the log popup window to inform the user that the download has started
        self.DownloadLogPopup.show()

        # Append a message to the log indicating the dataset download is in progress
        self.DownloadLogPopup.Append_Log("Downloading dataset started.\nIt takes minutes.\nPlease wait...")

        # Load the 'flowers-102-categories' dataset from the Hugging Face hub, using the training split
        self.dataset = load_dataset("huggan/flowers-102-categories", split="train")

        # Apply a predefined transformation pipeline to the dataset (e.g., resizing, normalization)
        self.dataset.set_transform(transforms)

        # Close the log popup after the dataset has been successfully downloaded and transformed
        self.DownloadLogPopup.close()

        # Create a grid of the first 16 images from the dataset for visualization
        # The grid will have 8 images per row and padding of 2 pixels between them
        grid = make_grid(self.dataset[:16]["input"], 8, 2)

        # Create a matplotlib figure to display the image grid
        plt.figure(figsize=(8, 2), dpi=150)

        # Display the image grid with channels rearranged for correct RGB visualization
        plt.imshow(grid.numpy().transpose((1, 2, 0)))

        # Hide axis ticks and labels for a cleaner display
        plt.axis("off")

        # Show the image grid in a pop-up window
        plt.show()

    # Method to load the downloaded dataset into a PyTorch DataLoader for training
    def LoadDataset(self):
        # Check if the dataset has been downloaded; if not, show a warning and exit early
        if self.dataset is None:
            QMessageBox.warning(
                None,                      # No parent widget
                "No Dataset",              # Title of the warning message box
                "First Download the Dataset!"  # Message content
            )
            return  # Exit the method if dataset is not available

        # Create a DataLoader to iterate over the dataset in batches during training
        # Parameters:
        #   self.dataset - the dataset to load
        #   batch_size - number of samples per batch
        #   shuffle=True - randomize the order of samples each epoch
        #   num_workers=0 - use the main thread for data loading (safe for PyQt apps)
        self.train_dataloader = torch.utils.data.DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=0
        )

        # Show a confirmation message that the dataset has been successfully loaded
        QMessageBox.information(
            None,                      # No parent widget
            "Dataset Loaded",          # Title of the message box
            "Dataset Loaded successfully."  # Message content
        )

    # Method to visualize the forward diffusion process by adding noise to clean images over time
    def VisualizeForwardDiffusionProcess(self):
        # Check if the training DataLoader is initialized; if not, show a warning and exit
        if self.train_dataloader is None:
            QMessageBox.warning(
                None,                # No parent widget
                "No Data",           # Title of the warning message box
                "First Load the Dataset!"  # Message content
            )
            return  # Exit early if dataset is not loaded

        # Retrieve a batch of clean images from the DataLoader and scale them to [-1, 1] range
        clean_images = next(iter(self.train_dataloader))["input"] * 2 - 1

        # Get the number of images in the batch
        nums = clean_images.shape[0]

        # Generate random Gaussian noise with the same shape as the clean images
        noise = torch.randn(clean_images.shape)

        # Initialize the DDIM noise scheduler with 1000 training timesteps
        self.noise_scheduler = DDIMScheduler(num_train_timesteps=1000)

        # Start with the original clean images for visualization
        allimgs = clean_images

        # Apply noise at increasing timesteps to simulate the forward diffusion process
        for step in range(200, 1001, 200):  # Steps: 200, 400, 600, 800, 1000
            # Create a tensor of timesteps for the entire batch (same timestep for all images)
            timesteps = torch.tensor([step - 1] * self.batch_size).long()

            # Add noise to the clean images at the specified timestep
            noisy_images = self.noise_scheduler.add_noise(clean_images, noise, timesteps)

            # Concatenate the noisy images to the visualization batch
            allimgs = torch.cat((allimgs, noisy_images))

        # Create a grid of all images (clean + noisy versions) for visualization
        imgs = make_grid(allimgs, nrow=4, padding=6)

        # Create a matplotlib figure with high resolution
        fig = plt.figure(dpi=150)

        # Normalize image values from [-1, 1] to [0, 1] and rearrange dimensions for display
        img = (imgs.permute(1, 2, 0) + 1) / 2
        img = img.clamp(0, 1)  # Ensure pixel values are within valid range

        # Display the image grid using matplotlib
        plt.imshow(img)
        plt.axis("off")  # Hide axis ticks and labels
        plt.show()       # Render the visualization

    # Method to create and initialize the UNet model for image generation
    def CreateModel(self):
        # Check if the model already exists; if so, notify the user and exit early
        if self.model is not None:
            QMessageBox.information(
                None,                 # No parent widget
                "Model Exist",        # Title of the message box
                "Model already Exist!"  # Message content
            )
            return  # Exit the method to avoid recreating the model

        # Instantiate an Attention module with 128 input channels (for testing or warm-up)
        attn = Attention(128)

        # Create a dummy input tensor with shape (1, 128, 64, 64) to simulate a feature map
        x = torch.rand(1, 128, 64, 64)

        # Pass the dummy input through the attention module (optional warm-up or validation)
        out = attn(x)

        # Define the resolution of the input images
        resolution = 64

        # Create a UNet model with 3 input channels (RGB) and specified hidden dimensions
        # Move the model to the appropriate device (GPU if available, otherwise CPU)
        self.model = UNet(
            in_channels=3,
            hidden_dims=[128, 256, 512, 1024],
            image_size=resolution
        ).to(self.device)

        # Calculate the total number of trainable parameters in the model
        num = sum(p.numel() for p in self.model.parameters())

        # Display the model architecture and parameter count in a scrollable message box
        show_scrollable_message(
            "Number of Parameters: %.2fM" % (num / 1e6),  # Format parameter count in millions
            str(self.model)  # Convert model architecture to string for display
        )

    # Method to initiate training of the diffusion model using a separate thread
    def TrainModel(self):
        # Check if the training DataLoader has been initialized
        if self.train_dataloader is None:
            # Show a warning if the dataset hasn't been loaded yet
            QMessageBox.warning(
                None,                    # No parent widget
                "Data Not Ready",        # Title of the warning message box
                "First Load the Data."   # Message content
            )

        # Check if the model has been created
        elif self.model is None:
            # Show a warning if the model is missing
            QMessageBox.warning(
                None,
                "Model Not Found",
                "Please create the model first."
            )

        # Check if the noise scheduler has been initialized
        elif self.noise_scheduler is None:
            # Show a warning if the noise scheduler is missing
            QMessageBox.warning(
                None,
                "noise_scheduler Not Found",
                "Visualize Forward Diffusion Process first."
            )

        else:
            # Enable the cancel button in the log popup to allow user to stop training
            self.DownloadLogPopup.cancel_button.setEnabled(True)

            # Show the log popup window to display training progress
            self.DownloadLogPopup.show()

            # Append an initial log message indicating that training has started
            self.DownloadLogPopup.Append_Log("Training model...\nPlease wait.")

            # Create a new thread to run the training process asynchronously
            self.training_thread = TrainingDiffusionUNetformerThread(
                self.DownloadLogPopup,     # Log popup for displaying training logs
                self.train_dataloader,     # DataLoader for training data
                self.model,                # The UNet model to be trained
                self.device,               # Device to run training on (CPU or GPU)
                self.noise_scheduler       # Scheduler for managing noise during training
            )

            # Connect the training thread's log signal to the log popup's append method
            self.training_thread.log_signal.connect(self.DownloadLogPopup.Append_Log)

            # Connect the cancel button to the training thread's stop method for user interruption
            self.DownloadLogPopup.cancel_button.clicked.connect(self.training_thread.stop)

            # Start the training thread to begin the model training process
            self.training_thread.start()

    # Method to generate images using a trained diffusion model and visualize the results
    def GenerateImage(self):
        # Check if the noise scheduler has been initialized
        if self.noise_scheduler is None:
            QMessageBox.warning(
                None,  # No parent widget
                "noise_scheduler Not Found",  # Title of the warning
                "Visualize Forward Diffusion Process first."  # Message content
            )
            return  # Exit early if noise scheduler is missing

        # Check if the model has been created
        if self.model is None:
            QMessageBox.warning(
                None,
                "Model Not Found",
                "Please create the model first."
            )
            return  # Exit early if model is missing

        # Check if the trained model file exists
        if not os.path.exists("resources/models/diffusion.pth"):
            QMessageBox.warning(
                None,
                "No trained model",
                "Please create, train and save the model first."
            )
            return  # Exit early if model weights are not found

        # Load the trained model weights into the model
        self.model.load_state_dict(torch.load("resources/models/diffusion.pth", map_location=self.device))

        # Show the log popup to inform the user that generation has started
        self.DownloadLogPopup.show()
        self.DownloadLogPopup.Append_Log("Generating Images Started\nIt takes minutes.\nPlease wait...")

        # Determine which button triggered the image generation and set the random seed accordingly
        sender = self.sender().objectName()
        match(sender):
            case "pushButton_GenerateImageCase1_TextToImageByDiffusion":
                generator = torch.manual_seed(1)  # Seed for reproducibility (case 1)
            case "pushButton_GenerateImageCase2_TextToImageByDiffusion":
                generator = torch.manual_seed(2)  # Seed for reproducibility (case 2)

        # Initialize lists to store final samples and intermediate diffusion steps
        all_samples = []
        all_imgs = []

        # Generate 5 batches of 2 images each (total 10 images)
        for i in range(1, 6):
            with torch.no_grad():  # Disable gradient computation for inference
                # Generate images using the diffusion scheduler
                generated_images, imgs = self.noise_scheduler.generate(
                    self.model,                  # Trained model
                    self.device,                 # Device to run on
                    num_inference_steps=50,      # Number of diffusion steps
                    generator=generator,         # Random seed generator
                    eta=1.0,                     # Noise scale
                    use_clipped_model_output=True,  # Clip output to valid range
                    batch_size=2                 # Number of images per batch
                )

                # Extract the final generated samples
                samples = generated_images["sample"]

                # Convert numpy arrays to tensors if necessary
                if isinstance(samples, np.ndarray):
                    samples = torch.from_numpy(samples)

                # Append the generated samples and intermediate steps to their respective lists
                all_samples.append(samples)
                all_imgs.append(imgs)

            # Log progress after each batch
            self.DownloadLogPopup.Append_Log(
                f"Step: {i} finished.\nGenerating next 2 images started...\nPlease wait..."
            )

        # Concatenate all generated samples into a single tensor
        imgnp = torch.cat(all_samples, dim=0)

        # Determine the number of generated images
        num_images = imgnp.shape[0] or len(imgnp)

        # Convert all intermediate diffusion steps to tensors if they are numpy arrays
        for i in range(len(all_imgs)):
            for j in range(len(all_imgs[i])):
                if isinstance(all_imgs[i][j], np.ndarray):
                    all_imgs[i][j] = torch.from_numpy(all_imgs[i][j])

        # Zip and concatenate the diffusion steps across batches for visualization
        self.imgs = [torch.cat(t, dim=0) for t in zip(*all_imgs)]

        # Create a matplotlib figure to display the generated images
        plt.figure(figsize=(10, 4), dpi=150)
        for i in range(min(num_images, 10)):  # Display up to 10 images
            ax = plt.subplot(2, 5, i + 1)  # Arrange in a 2x5 grid
            plt.imshow(imgnp[i])          # Show the image
            plt.xticks([])                # Hide x-axis ticks
            plt.yticks([])                # Hide y-axis ticks
            plt.tight_layout()            # Adjust layout to avoid overlap

        # Show the final image grid
        plt.show()

    # Method to visualize the reverse diffusion process by showing denoising steps for selected images
    def VisualizeReverseDiffusionProcess(self):
        # Check if the diffusion steps (self.imgs) are available; if not, show a warning and exit
        if self.imgs is None:
            QMessageBox.warning(
                None,                   # No parent widget
                "Images Not Found",     # Title of the warning message box
                "Generate Images first."  # Message content
            )
            return  # Exit early if no images are available

        # Select the final 5 timesteps: 800, 600, 400, 200, and 0 (reverse order of generation)
        steps = self.imgs[9::10]  # Every 10th step starting from index 9 (i.e., last step of each batch)

        # Get the batch size from the first diffusion step tensor
        batch_size = self.imgs[0].shape[0]

        # Select 4 specific image indices (e.g., flower samples) to visualize across timesteps
        imgs20 = []
        for j in [1, 3, 6, 9]:  # Indices of selected images
            for i in range(5):  # For each of the 5 timesteps
                imgs20.append(steps[i][j])  # Append the image at timestep i for sample j

        # Create a matplotlib figure to display the 20 selected images
        plt.figure(figsize=(10, 8), dpi=100)

        # Plot the 20 images in a 4x5 grid (4 samples × 5 timesteps)
        for i in range(20):
            k = i % 5  # Determine the timestep index for labeling
            ax = plt.subplot(4, 5, i + 1)  # Create a subplot in the grid
            plt.imshow(imgs20[i])         # Display the image
            plt.xticks([])                # Hide x-axis ticks
            plt.yticks([])                # Hide y-axis ticks
            plt.tight_layout()            # Adjust layout to avoid overlap
            plt.title(f't={800 - 200 * k}', fontsize=8, c="r", pad=2)  # Add timestep label

        # Show the final visualization
        plt.show()

    # Method to generate an image from a text prompt using OpenAI's image generation API
    # Parameters:
    #   self - reference to the class instance
    #   text - the text prompt describing the desired image
    #   openai_api_key - the API key used to authenticate with OpenAI
    def ConvertTextToImage(self, text, openai_api_key):
        try:
            # Initialize the OpenAI client with the provided API key
            client = OpenAI(api_key=openai_api_key)

            # (Optional) Retrieve the list of available models from OpenAI
            modelList = response = client.models.list()

            # Send a request to generate an image using the specified model and prompt
            response = client.images.generate(
                # Use the latest available image model (e.g., "gpt-image-1.5", "dall-e-3", "dall-e-2", "gpt-image-1-mini", or legacy "GPT Image 1").
                model="gpt-image-1.5",  # Use the latest available image model (e.g., "gpt-image-1.5")
                prompt=text,            # The text prompt to generate the image from
                size="auto",            # Let the API choose the optimal image size
                n=1                     # Number of images to generate
            )

            # Extract the URL of the generated image from the response
            image_url = response.data[0].url

            # Send an HTTP GET request to download the image from the URL
            img_response = requests.get(image_url)

            # Raise an exception if the HTTP request failed (e.g., 404 or 500 error)
            img_response.raise_for_status()

            # Open the image using PIL from the downloaded byte stream
            img = Image.open(BytesIO(img_response.content))

            # Create a matplotlib figure to display the image
            plt.figure(figsize=(6, 6))  # Set figure size
            plt.imshow(img)            # Display the image
            plt.axis('off')            # Hide axis ticks and labels
            plt.title("Generated Image")  # Set a title for the image
            plt.tight_layout()         # Adjust layout to fit the figure nicely
            plt.show()                 # Render the image in a pop-up window

            # Show a message box with the image URL for user reference
            QMessageBox.information(
                None,                # No parent widget
                "Image URL",         # Title of the message box
                str(image_url)       # Message content: the image URL
            )

        except Exception as e:
            # If any error occurs during the process, show an error message box
            QMessageBox.critical(
                None,                      # No parent widget
                "Image Generation Failed", # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

# Define a QThread subclass to handle training of the diffusion model in a separate thread
class TrainingDiffusionUNetformerThread(QThread):

    # Signal to emit log messages to the UI (e.g., training progress updates)
    log_signal = pyqtSignal(str)

    # Signal to trigger visualization updates (e.g., after each epoch)
    display_signal = pyqtSignal(int)

    # Constructor to initialize the training thread with required components
    def __init__(self, DownloadLogPopup, train_dataloader, model, device, noise_scheduler):
        # Call the base class constructor
        super().__init__()

        # Reference to the popup window used for displaying logs
        self.DownloadLogPopup = DownloadLogPopup

        # DataLoader for training data
        self.train_dataloader = train_dataloader

        # The diffusion model to be trained
        self.model = model

        # Scheduler for adding noise during training
        self.noise_scheduler = noise_scheduler

        # Device to run training on (CPU or GPU)
        self.device = device

        # Number of training epochs
        self.num_epochs = 100

        # Optimizer for training the model using AdamW
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=0.0001,
            betas=(0.95, 0.999),
            weight_decay=0.00001,
            eps=1e-8
        )

        # Learning rate scheduler with cosine decay and warmup
        self.lr_scheduler = get_scheduler(
            "cosine",
            optimizer=self.optimizer,
            num_warmup_steps=300,
            num_training_steps=(len(train_dataloader) * self.num_epochs)
        )

        # Flag to allow user to interrupt training manually
        self._stop_requested = False

    # Method to request stopping the training loop
    def stop(self):
        # Set the stop flag to True
        self._stop_requested = True

        # Disable the cancel button in the UI to prevent further interaction
        self.DownloadLogPopup.cancel_button.setEnabled(False)

    # Main training loop executed in the background thread
    def run(self):
        try:
            # Emit initial log messages
            self.log_signal.emit("Training thread started.")
            self.log_signal.emit(f"Train loader has {len(self.train_dataloader)} batches.")

            # Set gradient accumulation steps
            accum_steps = 2

            # Loop over epochs
            for epoch in range(self.num_epochs):
                if self._stop_requested:
                    break  # Exit if user requested stop

                self.model.train()  # Set model to training mode
                tloss = 0  # Track total loss for the epoch
                self.log_signal.emit(f"start epoch {epoch}")

                # Loop over training batches
                for step, batch in enumerate(self.train_dataloader):
                    if self._stop_requested:
                        self.log_signal.emit("Training stopped by user.")
                        break  # Exit inner loop if stop requested

                    # Prepare clean images and scale to [-1, 1]
                    clean_images = batch["input"].to(self.device) * 2 - 1
                    nums = clean_images.shape[0]

                    # Generate random noise and timesteps
                    noise = torch.randn_like(clean_images, device=self.device)
                    timesteps = torch.randint(
                        0,
                        self.noise_scheduler.num_train_timesteps,
                        (nums,),
                        device=self.device
                    ).long()

                    # Add noise to clean images using the scheduler
                    noisy_images = self.noise_scheduler.add_noise(clean_images, noise, timesteps)

                    # Forward pass through the model to predict noise
                    noise_pred = self.model(noisy_images, timesteps)["sample"]

                    # Compute L1 loss between predicted and actual noise
                    loss = torch.nn.functional.l1_loss(noise_pred, noise)
                    loss = loss / accum_steps  # Normalize for accumulation
                    loss.backward()  # Backpropagate

                    # Perform optimizer step after accumulating gradients
                    if (step + 1) % accum_steps == 0:
                        self.optimizer.step()
                        self.lr_scheduler.step()
                        self.optimizer.zero_grad()

                        # Clear unused GPU memory
                        if torch.cuda.is_available():
                            torch.cuda.empty_cache()

                    # Accumulate total loss for logging
                    tloss += loss.detach().item() * accum_steps

                    # Emit log every 10 steps
                    if step % 10 == 0:
                        self.log_signal.emit(f"step {step}, average loss {tloss / (step + 1)}")

            # Save the trained model to disk
            torch.save(self.model.state_dict(), 'resources/models/diffusion_.pth')
            self.log_signal.emit("Training Finished.\nModel Saved.")

            # Scroll the log output to the bottom
            self.DownloadLogPopup.log_output.moveCursor(QTextCursor.MoveOperation.End)
            self.DownloadLogPopup.log_output.ensureCursorVisible()
            QApplication.processEvents()

        except Exception as e:
            # Emit error message if training fails
            self.log_signal.emit(f"Error during training: {str(e)}")