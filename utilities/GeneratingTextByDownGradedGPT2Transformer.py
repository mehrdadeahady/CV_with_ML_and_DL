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
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
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
    from PyQt6.QtGui import  QTextCursor   
    from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt
    from PyQt6.QtWidgets import QMessageBox,QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QTextEdit,QScrollArea,QMainWindow,QApplication
except:
    print("You Should Install PyQt6 Library!")

# Define the main class responsible for managing text generation using a simplified GPT-2 transformer
class GeneratingTextByDownGradedGPT2Transformer(QObject):

    # Initialize the class and its components
    def __init__(self, parent=None):
        # Initialize the base QObject to enable signal-slot communication in PyQt
        super().__init__()

        # Set a fixed random seed for PyTorch to ensure reproducible results
        torch.manual_seed(0)

        # Create a log emitter to send messages to the UI
        self.log_emitter = LogEmitter()

        # Instantiate a popup window for displaying logs during training and processing
        self.DownloadLogPopup = DownloadLogPopup(
            # Pass the log emitter to the popup for real-time updates
            self.log_emitter
        )

        # Placeholder for the raw combined text from input files
        self.raw_text = None

        # List of punctuation characters extracted from the text
        self.punctuations = None

        # Dictionary mapping words to integer indices
        self.word_to_int = None

        # List of token indices representing the full tokenized text
        self.wordidx = None

        # Dictionary mapping indices back to words
        self.int_to_word = None

        # DataLoader for batching token sequences during training
        self.loader = None

        # Select the computation device: use GPU if available, otherwise fallback to CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Configuration object containing model hyperparameters
        self.config = None

        # The GPT-style transformer model instance
        self.model = None

    # Define a method to load and combine three Hemingway novels into a single text
    def LoadText(self):
        # Check if all required text files exist; if any are missing, show a warning and exit
        if (
            not os.path.exists("resources/OldManAndSea.txt") or
            not os.path.exists("resources/ToWhomTheBellTolls.txt") or
            not os.path.exists("resources/FarewellToArms.txt")
        ):
            QMessageBox.warning(None, "Text Books not exist", "Hemingway Books not found.")
            return

        # Open and read the contents of "OldManAndSea.txt" with UTF-8-SIG encoding
        with open("resources/OldManAndSea.txt", "r", encoding='utf-8-sig') as f:
            text = f.read()

        # Convert the text into a list of characters for in-place modification
        text = list(text)

        # Iterate through each character to replace straight quotes with typographic quotes
        for i in range(len(text)):
            # Replace double quotes with opening or closing quotes based on the next character
            if text[i] == '"':
                if i + 1 < len(text) and (text[i + 1] == ' ' or text[i + 1] == '\n'):
                    text[i] = '”'  # Closing quote
                elif i + 1 < len(text):
                    text[i] = '“'  # Opening quote

            # Replace apostrophes with typographic apostrophes if preceded by a non-space
            if text[i] == "'":
                if i - 1 >= 0 and text[i - 1] != ' ' and text[i - 1] != '\n':
                    text[i] = '’'

        # Join the modified character list back into a single string
        text = "".join(text)

        # Open and read the contents of "ToWhomTheBellTolls.txt"
        with open("resources/ToWhomTheBellTolls.txt", "r", encoding='utf-8-sig') as f:
            text1 = f.read()

        # Open and read the contents of "FarewellToArms.txt"
        with open("resources/FarewellToArms.txt", "r", encoding='utf-8-sig') as f:
            text2 = f.read()

        # Combine all three texts into a single string with space separators
        self.raw_text = text + " " + text1 + " " + text2

        # Save the combined text to a new file "ThreeNovels.txt"
        with open("resources/ThreeNovels.txt", "w", encoding='utf-8-sig') as f:
            f.write(self.raw_text)

        # Show a message box confirming successful loading and display a preview of the text
        QMessageBox.information(
            None,
            "Loaded and Combined 3 text books",
            "Text Books Loaded and Combined successfully.\n\n"
            "First 250 Characters in the combined texts:\n\n" + str(self.raw_text[:250])
        )

    # Define a method to tokenize the loaded raw text into word indices
    def TokenizeText(self):
        # Check if raw text has been loaded; if not, show a warning and exit
        if self.raw_text is None:
            QMessageBox.warning(None, "Text not loaded", "First, load the text.")
            return

        # If tokenization has already been done, notify the user and exit
        if self.word_to_int is not None and self.wordidx is not None and self.int_to_word is not None:
            QMessageBox.warning(None, "Text Tokenized", "Text already Tokenized.")
            return

        # Disable the cancel button during tokenization to prevent interruptions
        self.DownloadLogPopup.cancel_button.setEnabled(False)

        # Show the log popup window to display progress
        self.DownloadLogPopup.show()

        # Convert text to lowercase and replace newlines with spaces
        text = self.raw_text.lower().replace("\n", " ")

        # Identify all unique characters in the text
        chars = set(text)

        # Extract punctuation and special characters (non-alphanumeric)
        self.punctuations = [i for i in chars if not i.isalpha() and not i.isdigit()]

        # Log the list of punctuation characters found
        self.DownloadLogPopup.Append_Log("Punctuations in the Text:\n" + str(self.punctuations))

        # Add spaces around punctuation to ensure they are treated as separate tokens
        for x in self.punctuations:
            text = text.replace(f"{x}", f" {x} ")

        # Split the text into tokens based on whitespace
        text_tokenized = text.split()

        # Identify all unique tokens
        unique_tokens = set(text_tokenized)

        # Log the unique tokens found in the text
        self.DownloadLogPopup.Append_Log("\nUnique Tokens in the Text:\n" + str(unique_tokens))

        # Count the frequency of each token
        word_counts = Counter(text_tokenized)

        # Sort tokens by frequency (most common first)
        words = sorted(word_counts, key=word_counts.get, reverse=True)

        # Add a special "UNK" token for unknown words
        words.append("UNK")

        # Calculate total number of tokens and unique vocabulary size
        text_length = len(text_tokenized)
        ntokens = len(words)

        # Initialize the model configuration with the vocabulary size
        self.config = Config(ntokens)

        # Log statistics about the tokenized text
        self.DownloadLogPopup.Append_Log("\n" + f"The text contains {text_length} words")
        self.DownloadLogPopup.Append_Log("\n" + f"There are {ntokens} unique tokens")

        # Create a mapping from word to index
        self.word_to_int = {v: k for k, v in enumerate(words)}

        # Create a reverse mapping from index to word
        self.int_to_word = {v: k for k, v in self.word_to_int.items()}

        # Log the first 10 word-to-index mappings
        self.DownloadLogPopup.Append_Log(
            "\nword_to_int items: Key and Value in First 10 words in the text:\n" +
            str({k: v for k, v in self.word_to_int.items() if k in words[:10]})
        )

        # Log the first 10 index-to-word mappings
        self.DownloadLogPopup.Append_Log(
            "\nint_to_word items: Key and Value in First 10 words in the text:\n" +
            str({k: v for k, v in self.int_to_word.items() if v in words[:10]})
        )

        # Log the first 20 tokens from the tokenized text
        self.DownloadLogPopup.Append_Log(
            "\nFirst 20 chars in tokenized text:\n" + str(text_tokenized[:20])
        )

        # Convert the tokenized text into a list of corresponding token indices
        self.wordidx = [self.word_to_int[w] for w in text_tokenized]

        # Log the first 20 token indices
        self.DownloadLogPopup.Append_Log(
            "\nFirst 20 indexes of chars in tokenized text:\n" +
            str(self.wordidx[:20])
        )

        # Final log message indicating tokenization is complete
        self.DownloadLogPopup.Append_Log(
            "\nWord Tokenization of the Text finished, ready for creating batches."
        )

    # Define a method to create training batches from tokenized word indices
    def CreateBatches(self):
        # If batches have already been created, notify the user and exit
        if self.loader is not None:
            QMessageBox.warning(None, "Batches Created", "Batches already Created.")
            return

        # If tokenized word indices are not available, prompt the user to tokenize first
        if self.wordidx is None:
            QMessageBox.warning(None, "Text not Tokenized", "First, Tokenize the text.")
            return

        # Disable the cancel button during batch creation to prevent interruptions
        self.DownloadLogPopup.cancel_button.setEnabled(False)

        # Show the log popup window to display progress
        self.DownloadLogPopup.show()
        self.DownloadLogPopup.Append_Log("Creating Batches of Tokens.\nWait...")

        # Define the fixed sequence length for each training sample
        seq_len = 128

        # Initialize a list to hold (input, target) sequence pairs
        xys = []

        # Slide a window of size `seq_len` over the tokenized text to create sequences
        for n in range(0, len(self.wordidx) - seq_len - 1):
            # Input sequence of length `seq_len`
            x = self.wordidx[n : n + seq_len]

            # Target sequence is the input shifted by one position
            y = self.wordidx[n + 1 : n + seq_len + 1]

            # Convert input and target sequences to tensors and append as a tuple
            xys.append((torch.tensor(x), torch.tensor(y)))

        # Define the batch size for training
        batch_size = 32

        # Create a DataLoader to yield batches of (x, y) pairs, shuffled for training
        self.loader = DataLoader(xys, batch_size=batch_size, shuffle=True)

        # Retrieve the first batch to preview its structure
        x, y = next(iter(self.loader))

        # Log the first batch of input sequences
        self.DownloadLogPopup.Append_Log("\nX:\n" + str(x))

        # Log the corresponding target sequences
        self.DownloadLogPopup.Append_Log("\nY:\n" + str(y))

        # Log the shape of the input and target tensors
        self.DownloadLogPopup.Append_Log("\nShape of X and Y:\n" + str(x.shape) + " <> " + str(y.shape))

        # Final log message indicating batch creation is complete
        self.DownloadLogPopup.Append_Log("\nCreating Batches Finished, ready for Training.")

    # Define a method to create and initialize the model based on the current configuration
    def CreateModel(self):
        # If the model has already been created, notify the user and exit
        if self.model is not None:
            QMessageBox.warning(None, "Model Created", "Model already Created.")
            return

        # If configuration is missing (i.e., text not tokenized), prompt the user and exit
        if self.config is None:
            QMessageBox.warning(None, "Text not Tokenized", "First, Tokenize the text.")
            return

        # Instantiate the model using the current configuration and move it to the target device
        self.model = Model(self.config, self.device).to(self.device)

        # Calculate the total number of parameters in the transformer component
        num = sum(p.numel() for p in self.model.transformer.parameters())

        # Display a scrollable message showing model creation success and parameter count
        show_scrollable_message(
            "Model Created Successfully",
            "Number of Parameters: " + str(num / 1e6) + "\n\n" + str(self.model)
        )

    # Define a method to initiate model training in a separate thread
    def TrainModel(self):
        # Check if the training dataset (batches) has been created
        if self.loader is None:
            # Warn the user to prepare the dataset before training
            QMessageBox.warning(None, "Batches Not Ready", "Please Create Batches first.")

        # Check if the model has been instantiated
        elif self.model is None:
            # Warn the user to create the model before starting training
            QMessageBox.warning(None, "Model Not Found", "Please create the model first.")

        # Proceed with training only if both dataset and model are ready
        else:
            # Enable the cancel button to allow user interruption during training
            self.DownloadLogPopup.cancel_button.setEnabled(True)

            # Show the log popup window to the user
            self.DownloadLogPopup.show()

            # Log the start of the training process
            self.DownloadLogPopup.Append_Log("Training model...\nPlease wait.")

            # Create a separate thread to run the training process asynchronously
            self.training_thread = TrainingDownGradedGPTThread(
                # Reference to the log popup for status updates
                self.DownloadLogPopup,

                # DataLoader containing training batches
                self.loader,

                # Model to be trained
                self.model,

                # Device (CPU or GPU) to run the training on
                self.device,
            )

            # Connect the thread's log signal to the popup's log appending method
            self.training_thread.log_signal.connect(self.DownloadLogPopup.Append_Log)

            # Connect the cancel button to the thread's stop method to allow user to halt training
            self.DownloadLogPopup.cancel_button.clicked.connect(self.training_thread.stop)

            # Start the training thread to begin model training
            self.training_thread.start()

    # Define a method to generate new tokens from a prompt using the trained model
    def sample(self, idx, weights, max_new_tokens, temperature=1.0, top_k=None):
        # Set the model to evaluation mode (disables dropout, etc.)
        self.model.eval()

        # Load the trained model weights from the specified file
        self.model.load_state_dict(torch.load(weights, map_location=torch.device(self.device)))

        # Record the original length of the input sequence to separate new tokens later
        original_length = len(idx[0])

        # Generate tokens one at a time, up to the specified maximum
        for _ in range(max_new_tokens):
            # If the input is longer than the block size, truncate it to the last `block_size` tokens
            if idx.size(1) <= self.config.block_size:
                idx_cond = idx
            else:
                idx_cond = idx[:, -self.config.block_size:]

            # Run the model to get logits for the current input
            logits = self.model(idx_cond.to(self.device))

            # Select the logits corresponding to the last token in the sequence
            logits = logits[:, -1, :] / temperature  # Apply temperature scaling

            # If top_k is specified, filter logits to retain only the top_k highest values
            if top_k is not None:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = -float('Inf')  # Mask out lower logits

            # Convert logits to probabilities using softmax
            probs = F.softmax(logits, dim=-1)

            # Sample the next token from the probability distribution
            idx_next = torch.multinomial(probs, num_samples=1)

            # Append the sampled token to the sequence
            idx = torch.cat((idx, idx_next.cpu()), dim=1)

        # Return only the newly generated tokens (excluding the original prompt)
        return idx[:, original_length:]
    
    # Define a method to generate text from a prompt using the trained model
    def generate(self, prompt, weights, max_new_tokens, temperature=1.0, top_k=None):
        # Retrieve the index for unknown tokens
        UNK = self.word_to_int["UNK"]

        # Ensure the prompt is not empty
        assert len(prompt) > 0, "prompt must contain at least one token"

        # Preprocess the prompt: lowercase and replace newlines with spaces
        text = prompt.lower().replace("\n", " ")

        # Add spaces around punctuation to treat them as separate tokens
        for x in self.punctuations:
            text = text.replace(f"{x}", f" {x} ")

        # Tokenize the prompt into words
        text_tokenized = text.split()

        # Convert tokens to indices, using UNK for unknown words
        idx = [self.word_to_int.get(w, UNK) for w in text_tokenized]

        # Convert to a tensor and add a batch dimension
        idx = torch.LongTensor(idx).unsqueeze(0)

        # Generate new tokens from the model using the sampling method
        idx = self.sample(idx, weights, max_new_tokens, temperature=temperature, top_k=top_k)

        # Convert generated indices back to tokens
        tokens = [self.int_to_word[i] for i in idx.squeeze().numpy()]

        # Join tokens into a single string
        text = " ".join(tokens)

        # Remove extra spaces before closing punctuation
        for x in '''”).:;!?,-‘’''':
            text = text.replace(f" {x}", f"{x}")

        # Remove extra spaces after opening punctuation
        for x in '''“(-‘’''':
            text = text.replace(f"{x} ", f"{x}")

        # Return the original prompt followed by the generated text
        return prompt + " " + text

    # Define a method to generate text using a trained model based on the selected UI button
    def GenerateTextByModel(self):
        # Check if all required model checkpoints exist; if not, alert the user and exit
        if (
            not os.path.exists("resources/models/GPTe10.pth") or
            not os.path.exists("resources/models/GPTe20.pth") or
            not os.path.exists("resources/models/GPTe40.pth")
        ):
            QMessageBox.warning(
                None,
                "Models Not Ready",
                "Please, first Create, Train and Save models.\n"
            )
            return

        # Ensure tokenized data and vocabulary mappings are available
        if self.wordidx is None or self.word_to_int is None or self.int_to_word is None:
            QMessageBox.warning(None, "Text not Tokenized", "First, Load and Tokenize the text.")
            return

        # Ensure the model has been created before attempting generation
        if self.model is None:
            QMessageBox.warning(None, "Model Not Found", "Please create the model first.")
            return

        # Disable the cancel button during generation to prevent interruptions
        self.DownloadLogPopup.cancel_button.setEnabled(False)

        # Show the log popup window to display generation progress
        self.DownloadLogPopup.show()
        self.DownloadLogPopup.Append_Log(
            "Text generation is in progress.\nThis may take up to 1 minutes.\nPlease wait..."
        )

        # Identify which UI button triggered the generation
        sender = self.sender().objectName()

        # Default number of training epochs (can be updated per case)
        number_of_epochs_trained = 10

        # Match the sender button to a specific generation configuration
        match sender:
            # Generate from model trained for 10 epochs using prompt 1
            case "pushButton_GenerateTextBy10EpochsTrainedModelPrompt1_GeneratingTextByDownGradedGPT2Transformer":
                prompt = "UNK"
                number_of_epochs_trained = 10
                self.DownloadLogPopup.Append_Log(
                    self.generate(prompt, 'resources/models/GPTe10.pth', max_new_tokens=50)[4:]
                )

            # Generate from model trained for 20 epochs using prompt 1
            case "pushButton_GenerateTextBy20EpochsTrainedModelPrompt1_GeneratingTextByDownGradedGPT2Transformer":
                prompt = "UNK"
                number_of_epochs_trained = 20
                for i in range(10):
                    self.DownloadLogPopup.Append_Log(
                        self.generate(prompt, 'resources/models/GPTe20.pth', max_new_tokens=20)[4:]
                    )
                    self.DownloadLogPopup.Append_Log("-" * 50)

            # Generate from model trained for 40 epochs using prompt 1
            case "pushButton_GenerateTextBy40EpochsTrainedModelPrompt1_GeneratingTextByDownGradedGPT2Transformer":
                prompt = "UNK"
                number_of_epochs_trained = 40
                for i in range(10):
                    torch.manual_seed(i)
                    self.DownloadLogPopup.Append_Log(
                        self.generate(prompt, 'resources/models/GPTe40.pth', max_new_tokens=20)[4:]
                    )
                    self.DownloadLogPopup.Append_Log("-" * 50)

            # Generate from model trained for 10 epochs using prompt 2
            case "pushButton_GenerateTextBy10EpochsTrainedModelPrompt2_GeneratingTextByDownGradedGPT2Transformer":
                prompt = "the old man saw the shark near the"
                number_of_epochs_trained = 10
                self.DownloadLogPopup.Append_Log(
                    self.generate(
                        prompt,
                        'resources/models/GPTe40.pth',
                        max_new_tokens=50,
                        temperature=0.95,
                        top_k=100
                    )
                )

            # Generate from model trained for 20 epochs using prompt 2
            case "pushButton_GenerateTextBy20EpochsTrainedModelPrompt2_GeneratingTextByDownGradedGPT2Transformer":
                prompt = "the old man saw the shark near the"
                number_of_epochs_trained = 20
                for i in range(10):
                    torch.manual_seed(i)
                    self.DownloadLogPopup.Append_Log(
                        self.generate(
                            prompt,
                            'resources/models/GPTe20.pth',
                            max_new_tokens=20,
                            temperature=0.9,
                            top_k=50
                        )
                    )
                    self.DownloadLogPopup.Append_Log("-" * 50)

            # Generate from model trained for 40 epochs using prompt 2
            case "pushButton_GenerateTextBy40EpochsTrainedModelPrompt2_GeneratingTextByDownGradedGPT2Transformer":
                prompt = "the old man saw the shark near the"
                number_of_epochs_trained = 40
                for i in range(10):
                    torch.manual_seed(i)
                    self.DownloadLogPopup.Append_Log(
                        self.generate(prompt, 'resources/models/GPTe40.pth', max_new_tokens=20)
                    )
                    self.DownloadLogPopup.Append_Log("-" * 50)

        # Log the final summary of the generation process
        self.DownloadLogPopup.Append_Log(
            "\n" + f"Generating Above Text from prompt:\n{prompt}\n"
            f"with Model Trained : {number_of_epochs_trained} Epochs Finished."
        )

