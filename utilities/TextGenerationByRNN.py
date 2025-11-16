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
from collections import Counter
from utilities.DeepLearningFoundationOperations import DownloadLogPopup, LogEmitter
from utilities.DLbyPyTorch import EarlyStop, DLbyPyTorch, PopupStream
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
    from PyQt6.QtGui import  QTextCursor   
    from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt
    from PyQt6.QtWidgets import QMessageBox,QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QTextEdit,QScrollArea,QMainWindow,QApplication
except:
    print("You Should Install PyQt6 Library!")

# Define a class for text generation using a Recurrent Neural Network (RNN)
class TextGenerationByRNN(QObject):

    # Constructor method to initialize the class instance
    def __init__(self, parent=None):
        # Call the constructor of the parent QObject class
        super().__init__()

        # Set a fixed seed for PyTorch to ensure reproducibility of results
        torch.manual_seed(0)

        # Set a fixed seed for NumPy to ensure reproducibility of results
        np.random.seed(0)

        # Define the batch size for training or inference
        self.batch_size = 32

        # Original input text to be used for tokenization and model training
        self.text = "Tis is a sample text for tokenization!"

        # Placeholder for storing a sample of processed/generated text
        self.sample_text = ""

        # Placeholder for storing cleaned version of the input text
        self.clean_text = ""

        # Placeholder for storing word indices after tokenization
        self.wordidx = None

        # Dictionary mapping words to their corresponding integer indices
        self.word_to_int = None

        # Dictionary mapping integer indices back to their corresponding words
        self.int_to_word = None

        # Define the length of input sequences for training the RNN
        self.seq_len = 100

        # Placeholder for the data loader that will feed data into the model
        self.loader = None

        # Select the computation device: use GPU if available, otherwise fallback to CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Initialize a custom log emitter for sending messages or updates (likely via Qt signals)
        self.log_emitter = LogEmitter()

        # Placeholder for the RNN model instance
        self.model = None

    # Define a method to perform character-level tokenization on the input text
    def CharacterTokenization(self):
        # Retrieve the original text stored in the class attribute
        text = self.text

        # Convert the text into a list of individual characters (character-level tokenization)
        tokenizedText = list(text)

        # Display a message box showing the original sample text and its character-tokenized version
        QMessageBox.information(
            None,
            "Compare:",
            "Raw Text:\n" + self.sample_text + "\nCharacter Tokenized:\n" + str(tokenizedText)
        )

    # Define a method to perform word-level tokenization on the input text
    def WordTokenization(self):
        # Retrieve the original text stored in the class attribute
        text = self.text

        # (Optional) Example of manually spacing punctuation for tokenization — currently commented out
        # text = text.replace("!", " !")

        # Iterate over a list of punctuation marks to ensure they are spaced for proper token separation
        for x in list(",!"):
            # Replace each punctuation mark with a space followed by the mark to isolate it as a token
            text = text.replace(f"{x}", f" {x}")

        # Split the modified text into tokens based on spaces (word-level tokenization)
        tokenizedText = text.split(" ")

        # Display a message box showing the original sample text and its word-tokenized version
        QMessageBox.information(
            None,
            "Compare:",
            "Raw Text:\n" + self.sample_text + "\nWord Tokenized:\n" + str(tokenizedText)
        )

    # Define a method to perform subword-level tokenization on the input text
    def SubWordTokenization(self):
        # Retrieve the original text stored in the class attribute
        text = self.text

        # Iterate over punctuation marks to ensure they are spaced for proper token separation
        for x in list(",!"):
            # Replace each punctuation mark with a space followed by the mark
            text = text.replace(f"{x}", f" {x}")

        # Split the modified text into individual words for subword analysis
        detectDrivedWords = text.split(" ")

        # Iterate over each word to detect and split suffixes like "ization"
        for x in detectDrivedWords:
            # Check if the word contains the suffix "ization"
            if x.__contains__("ization"):
                # Define the suffix to be extracted
                suffix = "ization"

                # Extract the base word by removing the suffix
                baseWord = x[0:len(x) - len(suffix)]

                # Replace the original word with its base and suffix as separate tokens
                text = text.replace(f"{x}", f" {baseWord}" + f" {suffix}")

        # Split the updated text into tokens based on spaces
        tokenizedText = text.split(" ")

        # Display a message box showing the original sample text and its subword-tokenized version
        QMessageBox.information(
            None,
            "Compare:",
            "Raw Text:\n" + self.sample_text + "\nSubWord Tokenized:\n" + str(tokenizedText)
        )

    # Define a method to load sample text from a file
    def LoadSampleText(self):
        # Check if the sample text file exists at the specified path
        if os.path.exists("resources/anna.txt"):
            # Open the file in read mode and assign its contents to a variable
            with open("resources/anna.txt", "r") as f:
                text = f.read()

            # Store the loaded text in the class attribute for later use
            self.sample_text = text

            # Display the first 100 characters of the sample text in a scrollable message box
            show_scrollable_message("First 100 Characters in Sample Text:", text[:100])
        else:
            # Show a warning message box if the sample text file is not found
            QMessageBox.warning(None, "No Text File", "Sample Text not Found!")

    # Define a method to clean the loaded sample text for further processing
    def CleanSampleText(self):
        # Check if the sample text has been loaded and is not empty
        if len(self.sample_text) > 0:
            # Convert all characters in the sample text to lowercase and replace newline characters with spaces
            clean_text = self.sample_text.lower().replace("\n", " ")

            # Replace hyphens with spaces to separate hyphenated words
            clean_text = clean_text.replace("-", " ")

            # Iterate over a set of punctuation characters to isolate them with spaces
            for x in ",.:;?!$()/_&%*@'`":
                # Surround each punctuation mark with spaces to treat them as separate tokens
                clean_text = clean_text.replace(f"{x}", f" {x} ")

            # Handle double quotes separately by surrounding them with spaces
            clean_text = clean_text.replace('"', ' " ')

            # Split the cleaned text into a list of tokens and store it in the class attribute
            self.clean_text = clean_text.split()

            # Call a method to compute and display statistics about the cleaned sample text
            self.SampleTextStatistics()
        else:
            # Show a warning message if no sample text has been loaded yet
            QMessageBox.warning(None, "No Text Found", "First Load the Sample Text!")

    # Define a method to compute and display statistics about the cleaned sample text
    def SampleTextStatistics(self):
        # Count the frequency of each word in the cleaned text using a Counter
        word_counts = Counter(self.clean_text)

        # Sort the words by frequency in descending order to prioritize common tokens
        words = sorted(word_counts, key=word_counts.get, reverse=True)

        # Calculate the total number of words in the cleaned text
        text_length = len(self.clean_text)

        # Calculate the number of unique tokens in the cleaned text
        num_unique_words = len(words)

        # Initialize a statistics string with total word count
        statistics = f"the text contains {text_length} words\n"

        # Append the number of unique tokens to the statistics string
        statistics += f"there are {num_unique_words} unique tokens\n"

        # Create a dictionary mapping each word to a unique integer index
        self.word_to_int = {v: k for k, v in enumerate(words)}

        # Create a reverse dictionary mapping each index back to its corresponding word
        self.int_to_word = {k: v for k, v in enumerate(words)}

        # Append the first 10 word-to-index mappings to the statistics string
        statistics += "First 10 tokens(value,key): " + str({k: v for k, v in self.word_to_int.items() if k in words[:10]}) + "\n"

        # Append the first 10 index-to-word mappings to the statistics string
        statistics += "First 10 tokens(key,value): " + str({k: v for k, v in self.int_to_word.items() if v in words[:10]}) + "\n"

        # Convert the cleaned text into a list of corresponding word indices
        self.wordidx = [self.word_to_int[w] for w in self.clean_text]

        # Append the indices of the first 10 tokens to the statistics string
        statistics += "First 10 index of tokens: " + str([self.word_to_int[w] for w in self.clean_text[:10]]) + "\n"

        # Display the compiled statistics in a scrollable message box
        show_scrollable_message("Cleaned Text Statistics:", statistics)

    # Define a method to prepare the sample text for training by creating input-output sequences
    def PrepareSampleText(self):
        # Check if word indices have been generated from the cleaned text
        if self.wordidx is None:
            # Show a warning if the sample text hasn't been cleaned yet
            QMessageBox.warning(None, "Text not Ready", "First, Clean the Sample Text.")
        else:
            # Proceed only if the data loader hasn't already been created
            if self.loader is None:
                # Create a popup window to display training logs and progress
                self.DownloadLogPopup = DownloadLogPopup(
                    # Pass the log emitter to stream messages to the popup
                    self.log_emitter
                )

                # Show the popup window to the user
                self.DownloadLogPopup.show()

                # Log the start of the sample text preparation process
                self.DownloadLogPopup.Append_Log("Preparing Sample Text...\nPlease wait.")

                # Initialize a list to store input-output sequence pairs
                xys = []

                # Loop through the word indices to generate sequences of length `seq_len`
                for n in range(0, len(self.wordidx) - self.seq_len - 1):
                    # Extract a sequence of input tokens
                    x = self.wordidx[n : n + self.seq_len]

                    # Extract the corresponding output sequence (shifted by one position)
                    y = self.wordidx[n + 1 : n + self.seq_len + 1]

                    # Append the input-output pair as tensors to the list
                    xys.append((torch.tensor(x), torch.tensor(y)))

                    # Log progress every 1000 sequences
                    if n % 1000 == 0:
                        self.DownloadLogPopup.Append_Log(f"Index {n} prepared")

                # Set a manual seed for reproducibility in data loading
                torch.manual_seed(42)

                # Create a PyTorch DataLoader to batch and shuffle the training data
                self.loader = DataLoader(
                    xys,
                    batch_size=self.batch_size,
                    shuffle=True
                )

                # Retrieve the first batch of input-output pairs from the loader
                x, y = next(iter(self.loader))

                # Log the prepared data and its shape for verification
                self.DownloadLogPopup.Append_Log(
                    f"Text prepared:\nx=\n" + str(x) +
                    "\ny=\n" + str(y) +
                    "\nx shape=\n" + str(x.shape) +
                    "\ny shape=\n" + str(y.shape)
                )
            else:
                # Show a warning if the sample text has already been prepared
                QMessageBox.warning(None, "Text Prepared", "Text already prepared.")

    # Define a method to create the RNN model for text generation
    def CreateModel(self):
        # Check if the word-to-index dictionary has been initialized
        if self.word_to_int is None:
            # Show a warning if the sample text hasn't been cleaned and processed yet
            QMessageBox.warning(None, "Text not Ready", "First, Clean the Sample Text.")
        else:
            # Proceed only if the model hasn't already been created
            if self.model is None:
                # Instantiate the WordLSTM model using the word-to-index mapping
                self.model = WordLSTM(word_to_int=self.word_to_int).to(self.device)

                # Show a message confirming that the model has been successfully created
                QMessageBox.warning(None, "Model Created", str(self.model))
            else:
                # Show a message indicating that the model already exists
                QMessageBox.warning(None, "Model Created", "Model Already Created.")

    # Define a method to initiate training of the model
    def TrainModel(self):
        # Check if the dataset has been prepared and loaded
        if self.loader is None:
            # Warn the user to prepare the dataset before training
            QMessageBox.warning(None, "Dataset Not Ready", "Please prepare the text first.")

        # Check if the model has been created
        elif self.model is None:
            # Warn the user to create the model before starting training
            QMessageBox.warning(None, "Model Not Found", "Please create the model first.")

        # Proceed with training only if both dataset and model are ready
        else:
            # Create a popup window to display real-time training logs
            self.DownloadLogPopup = DownloadLogPopup(
                # Pass the log emitter to stream messages to the popup
                self.log_emitter
            )

            # Enable the cancel button to allow user interruption during training
            self.DownloadLogPopup.cancel_button.setEnabled(True)

            # Show the log popup window to the user
            self.DownloadLogPopup.show()

            # Log the start of the training process
            self.DownloadLogPopup.Append_Log("Training model...\nPlease wait.")

            # Create a separate thread to run the training process asynchronously
            self.training_thread = TrainingLSTMThread(
                # Reference to the log popup for status updates
                self.DownloadLogPopup,

                # Data loader containing input-output sequences
                self.loader,

                # RNN model to be trained
                self.model,

                # Device (CPU or GPU) to run the training on
                self.device,

                # Batch size for training
                self.batch_size
            )

            # Connect the thread's log signal to the popup's log appending method
            self.training_thread.log_signal.connect(self.DownloadLogPopup.Append_Log)

            # Connect the cancel button to the thread's stop method to allow user to halt training
            self.DownloadLogPopup.cancel_button.clicked.connect(self.training_thread.stop)

            # Start the training thread to begin model training
            self.training_thread.start()

    # Define a method to load a previously trained WordLSTM model from disk
    def LoadTrainedModel(self):

        # Check if the model has been instantiated
        if self.model is None:
            # Show a warning message prompting the user to create the model first
            QMessageBox.warning(
                None,                          # No parent widget
                "Model Does Not Exist",        # Title of the warning dialog
                "Please create the model first."  # Message body with refined grammar
            )
            # Return False to indicate that model loading failed
            return False

        else:
            # Check if the saved model file exists at the specified path
            if os.path.exists("resources/models/wordLSTM.pth"):

                # Load the model weights from the file and map them to the appropriate device
                self.model.load_state_dict(
                    torch.load(
                        "resources/models/wordLSTM.pth",  # Path to the saved model file
                        map_location=self.device          # Load weights onto the correct device (CPU/GPU)
                    )
                )

                # Set the model to evaluation mode to disable dropout and batch norm layers
                self.model.eval()

                # Return True to indicate successful model loading
                return True

            else:
                # Show a warning message if the model file is not found
                QMessageBox.warning(
                    None,                          # No parent widget
                    "Model Not Saved",             # Title of the warning dialog
                    "Please train and save the model first."  # Message body with refined grammar
                )
                # Return False to indicate that model loading failed
                return False

    # Define a method to generate text using the trained model and a given prompt
    def sample(self, model, prompt, length=200):
        # Set the model to evaluation mode to disable dropout and other training-time behaviors
        model.eval()

        # Convert the prompt to lowercase and split it into a list of words
        text = prompt.lower().split(' ')

        # Initialize the hidden and cell states for the model with batch size 1
        hc = model.init_hidden(1)

        # Adjust the number of tokens to generate by subtracting the prompt length
        length = length - len(text)

        # Generate tokens one by one until the desired length is reached
        for i in range(0, length):
            # If the current text is shorter than or equal to the sequence length, use the full text
            if len(text) <= self.seq_len:
                x = torch.tensor([[self.word_to_int[w] for w in text]])
            # Otherwise, use only the last `seq_len` tokens as input
            else:
                x = torch.tensor([[self.word_to_int[w] for w in text[-self.seq_len:]]])

            # Move the input tensor to the appropriate device (CPU or GPU)
            inputs = x.to(self.device)

            # Perform a forward pass through the model to get output and updated hidden state
            output, hc = model(inputs, hc)

            # Extract the logits (raw scores) for the last predicted token
            logits = output[0][-1]

            # Apply softmax to convert logits into a probability distribution
            p = nn.functional.softmax(logits, dim=0).detach().cpu().numpy()

            # Sample a token index from the probability distribution
            idx = np.random.choice(len(logits), p=p)

            # Append the predicted word to the generated text
            text.append(self.int_to_word[idx])

        # Join the list of words into a single string
        text = " ".join(text)

        # Post-process punctuation spacing to improve formatting
        for m in ",.:;?!$()/_&%*@'`":
            text = text.replace(f" {m}", f"{m} ")

        # Clean up spacing around quotation marks and apostrophes
        text = text.replace('"  ', '"')
        text = text.replace("'  ", "'")
        text = text.replace('" ', '"')
        text = text.replace("' ", "'")

        # Return the final generated text
        return text

    # Define a method to test the trained model by generating text from a prompt
    def TestModel(self):
        # Attempt to load the trained model from disk
        if not self.LoadTrainedModel():
            # Exit early if model loading failed
            return

        # Check if the word-to-index and index-to-word mappings are available
        if self.word_to_int is None or self.int_to_word is None:
            # Show a warning if the sample text hasn't been processed yet
            QMessageBox.warning(None, "No Text Found", "First Load the Sample Text, Clean and Prepare it!")
        else:
            # Create a popup window to display logs and generated text
            self.DownloadLogPopup = DownloadLogPopup(
                # Pass the log emitter to stream messages to the popup
                self.log_emitter
            )

            # Enable the cancel button in case the user wants to interrupt the process
            self.DownloadLogPopup.cancel_button.setEnabled(True)

            # Show the popup window to the user
            self.DownloadLogPopup.show()

            # Log the start of the text generation process
            self.DownloadLogPopup.Append_Log("Generating Text by predicting next Token:\nPlease wait...\n")

            # Generate text using the trained model and a given prompt, then log the result
            self.DownloadLogPopup.Append_Log(
                self.sample(self.model, prompt='Anna and the prince')
            )

    # Define a method to generate text using a trained model with optional top-k sampling and temperature control
    def generate(self, model, prompt, top_k=None, length=200, temperature=1):
        # Set the model to evaluation mode to disable dropout and other training-specific behaviors
        model.eval()

        # Convert the input prompt to lowercase and split it into individual words
        text = prompt.lower().split(' ')

        # Initialize the hidden and cell states for the model with batch size 1
        hc = model.init_hidden(1)

        # Adjust the number of tokens to generate based on the length of the prompt
        length = length - len(text)

        # Generate tokens one at a time until the desired length is reached
        for i in range(0, length):
            # If the current text is shorter than or equal to the sequence length, use the full text
            if len(text) <= self.seq_len:
                x = torch.tensor([[self.word_to_int[w] for w in text]])
            # Otherwise, use only the last `seq_len` tokens as input
            else:
                x = torch.tensor([[self.word_to_int[w] for w in text[-self.seq_len:]]])

            # Move the input tensor to the appropriate device (CPU or GPU)
            inputs = x.to(self.device)

            # Perform a forward pass through the model to get output and updated hidden state
            output, hc = model(inputs, hc)

            # Extract the logits (raw scores) for the last predicted token
            logits = output[0][-1]

            # Apply temperature scaling to control randomness in sampling
            logits = logits / temperature

            # Convert logits to probabilities using softmax and move to CPU
            p = nn.functional.softmax(logits, dim=0).detach().cpu()

            # If top_k is not specified, sample from the full distribution
            if top_k is None:
                idx = np.random.choice(len(logits), p=p.numpy())
            else:
                # Perform top-k sampling: select the top k probabilities
                ps, tops = p.topk(top_k)

                # Normalize the top-k probabilities to form a valid distribution
                ps = ps / ps.sum()

                # Randomly sample from the top-k candidates
                idx = np.random.choice(tops, p=ps.numpy())

            # Append the predicted word to the generated text
            text.append(self.int_to_word[idx])

        # Join the list of words into a single string
        text = " ".join(text)

        # Post-process punctuation to remove extra spaces before punctuation marks
        for m in ",.:;?!$()/_&%*@'`":
            text = text.replace(f" {m}", f"{m} ")

        # Clean up spacing around quotation marks and apostrophes
        text = text.replace('"  ', '"')
        text = text.replace("'  ", "'")
        text = text.replace('" ', '"')
        text = text.replace("' ", "'")

        # Return the final generated text
        return text

    # Define a method to generate multiple samples using default generation settings
    def SampleWithDefaultSetting(self):
        # Attempt to load the trained model from disk
        if not self.LoadTrainedModel():
            # Exit early if model loading failed
            return

        # Check if the word-to-index and index-to-word mappings are available
        if self.word_to_int is None or self.int_to_word is None:
            # Show a warning if the sample text hasn't been processed yet
            QMessageBox.warning(None, "No Text Found", "First Load the Sample Text, Clean and Prepare it!")
        else:
            # Create a popup window to display logs and generated samples
            self.DownloadLogPopup = DownloadLogPopup(
                # Pass the log emitter to stream messages to the popup
                self.log_emitter
            )

            # Enable the cancel button in case the user wants to interrupt the process
            self.DownloadLogPopup.cancel_button.setEnabled(True)

            # Show the popup window to the user
            self.DownloadLogPopup.show()

            # Log the start of the text generation process
            self.DownloadLogPopup.Append_Log("Generating Text by Default Settings:\nPlease wait...\n")

            # Define a fixed prompt for generation
            prompt = "I ' m not going to see"

            # Generate and log 10 samples using default settings (no top-k, temperature=1)
            for _ in range(10):
                generated_text = self.generate(
                    self.model,
                    prompt,
                    top_k=None,
                    length=len(prompt.split(" ")) + 1,
                    temperature=1
                )
                self.DownloadLogPopup.Append_Log(generated_text)

    # Define a method to generate text using various top-k and temperature settings based on the button clicked
    def SampleWithTopKAndTemprature(self):
        # Identify which button triggered this method
        sender = self.sender().objectName()

        # Attempt to load the trained model from disk
        if not self.LoadTrainedModel():
            # Exit early if model loading failed
            return

        # Ensure that the vocabulary mappings are available
        if self.word_to_int is None or self.int_to_word is None:
            QMessageBox.warning(None, "No Text Found", "First Load the Sample Text, Clean and Prepare it!")
        else:
            # Create a popup window to display logs and generated samples
            self.DownloadLogPopup = DownloadLogPopup(
                self.log_emitter  # Pass the log emitter for real-time updates
            )

            # Enable the cancel button in case the user wants to interrupt generation
            self.DownloadLogPopup.cancel_button.setEnabled(True)

            # Clear any previous logs
            self.DownloadLogPopup.cleanup()

            # Show the popup window
            self.DownloadLogPopup.show()

            # Define the prompt to use for generation
            prompt = "I ' m not going to see"

            # Determine which button was clicked and apply the corresponding generation settings
            match sender:
                case "pushButton_SampleWithDefaultSetting_TextGenerationByRNN":
                    self.DownloadLogPopup.Append_Log("Generating Text by Default Settings:\nPlease wait...\n")
                    for _ in range(10):
                        self.DownloadLogPopup.Append_Log(
                            self.generate(self.model, prompt, top_k=None, length=len(prompt.split()) + 1, temperature=1)
                        )

                case "pushButton_SampleWithLowTemperature_TextGenerationByRNN":
                    self.DownloadLogPopup.Append_Log("Generating Text With Low Temperature:\nPlease wait...\n")
                    for _ in range(10):
                        self.DownloadLogPopup.Append_Log(
                            self.generate(self.model, prompt, top_k=None, length=len(prompt.split()) + 1, temperature=0.5)
                        )

                case "pushButton_SampleWithHighTemperature_TextGenerationByRNN":
                    self.DownloadLogPopup.Append_Log("Generating Text With High Temperature:\nPlease wait...\n")
                    for _ in range(10):
                        self.DownloadLogPopup.Append_Log(
                            self.generate(self.model, prompt, top_k=None, length=len(prompt.split()) + 1, temperature=2)
                        )

                case "pushButton_SampleWithLowTopK_TextGenerationByRNN":
                    self.DownloadLogPopup.Append_Log("Generating Text With Low Top K:\nPlease wait...\n")
                    for _ in range(10):
                        self.DownloadLogPopup.Append_Log(
                            self.generate(self.model, prompt, top_k=3, length=len(prompt.split()) + 1, temperature=1)
                        )

                case "pushButton_SampleWithHighTopK_TextGenerationByRNN":
                    self.DownloadLogPopup.Append_Log("Generating Text With High Top K:\nPlease wait...\n")
                    for _ in range(10):
                        self.DownloadLogPopup.Append_Log(
                            self.generate(self.model, prompt, top_k=1000, length=len(prompt.split()) + 1, temperature=1)
                        )