# Define a QThread subclass to handle model training in a separate thread
class TrainingDownGradedGPTThread(QThread):

    # Signal to emit log messages to the UI (e.g., training progress updates)
    log_signal = pyqtSignal(str)

    # Signal to trigger visualization updates (e.g., after each epoch)
    display_signal = pyqtSignal(int)

    # Initialize the training thread with UI popup, data loader, model, and device
    def __init__(self, DownloadLogPopup, loader, model, device):
        # Call the parent QThread constructor
        super().__init__()

        # Reference to the popup window used for displaying logs
        self.DownloadLogPopup = DownloadLogPopup

        # DataLoader providing batches of training data
        self.loader = loader

        # The LSTM model to be trained
        self.model = model

        # Device on which training will run (e.g., 'cpu' or 'cuda')
        self.device = device

        # Learning rate for the optimizer
        self.lr = 0.0001

        # Adam optimizer for model training
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

        # CrossEntropyLoss for sequence classification
        self.loss_func = nn.CrossEntropyLoss()

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
            for epoch in range(1, 41):

                # Exit early if stop was requested
                if self._stop_requested:
                    break

                # Initialize total loss for the epoch
                total_loss = 0

                # Loop through each batch in the data loader, starting index at 1
                for iteration, (x, y) in enumerate(self.loader, 1):

                    # Check again for stop request
                    if self._stop_requested:
                        self.log_signal.emit("Training stopped by user.")
                        break

                    # Move input and target tensors to the specified device
                    x, y = x.to(self.device), y.to(self.device)

                    # Forward pass through the model
                    output = self.model(x)

                    # Compute loss using CrossEntropy
                    loss = self.loss_func(output.view(-1, output.size(-1)), y.view(-1))

                    # Zero out gradients before backpropagation
                    self.optimizer.zero_grad()

                    # Backpropagate the loss
                    loss.backward()

                    # Clip gradients to prevent exploding gradients
                    nn.utils.clip_grad_norm_(self.model.parameters(), 1)

                    # Update model parameters
                    self.optimizer.step()

                    # Accumulate loss for the epoch
                    total_loss += loss.item()

                    # Log progress every 100 iterations (batches)
                    if iteration % 100 == 0:
                        self.log_signal.emit(
                            f"Epoch {epoch}, Iteration {iteration}, Average Loss = {total_loss / iteration:.4f}"
                        )

                # Log average loss for the epoch if any iterations occurred
                if iteration > 0:
                    self.log_signal.emit(f"Epoch {epoch} Loss = {total_loss / iteration:.4f}")
                else:
                    self.log_signal.emit(f"Epoch {epoch} skipped (no data)")

                # Save model checkpoint every 10 epochs
                if epoch % 10 == 0:
                    torch.save(self.model.state_dict(), f'resources/models/GPTe{epoch}_.pth')

            # Emit a message indicating training is complete
            self.log_signal.emit("Training Finished.")

            # Scroll the log output to the bottom to show final messages
            self.DownloadLogPopup.log_output.moveCursor(QTextCursor.MoveOperation.End)
            self.DownloadLogPopup.log_output.ensureCursorVisible()

            # Process any pending UI events to refresh the interface
            QApplication.processEvents()

        except Exception as e:
            # Emit an error message if training fails
            self.log_signal.emit(f"Error during training: {str(e)}")

# Define the main language model class inheriting from nn.Module
class Model(nn.Module):
    # Initialize the model with configuration parameters
    def __init__(self, config, device):
        # Call the base class constructor
        super().__init__()

        # Store the maximum sequence length (context window)
        self.block_size = config.block_size
        self.device = device

        # Define the transformer architecture using a ModuleDict
        self.transformer = nn.ModuleDict(dict(
            # Token embedding layer: maps token indices to embedding vectors
            wte = nn.Embedding(config.vocab_size, config.n_embd),

            # Positional embedding layer: encodes position information
            wpe = nn.Embedding(config.block_size, config.n_embd),

            # Dropout layer for regularization
            drop = nn.Dropout(config.embd_pdrop),

            # Stack of transformer blocks (e.g., multi-head attention + feedforward)
            h = nn.ModuleList([Block(config) for _ in range(config.n_layer)]),

            # Final layer normalization after all transformer blocks
            ln_f = nn.LayerNorm(config.n_embd),
        ))

        # Output projection layer mapping embeddings to vocabulary logits
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

        # Custom initialization for projection weights in attention blocks
        for pn, p in self.named_parameters():
            # Apply scaled normal initialization to projection weights
            if pn.endswith('c_proj.weight'):
                torch.nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * config.n_layer))

    # Define the forward pass of the model
    def forward(self, idx, targets=None):
        # Get batch size (b) and sequence length (t) from input tensor shape
        b, t = idx.size()

        # Create position indices for positional embeddings
        pos = torch.arange(0, t, dtype=torch.long).unsqueeze(0).to(self.device)

        # Look up token embeddings for input indices
        tok_emb = self.transformer.wte(idx)

        # Look up positional embeddings
        pos_emb = self.transformer.wpe(pos)

        # Add token and positional embeddings, then apply dropout
        x = self.transformer.drop(tok_emb + pos_emb)

        # Pass the input through each transformer block sequentially
        for block in self.transformer.h:
            x = block(x)

        # Apply final layer normalization
        x = self.transformer.ln_f(x)

        # Project the final hidden states to vocabulary logits
        logits = self.lm_head(x)

        # Return the logits (optionally used for loss computation externally)
        return logits  