# Define a QThread subclass to handle LSTM model training asynchronously
class TrainingLSTMThread(QThread):

    # Signal to emit log messages to the UI (e.g., training progress updates)
    log_signal = pyqtSignal(str)

    # Signal to trigger visualization updates (e.g., after each epoch)
    display_signal = pyqtSignal(int)

    # Constructor to initialize the training thread with model, data, and UI hooks
    def __init__(self, DownloadLogPopup, loader, model, device, batch_size):
        # Call the parent QThread constructor
        super().__init__()

        # Reference to the popup window used for displaying logs
        self.DownloadLogPopup = DownloadLogPopup

        # The LSTM model to be trained
        self.model = model

        # Learning rate for the optimizer
        self.lr = 0.0001

        # Adam optimizer for updating model parameters
        self.optimizer = torch.optim.Adam(model.parameters(), lr=self.lr)

        # Cross-entropy loss function for sequence prediction
        self.loss_func = nn.CrossEntropyLoss()

        # Batch size used during training
        self.batch_size = batch_size

        # Device on which training will run (e.g., 'cpu' or 'cuda')
        self.device = device

        # DataLoader providing batches of training data
        self.loader = loader

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
            self.log_signal.emit(f"Train loader has {len(self.loader)} batches.")

            # Set the model to training mode
            self.model.train()

            # Loop over a fixed number of epochs
            for epoch in range(50):
                # Exit early if stop was requested
                if self._stop_requested:
                    break

                # Initialize total loss for the epoch
                tloss = 0

                # Initialize hidden and cell states for the LSTM
                sh, sc = self.model.init_hidden(self.batch_size)

                # Loop over batches from the DataLoader
                for i, (x, y) in enumerate(self.loader):
                    # Check again for stop request
                    if self._stop_requested:
                        self.log_signal.emit("Training stopped by user.")
                        break

                    # Only process batches that match the expected batch size
                    if x.shape[0] == self.batch_size:
                        # Move input and target tensors to the correct device
                        inputs, targets = x.to(self.device), y.to(self.device)

                        # Reset gradients before backpropagation
                        self.optimizer.zero_grad()

                        # Forward pass through the model
                        output, (sh, sc) = self.model(inputs, (sh, sc))

                        # Compute loss (transpose output to match target shape)
                        loss = self.loss_func(output.transpose(1, 2), targets)

                        # Detach hidden states to prevent backprop through entire history
                        sh, sc = sh.detach(), sc.detach()

                        # Backpropagate the loss
                        loss.backward()

                        # Clip gradients to prevent exploding gradients
                        nn.utils.clip_grad_norm_(self.model.parameters(), 5)

                        # Update model parameters
                        self.optimizer.step()

                        # Accumulate loss
                        tloss += loss.item()

                    # Log progress every 100 iterations
                    if (i + 1) % 100 == 0:
                        self.log_signal.emit(
                            f"at epoch {epoch + 1} iteration {i + 1} average loss = {tloss / (i + 1)}"
                        )

            # Save the trained model weights to disk
            torch.save(self.model.state_dict(), "resources/models/wordLSTM_.pth")

            # Emit a message indicating training is complete
            self.log_signal.emit("Training Finished.")

            # Scroll the log output to the bottom
            self.DownloadLogPopup.log_output.moveCursor(QTextCursor.MoveOperation.End)
            self.DownloadLogPopup.log_output.ensureCursorVisible()

            # Process any pending UI events to refresh the interface
            QApplication.processEvents()

        except Exception as e:
            # Emit an error message if training fails
            self.log_signal.emit(f"Error during training: {str(e)}")