# Define a single transformer block used in the model architecture
class Block(nn.Module):
    # Initialize the transformer block with the given configuration
    def __init__(self, config):
        # Call the base class constructor
        super().__init__()

        # First layer normalization applied before self-attention
        self.ln_1 = nn.LayerNorm(config.n_embd)

        # Causal self-attention layer to preserve autoregressive property
        self.attn = CausalSelfAttention(config)

        # Second layer normalization applied before the feedforward network
        self.ln_2 = nn.LayerNorm(config.n_embd)

        # Define the feedforward MLP using a ModuleDict for clarity and modularity
        self.mlp = nn.ModuleDict(dict(
            # Fully connected layer expanding the embedding dimension by 4x
            c_fc   = nn.Linear(config.n_embd, 4 * config.n_embd),

            # Projection layer reducing back to original embedding size
            c_proj = nn.Linear(4 * config.n_embd, config.n_embd),

            # Activation function (Gaussian Error Linear Unit)
            act    = GELU(),

            # Dropout layer for regularization
            dropout = nn.Dropout(config.resid_pdrop),
        ))

        # Define the MLP forward pass as a lambda function for brevity
        m = self.mlp
        self.mlpf = lambda x: m.dropout(m.c_proj(m.act(m.c_fc(x))))

    # Define the forward pass through the transformer block
    def forward(self, x):
        # Apply first layer norm, then self-attention, and add residual connection
        x = x + self.attn(self.ln_1(x))

        # Apply second layer norm, then MLP, and add residual connection
        x = x + self.mlpf(self.ln_2(x))

        # Return the transformed tensor
        return x
    
# Define a causal self-attention module for autoregressive transformers
class CausalSelfAttention(nn.Module):
    # Initialize the attention module with the given configuration
    def __init__(self, config):
        # Call the base class constructor
        super().__init__()

        # Linear layer to compute concatenated queries, keys, and values from input
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)

        # Linear projection layer applied after attention output
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)

        # Dropout applied to attention weights for regularization
        self.attn_dropout = nn.Dropout(config.attn_pdrop)

        # Dropout applied to the final output of the attention block
        self.resid_dropout = nn.Dropout(config.resid_pdrop)

        # Register a lower-triangular mask to enforce causality (no peeking ahead)
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(config.block_size, config.block_size))
            .view(1, 1, config.block_size, config.block_size)
        )

        # Number of attention heads
        self.n_head = config.n_head

        # Embedding dimension (must be divisible by number of heads)
        self.n_embd = config.n_embd

    # Define the forward pass of the attention mechanism
    def forward(self, x):
        # Extract batch size (B), sequence length (T), and embedding dim (C)
        B, T, C = x.size()

        # Compute queries, keys, and values by splitting the projection output
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)

        # Compute the size of each attention head
        hs = C // self.n_head

        # Reshape and transpose keys for multi-head attention: (B, n_head, T, hs)
        k = k.view(B, T, self.n_head, hs).transpose(1, 2)

        # Reshape and transpose queries similarly
        q = q.view(B, T, self.n_head, hs).transpose(1, 2)

        # Reshape and transpose values similarly
        v = v.view(B, T, self.n_head, hs).transpose(1, 2)

        # Compute scaled dot-product attention scores
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))

        # Apply causal mask to prevent attention to future positions
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float('-inf'))

        # Normalize attention scores using softmax
        att = F.softmax(att, dim=-1)

        # Apply dropout to attention weights
        att = self.attn_dropout(att)

        # Compute weighted sum of values using attention weights
        y = att @ v

        # Reshape and merge attention heads back into original embedding dimension
        y = y.transpose(1, 2).contiguous().view(B, T, C)

        # Apply final projection and dropout to the attention output
        y = self.resid_dropout(self.c_proj(y))

        # Return the final output tensor
        return y
    
# Define a configuration class to store hyperparameters for the model
class Config():
    # Initialize the configuration with vocabulary size
    def __init__(self, ntokens):
        # Number of transformer blocks (depth of the model)
        self.n_layer = 3

        # Number of attention heads in each block
        self.n_head = 4

        # Dimensionality of token embeddings and hidden states
        self.n_embd = 256

        # Size of the vocabulary (number of unique tokens)
        self.vocab_size = ntokens

        # Maximum sequence length (context window size)
        self.block_size = 128

        # Dropout probability for token and positional embeddings
        self.embd_pdrop = 0.1

        # Dropout probability for residual connections
        self.resid_pdrop = 0.1

        # Dropout probability for attention weights
        self.attn_pdrop = 0.1

# Define a custom GELU activation function as a PyTorch module
class GELU(nn.Module):
    # Define the forward computation of the GELU function
    def forward(self, x):
        # Apply the Gaussian Error Linear Unit (GELU) approximation
        # Formula: 0.5 * x * (1 + tanh(√(2/π) * (x + 0.044715 * x³)))
        return 0.5 * x * (
            1.0 + torch.tanh(
                math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0))
            )
        )