# Define a PyTorch neural network module for word-level LSTM-based language modeling
class WordLSTM(nn.Module):

    # Constructor to initialize the model architecture
    def __init__(self, input_size=128, n_embed=128, n_layers=3, drop_prob=0.2, word_to_int=None):
        # Call the parent class constructor
        super().__init__()

        # Dimensionality of input features (typically same as embedding size)
        self.input_size = input_size

        # Dropout probability between LSTM layers
        self.drop_prob = drop_prob

        # Number of stacked LSTM layers
        self.n_layers = n_layers

        # Size of the embedding and hidden state vectors
        self.n_embed = n_embed

        # Vocabulary size derived from the word-to-index mapping
        vocab_size = len(word_to_int)

        # Embedding layer to convert word indices to dense vectors
        self.embedding = nn.Embedding(vocab_size, n_embed)

        # LSTM layer for sequence modeling
        self.lstm = nn.LSTM(
            input_size=self.input_size,     # Input feature size per time step
            hidden_size=self.n_embed,       # Hidden state dimensionality
            num_layers=self.n_layers,       # Number of LSTM layers
            dropout=self.drop_prob,         # Dropout between layers
            batch_first=True                # Input/output tensors have shape (batch, seq, feature)
        )

        # Fully connected layer to project LSTM outputs to vocabulary logits
        self.fc = nn.Linear(input_size, vocab_size)

    # Forward pass through the model
    def forward(self, x, hc):
        # Convert input word indices to embeddings
        embed = self.embedding(x)

        # Pass embeddings through the LSTM with initial hidden/cell states
        x, hc = self.lstm(embed, hc)

        # Project LSTM outputs to vocabulary space
        x = self.fc(x)

        # Return logits and updated hidden/cell states
        return x, hc

    # Method to initialize hidden and cell states for the LSTM
    def init_hidden(self, n_seqs):
        # Get a reference tensor for creating new hidden states
        weight = next(self.parameters()).data

        # Return zero-initialized hidden and cell states with correct dimensions
        return (
            weight.new(self.n_layers, n_seqs, self.n_embed).zero_(),  # Hidden state
            weight.new(self.n_layers, n_seqs, self.n_embed).zero_()   # Cell state
        )