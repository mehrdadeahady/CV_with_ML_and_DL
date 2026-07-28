import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
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
import io
import sys
import contextlib
import time
import pickle
import shutil
import random
import tkinter as tk
import threading
import math
from copy import deepcopy
from collections import Counter
from utilities.DeepLearningFoundationOperations import DownloadLogPopup, LogEmitter
from utilities.DLbyPyTorch import EarlyStop, DLbyPyTorch, PopupStream
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
    from PyQt6.QtGui import  QTextCursor   
    from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt
    from PyQt6.QtWidgets import QMessageBox,QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QTextEdit,QScrollArea,QMainWindow,QApplication
except:
    print("You Should Install PyQt6 Library!")

# Define a class for creating a Transformer-based translator
class CreateTranslatorByTransformer(QObject):

    # Constructor method for initializing the translator object
    def __init__(self, parent=None):
        # Call the constructor of the parent QObject class to enable signal-slot functionality
        super().__init__()

        # Set a fixed seed for PyTorch to ensure reproducibility of training results
        torch.manual_seed(0)

        # Initialize a custom signal emitter for logging messages to the UI
        self.log_emitter = LogEmitter()

        # Define a local directory to store the model/tokenizer
        local_dir = "temp/xlm-clm-enfr-1024"

        if os.path.exists(local_dir):
           try:
               # Load the tokenizer from local directory
               self.tokenizer = XLMTokenizer.from_pretrained(local_dir, local_files_only=True)
           except Exception as e:
                QMessageBox.critical(None,"Error","Couldn't download XLMTokenizer.\n"+e)
        else:
            # Download/Load a pre-trained multilingual tokenizer from the XLM model family
            self.tokenizer = XLMTokenizer.from_pretrained("xlm-clm-enfr-1024")

            # Save the tokenizer files to disk
            self.tokenizer.save_pretrained(local_dir)

        # Placeholder for the input DataFrame containing training data
        self.df = None

        # Define the padding token index used in sequences
        self.PAD = 0

        # Define the unknown token index for out-of-vocabulary words
        self.UNK = 1

        # English word-to-index dictionary (word → ID)
        self.en_word_dict = None

        # English index-to-word dictionary (ID → word)
        self.en_idx_dict = None

        # French word-to-index dictionary (word → ID)
        self.fr_word_dict = None

        # French index-to-word dictionary (ID → word)
        self.fr_idx_dict = None

        # Tokenized English sentences (list of token ID sequences)
        self.en_tokens = None

        # Tokenized French sentences (list of token ID sequences)
        self.fr_tokens = None

        # Set the device for model training and inference (GPU if available, else CPU)
        self.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        # Placeholder for the batch loader that will yield training batches
        self.BatchLoader = None

        # Placeholder for the Transformer model instance
        self.model = None

    # Method to load the bilingual dictionary from a CSV file
    def LoadDictionary(self):
        # Check if the dictionary CSV file exists at the specified path
        if os.path.exists("resources/en2fr.csv"):
            # Read the CSV file into a pandas DataFrame
            self.df = pd.read_csv("resources/en2fr.csv")

            # Get the total number of examples in the DataFrame
            dataframe_length = len(self.df)

            # Display a message box showing the number of examples and sample entries at index 30856
            QMessageBox.warning(
                None,
                "Dictionary Loaded:",
                f"There are {dataframe_length} examples in the training data"
                + "\n\nEnglish Value in index 30856 for test:\n" + self.df.iloc[30856]["en"]
                + "\n\nFrench Value in index 30856 for test:\n" + self.df.iloc[30856]["fr"]
            )
        else:
            # Show a warning message if the dictionary file is not found
            QMessageBox.warning(None, "No Dictionary File", "Sample Dictionary not Found!")

    # Method to tokenize English and French text using subword units and build token dictionaries
    def SubWordTokenizingDictionary(self):
        # Check if the dictionary DataFrame is loaded
        if self.df is None:
            QMessageBox.warning(None, "No Dictionary Loaded", "First, Load the Dictionary!")
            return

        # Create a popup window to display real-time logs during tokenization
        self.DownloadLogPopup = DownloadLogPopup(
            # Pass the log emitter to stream messages to the popup
            self.log_emitter
        )

        # Disable the cancel button during tokenization
        self.DownloadLogPopup.cancel_button.setEnabled(False)

        # Show the log popup window to the user
        self.DownloadLogPopup.show()

        # Log the start of the tokenization process
        self.DownloadLogPopup.Append_Log("SubWord Tokenizing Dictionary.")

        # Internal function to tokenize English text and build dictionaries
        def tokenizing_en():
            self.DownloadLogPopup.Append_Log("\nTokenizing English started.\nPlease wait...\n")

            # Extract English sentences from the DataFrame
            en = self.df["en"].tolist()

            # Tokenize each sentence using the tokenizer and add BOS/EOS tokens
            self.en_tokens = [["BOS"] + self.tokenizer.tokenize(x) + ["EOS"] for x in en]

            # Count frequency of each token across all sentences
            word_count = Counter()
            for sentence in self.en_tokens:
                for word in sentence:
                    word_count[word] += 1

            # Select the top 50,000 most frequent tokens
            frequency = word_count.most_common(50000)
            total_en_words = len(frequency) + 2  # Account for PAD and UNK

            # Create word-to-index dictionary with reserved indices for PAD and UNK
            self.en_word_dict = {w[0]: idx + 2 for idx, w in enumerate(frequency)}
            self.en_word_dict["PAD"] = self.PAD
            self.en_word_dict["UNK"] = self.UNK

            # Create index-to-word dictionary for reverse lookup
            self.en_idx_dict = {v: k for k, v in self.en_word_dict.items()}

            self.DownloadLogPopup.Append_Log("\nTokenizing English finished.\nPlease wait for testing...\n")

            # Run a test to verify tokenization and dictionary mapping
            test_tokenized_en()

            self.DownloadLogPopup.Append_Log("\nTesting Tokenized English finished.\nPlease wait for french...\n")

        # Internal function to test English tokenization and dictionary mappings
        def test_tokenized_en():
            # Tokenize a sample sentence
            tokenized_en = self.tokenizer.tokenize("I don't speak French.")

            # Convert tokens to indices using the English dictionary
            enidx = [self.en_word_dict.get(i, self.UNK) for i in tokenized_en]

            # Log the tokenized form and corresponding indices
            self.DownloadLogPopup.Append_Log(
                "\nTesting English Tokens.\nRaw Sample:\nI don't speak French.\n"
                "Tokenized Sample:\n" + str(tokenized_en) +
                "\nIndex of Tokens in Dictionary:\n" + str(enidx)
            )

            # Convert indices back to tokens using the reverse dictionary
            entokens = [self.en_idx_dict.get(i, "UNK") for i in enidx]
            self.DownloadLogPopup.Append_Log("\nGet Tokens from Dictionary by Index:\n" + str(entokens))

            # Reconstruct the original phrase from tokens
            en_phrase = "".join(entokens)
            en_phrase = en_phrase.replace("</w>", " ")
            for x in '''?:;.,'("-!&)%''':
                en_phrase = en_phrase.replace(f" {x}", f"{x}")

            # Log the reconstructed phrase
            self.DownloadLogPopup.Append_Log("\nConvert Tokens to original raw Text:\n" + str(en_phrase))

        # Internal function to tokenize French text and build dictionaries
        def tokenizing_fr():
            self.DownloadLogPopup.Append_Log("\nTokenizing French started.\nPlease wait...\n")

            # Extract French sentences from the DataFrame
            fr = self.df["fr"].tolist()

            # Tokenize each sentence and add BOS/EOS tokens
            self.fr_tokens = [["BOS"] + self.tokenizer.tokenize(x) + ["EOS"] for x in fr]

            # Count frequency of each token
            word_count = Counter()
            for sentence in self.fr_tokens:
                for word in sentence:
                    word_count[word] += 1

            # Select the top 50,000 most frequent tokens
            frequency = word_count.most_common(50000)
            total_fr_words = len(frequency) + 2

            # Create word-to-index dictionary for French
            self.fr_word_dict = {w[0]: idx + 2 for idx, w in enumerate(frequency)}
            self.fr_word_dict["PAD"] = self.PAD
            self.fr_word_dict["UNK"] = self.UNK

            # Create index-to-word dictionary for French
            self.fr_idx_dict = {v: k for k, v in self.fr_word_dict.items()}

            self.DownloadLogPopup.Append_Log("\nTokenizing French finished.\nPlease wait for testing...\n")

            # Run a test to verify French tokenization and dictionary mapping
            test_tokenized_fr()

            self.DownloadLogPopup.Append_Log("\nTesting Tokenized french finished.\n")

        # Internal function to test French tokenization and dictionary mappings
        def test_tokenized_fr():
            # Tokenize a sample French sentence
            tokenized_fr = self.tokenizer.tokenize("Je ne parle pas français.")

            # Convert tokens to indices using the French dictionary
            fridx = [self.fr_word_dict.get(i, self.UNK) for i in tokenized_fr]

            # Log the tokenized form and corresponding indices
            self.DownloadLogPopup.Append_Log(
                "\nTesting French Tokens.\nRaw Sample:\nJe ne parle pas français.\n"
                "Tokenized Sample:\n" + str(tokenized_fr) +
                "\nIndex of Tokens in Dictionary:\n" + str(fridx)
            )

            # Convert indices back to tokens using the reverse dictionary
            frtokens = [self.fr_idx_dict.get(i, "UNK") for i in fridx]
            self.DownloadLogPopup.Append_Log("\nGet Tokens from Dictionary by Index:\n" + str(frtokens))

            # Reconstruct the original phrase from tokens
            fr_phrase = "".join(frtokens)
            fr_phrase = fr_phrase.replace("</w>", " ")
            for x in '''?:;.,'("-!&)%''':
                fr_phrase = fr_phrase.replace(f" {x}", f"{x}")

            # Log the reconstructed phrase
            self.DownloadLogPopup.Append_Log("\nConvert Tokens to original raw Text:\n" + str(fr_phrase))

        # Internal function to save the tokenized dictionaries to a file
        def save_tokenized_dictionary():
            # Ensure all dictionaries are initialized before saving
            if self.en_word_dict is not None and self.en_idx_dict is not None and \
               self.fr_word_dict is not None and self.fr_idx_dict is not None:
                # Save dictionaries using pickle
                with open("resources/dict.p", "wb") as fb:
                    pickle.dump((self.en_word_dict, self.en_idx_dict, self.fr_word_dict, self.fr_idx_dict), fb)
                self.DownloadLogPopup.Append_Log("\nTokenized Dictionary Saved in: resources/dict.p.\n")

        # Execute the tokenization and saving steps in order
        tokenizing_en()
        tokenizing_fr()
        save_tokenized_dictionary()

    # Method to prepare tokenized data for training by batching and sorting
    def PrepareData(self):
        # Check if data has already been prepared; if so, notify and exit
        if self.BatchLoader is not None:
            QMessageBox.warning(None, "Data Prepared", "Data already Prepared.")
            return

        # Ensure that both English and French dictionaries are available
        if self.en_word_dict is None or self.fr_word_dict is None:
            QMessageBox.warning(None, "Dictionary not ready", "First, load and tokenize the dictionary.")
            return

        # Convert English token sequences to index sequences using the English dictionary
        out_en_ids = [[self.en_word_dict.get(w, self.UNK) for w in s] for s in self.en_tokens]

        # Convert French token sequences to index sequences using the French dictionary
        out_fr_ids = [[self.fr_word_dict.get(w, self.UNK) for w in s] for s in self.fr_tokens]

        # Sort sentence indices by length of English sequences (for efficient batching)
        sorted_ids = sorted(range(len(out_en_ids)), key=lambda x: len(out_en_ids[x]))

        # Reorder English and French sequences based on sorted indices
        out_en_ids = [out_en_ids[x] for x in sorted_ids]
        out_fr_ids = [out_fr_ids[x] for x in sorted_ids]

        # Define the batch size for training
        batch_size = 128

        # Create shuffled starting indices for each batch
        idx_list = np.arange(0, len(self.en_tokens), batch_size)
        np.random.shuffle(idx_list)

        # Generate list of index arrays, each representing a batch
        batch_indexs = []
        for idx in idx_list:
            batch_indexs.append(np.arange(idx, min(len(self.en_tokens), idx + batch_size)))

        # Initialize the BatchLoader with the prepared batches and tokenized data
        self.BatchLoader = BatchLoader(batch_indexs, out_en_ids, out_fr_ids, self.DEVICE)

        # Instantiate a PositionalEncoding layer to initialize its internal buffers
        pe = PositionalEncoding(256, 0.1, DEVICE=self.DEVICE)

        # Create a dummy input tensor to trigger the forward pass (useful for buffer initialization)
        x = torch.zeros(1, 8, 256).to(self.DEVICE)
        y = pe.forward(x)

        # Notify the user that data preparation is complete
        QMessageBox.information(None, "Data Prepared", "Data Prepared.")

    # Method to create and initialize the Transformer model architecture
    def CreateModel(self):
        # Check if the model already exists; if so, notify and exit
        if self.model is not None:
            QMessageBox.warning(None, "Model Exist", "Model already Created.")
            return

        # Ensure that both English and French dictionaries are available
        if self.en_word_dict is None or self.fr_word_dict is None:
            QMessageBox.warning(None, "Dictionary not ready", "First, load and tokenize the dictionary.")
            return

        # Determine the vocabulary sizes for source (English) and target (French) languages
        src_vocab = len(self.en_word_dict)
        tgt_vocab = len(self.fr_word_dict)

        # Define Transformer hyperparameters
        N = 6               # Number of layers in both encoder and decoder
        d_model = 256       # Dimensionality of input/output embeddings and hidden states
        d_ff = 1024         # Dimensionality of the feed-forward network
        h = 8               # Number of attention heads
        dropout = 0.1       # Dropout rate for regularization

        # Instantiate multi-headed attention module
        attn = MultiHeadedAttention(h, d_model).to(self.DEVICE)

        # Instantiate position-wise feed-forward network
        ff = PositionwiseFeedForward(d_model, d_ff, dropout).to(self.DEVICE)

        # Instantiate positional encoding module
        pos = PositionalEncoding(d_model, dropout, DEVICE=self.DEVICE).to(self.DEVICE)

        # Construct the Transformer model with encoder, decoder, embeddings, and generator
        model = Transformer(
            # Encoder: stack of N encoder layers
            Encoder(
                EncoderLayer(d_model, deepcopy(attn), deepcopy(ff), dropout).to(self.DEVICE),
                N
            ).to(self.DEVICE),

            # Decoder: stack of N decoder layers with self-attention and encoder-decoder attention
            Decoder(
                DecoderLayer(d_model, deepcopy(attn), deepcopy(attn), deepcopy(ff), dropout).to(self.DEVICE),
                N
            ).to(self.DEVICE),

            # Source embedding: token embedding + positional encoding
            nn.Sequential(
                Embeddings(d_model, src_vocab).to(self.DEVICE),
                deepcopy(pos)
            ),

            # Target embedding: token embedding + positional encoding
            nn.Sequential(
                Embeddings(d_model, tgt_vocab).to(self.DEVICE),
                deepcopy(pos)
            ),

            # Output generator: maps decoder output to vocabulary logits
            Generator(d_model, tgt_vocab)
        ).to(self.DEVICE)

        # Initialize model parameters using Xavier uniform initialization for weights with more than 1 dimension
        for p in model.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

        # Assign the constructed model to the instance variable
        self.model = model.to(self.DEVICE)

        # Notify the user that the model has been successfully created
        QMessageBox.information(None, "Model Created", "Transformer Model created successfully.")

    # Method to initiate training of the Transformer model using a separate thread
    def TrainModel(self):
        # Check if the model has been created; if not, notify the user and exit
        if self.model is None:
            QMessageBox.warning(None, "Model not Exist", "First create the Model.")
            return

        # Check if the training data has been prepared; if not, notify the user and exit
        if self.BatchLoader is None:
            QMessageBox.warning(None, "Data not Ready", "First Prepare the Data.")
            return

        # Initialize the optimizer using the Noam learning rate schedule with Adam optimizer
        optimizer = NoamOpt(
            model_size=256,                  # Model dimensionality
            factor=1,                        # Scaling factor for learning rate
            warmup=2000,                     # Number of warm-up steps
            optimizer=torch.optim.Adam(      # Base optimizer
                self.model.parameters(),
                lr=0,
                betas=(0.9, 0.98),
                eps=1e-9
            )
        )

        # Define the label smoothing loss function for the target vocabulary
        criterion = LabelSmoothing(
            size=len(self.fr_word_dict),     # Target vocabulary size
            padding_idx=0,                   # Index of the padding token
            smoothing=0.1                    # Smoothing factor
        )

        # Wrap the loss function and optimizer in a utility for simplified training
        loss_func = SimpleLossCompute(
            generator=self.model.generator,  # Output projection layer
            criterion=criterion,
            optimizer=optimizer
        )

        # Create a popup window to display real-time training logs
        self.DownloadLogPopup = DownloadLogPopup(
            self.log_emitter                # Pass the log emitter to stream messages to the popup
        )

        # Enable the cancel button to allow user interruption during training
        self.DownloadLogPopup.cancel_button.setEnabled(True)

        # Show the log popup window to the user
        self.DownloadLogPopup.show()

        # Log the start of the training process
        self.DownloadLogPopup.Append_Log("Training model...\nPlease wait.")

        # Create a separate thread to run the training process without freezing the UI
        self.training_thread = TrainingTransformerThread(
            self.DownloadLogPopup,          # Reference to the log popup for status updates
            self.model,                     # The Transformer model to be trained
            self.DEVICE,                    # Device (CPU or GPU) to run the training on
            optimizer,                      # Optimizer with learning rate scheduling
            loss_func,                      # Loss computation wrapper
            self.BatchLoader                # Data loader for training batches
        )

        # Connect the thread's log signal to the popup's log appending method
        self.training_thread.log_signal.connect(self.DownloadLogPopup.Append_Log)

        # Connect the cancel button to the thread's stop method to allow user to halt training
        self.DownloadLogPopup.cancel_button.clicked.connect(self.training_thread.stop)

        # Start the training thread to begin model training asynchronously
        self.training_thread.start()

    # Method to translate an English sentence into French using the trained Transformer model
    def translate(self, eng):
        # Tokenize the input English sentence into subword units
        tokenized_en = self.tokenizer.tokenize(eng)

        # Add special tokens to mark the beginning and end of the sentence
        tokenized_en = ["BOS"] + tokenized_en + ["EOS"]

        # Convert each token to its corresponding index using the English word dictionary
        enidx = [self.en_word_dict.get(i, self.UNK) for i in tokenized_en]

        # Convert the index list to a PyTorch tensor and move it to the target device
        src = torch.tensor(enidx).long().to(self.DEVICE).unsqueeze(0)  # Shape: [1, sequence_length]

        # Create a source mask to ignore padding tokens during attention
        src_mask = (src != 0).unsqueeze(-2)  # Shape: [1, 1, sequence_length]

        # Pass the source sequence through the encoder to obtain memory representations
        memory = self.model.encode(src, src_mask)

        # Initialize the target sequence with the BOS (beginning-of-sequence) token
        start_symbol = self.fr_word_dict["BOS"]
        ys = torch.ones(1, 1).fill_(start_symbol).type_as(src.data)  # Shape: [1, 1]

        # Initialize an empty list to store the predicted French tokens
        translation = []

        # Begin autoregressive decoding loop (max 100 steps)
        for i in range(100):
            # Decode the current target sequence using the encoder memory
            out = self.model.decode(
                memory,
                src_mask,
                ys,
                subsequent_mask(ys.size(1)).type_as(src.data)  # Prevent attention to future tokens
            )

            # Generate probability distribution over the target vocabulary for the last token
            prob = self.model.generator(out[:, -1])  # Shape: [1, vocab_size]

            # Select the token with the highest probability (greedy decoding)
            _, next_word = torch.max(prob, dim=1)
            next_word = next_word.data[0]

            # Append the predicted token to the target sequence
            ys = torch.cat(
                [ys, torch.ones(1, 1).type_as(src.data).fill_(next_word)],
                dim=1
            )

            # Convert the predicted index to its corresponding French token
            sym = self.fr_idx_dict[ys[0, -1].item()]

            # Stop decoding if EOS (end-of-sequence) token is generated
            if sym != 'EOS':
                translation.append(sym)
            else:
                break

        # Join the predicted tokens into a single string
        trans = "".join(translation)

        # Replace subword markers with spaces to reconstruct words
        trans = trans.replace("</w>", " ")

        # Clean up spacing around punctuation
        for x in '''?:;.,'("-!&)%''':
            trans = trans.replace(f" {x}", f"{x}")

        # Return the final translated French sentence
        return trans

    # Method to test the trained Transformer model by translating an input English sentence
    def TestModel(self, text):
        # Check if the model has been created; if not, notify the user and exit
        if self.model is None:
            QMessageBox.warning(None, "Model not Exist", "First create the Model.")
            return

        # Check if the tokenized dictionary file exists; if not, notify the user and exit
        if not os.path.exists("resources/dict.p"):
            QMessageBox.warning(None, "Dictionary not ready", "First, load and tokenize the dictionary.")
            return

        # Check if the trained model weights file exists; if not, notify the user and exit
        if not os.path.exists("resources/models/en2fr.pth"):
            QMessageBox.warning(None, "Trained Model not saved", "First, Train and Save the Model.")
            return

        # Load the tokenized dictionaries from the pickle file
        with open("resources/dict.p", "rb") as fb:
            en_word_dict, en_idx_dict, fr_word_dict, fr_idx_dict = pickle.load(fb)

        # Load the trained model weights from file and map them to the appropriate device
        trained_weights = torch.load("resources/models/en2fr.pth", map_location=self.DEVICE)

        # Load the weights into the model
        self.model.load_state_dict(trained_weights)

        # Set the model to evaluation mode (disables dropout, etc.)
        self.model.eval()

        # Translate the input English text using the trained model
        translated_fr = self.translate(text)

        # Display the original English and translated French sentences in a message box
        QMessageBox.information(
            None,
            "Translating En to Fr:",
            "English:\n" + text + "\nFrench:\n" + str(translated_fr)
        )

# Define a QThread subclass to handle model training in a separate thread
class TrainingTransformerThread(QThread):

    # Signal to emit log messages to the UI (e.g., training progress updates)
    log_signal = pyqtSignal(str)

    # Signal to trigger visualization updates (e.g., after each epoch)
    display_signal = pyqtSignal(int)

    # Constructor to initialize the training thread with model, data, and UI hooks
    def __init__(self, DownloadLogPopup, model, DEVICE, optimizer, loss_func, BatchLoader):
        # Call the parent QThread constructor
        super().__init__()

        # Reference to the popup window used for displaying logs
        self.DownloadLogPopup = DownloadLogPopup

        # The Transformer model to be trained
        self.model = model

        # Optimizer used for updating model parameters
        self.optimizer = optimizer

        # Loss function wrapper that handles loss computation and optimization
        self.loss_func = loss_func

        # Device on which training will run (e.g., 'cpu' or 'cuda')
        self.DEVICE = DEVICE

        # Data loader that yields batches of training data
        self.BatchLoader = BatchLoader

        # Flag to allow user to interrupt training manually
        self._stop_requested = False

    # Method to request stopping the training loop
    def stop(self):
        # Set the stop flag to True
        self._stop_requested = True

        # Disable the cancel button in the UI to prevent further interaction
        self.DownloadLogPopup.cancel_button.setEnabled(False)

   # Main method that runs when the training thread is started
    def run(self):
        try:
            # Emit a log message indicating the training thread has started
            self.log_signal.emit("Training thread started.")

            # Emit a log message showing how many batches are in the training loader
            self.log_signal.emit(f"Train loader has {len(self.BatchLoader)} batches.")

            # Loop over a fixed number of training epochs (e.g., 100)
            for epoch in range(100):

                # Check if a stop has been requested before starting the epoch
                if self._stop_requested:
                    break

                # Set the model to training mode (enables dropout, etc.)
                self.model.train()

                # Initialize total loss for the epoch
                tloss = 0.0

                # Initialize total token count for the epoch (used for averaging)
                tokens = 0

                # Initialize batch counter for logging
                batch_count = 0

                # Iterate over each batch in the training data loader
                for batch in self.BatchLoader:

                    # Check again if a stop has been requested mid-epoch
                    if self._stop_requested:
                        # Emit a log message indicating training was stopped
                        self.log_signal.emit("Training stopped by user.")
                        break

                    # Perform a forward pass through the model with the current batch
                    out = self.model(batch.src, batch.trg, batch.src_mask, batch.trg_mask)

                    # Compute the loss and perform a backward pass + optimizer step
                    loss = self.loss_func(out, batch.trg_y, batch.ntokens)

                    # Accumulate the total loss for this epoch
                    tloss += loss

                    # Accumulate the total number of tokens processed
                    tokens += batch.ntokens

                    # Increment the batch counter
                    batch_count += 1

                    # Every 10 batches, log the running average loss
                    if batch_count % 10 == 0:
                        # Compute running average loss (safe division)
                        running_avg = tloss / tokens if tokens > 0 else 0

                        # Emit a log message with the current running average loss
                        self.log_signal.emit(
                            f"Epoch {epoch}, Batch {batch_count}, running avg loss: {running_avg:.4f}"
                        )

                # After finishing the epoch, log the average loss (if any tokens were processed)
                if tokens > 0:
                    # Compute average loss over the epoch
                    epoch_avg = tloss / tokens

                    # Emit a log message with the epoch's average loss
                    self.log_signal.emit(f"Epoch {epoch}, average loss: {epoch_avg:.4f}")
                else:
                    # Emit a fallback message if no tokens were processed
                    self.log_signal.emit(f"Epoch {epoch}, no tokens processed.")

            # Save the trained model's parameters to disk
            torch.save(self.model.state_dict(), "resources/models/en2fr_.pth")

            # Emit a message indicating that training has completed
            self.log_signal.emit("Training Finished.")

            # Scroll the log output to the bottom to show the latest messages
            self.DownloadLogPopup.log_output.moveCursor(QTextCursor.MoveOperation.End)

            # Ensure the cursor is visible in the log output
            self.DownloadLogPopup.log_output.ensureCursorVisible()

            # Process any pending UI events to refresh the interface
            QApplication.processEvents()

        # Catch and handle any exceptions that occur during training
        except Exception as e:
            # Emit an error message with the exception details
            self.log_signal.emit(f"Error during training: {str(e)}")
   
# Custom data loader class for batching and padding tokenized sequences
class BatchLoader():
    
    # Constructor to initialize the batch loader with data and device configuration
    def __init__(self, batch_indexs, out_en_ids, out_fr_ids, DEVICE):
        self.idx = 0                          # Internal index to track current batch position
        self.batch_indexs = batch_indexs      # List of index arrays, each representing a batch
        self.out_en_ids = out_en_ids          # List of tokenized English sequences (as index lists)
        self.out_fr_ids = out_fr_ids          # List of tokenized French sequences (as index lists)
        self.DEVICE = DEVICE                  # Device to move tensors to (e.g., 'cpu' or 'cuda')

    # Make the class iterable by returning itself
    def __iter__(self):
        return self

    # Return the number of batches available
    def __len__(self):
        return len(self.batch_indexs)

    # Method to pad sequences in a batch to the same length
    def SequencePadding(self, X, padding=0):
        L = [len(x) for x in X]               # Get lengths of all sequences
        ML = max(L)                           # Find the maximum sequence length
        # Pad each sequence with the padding token to match the maximum length
        padded_seq = np.array([
            np.concatenate([x, [padding] * (ML - len(x))]) if len(x) < ML else x
            for x in X
        ])
        return padded_seq

    # Method to retrieve the next batch of data
    def __next__(self):
        self.idx += 1                         # Move to the next batch index
        if self.idx <= len(self.batch_indexs):
            b = self.batch_indexs[self.idx - 1]  # Get the indices for the current batch

            # Retrieve and pad English and French sequences for the batch
            batch_en = [self.out_en_ids[x] for x in b]
            batch_fr = [self.out_fr_ids[x] for x in b]
            batch_en = self.SequencePadding(batch_en)
            batch_fr = self.SequencePadding(batch_fr)

            # Return a Batch object containing the padded sequences and masks
            return Batch(batch_en, batch_fr, DEVICE=self.DEVICE)

        # Raise StopIteration when all batches have been processed
        raise StopIteration

# Define the Batch class to encapsulate a single training batch with masks and token counts
class Batch:
    # Constructor to initialize source and target tensors along with masks and token statistics
    def __init__(self, src, trg=None, pad=0, DEVICE="cpu"):
        # Convert the source sequence to a PyTorch tensor and move it to the specified device
        src = torch.from_numpy(src).to(DEVICE).long()

        # Store the source tensor
        self.src = src

        # Create a source mask to ignore padding tokens during attention
        self.src_mask = (src != pad).unsqueeze(-2)  # Shape: [batch_size, 1, src_len]

        # If a target sequence is provided, process it for training
        if trg is not None:
            # Convert the target sequence to a PyTorch tensor and move it to the device
            trg = torch.from_numpy(trg).to(DEVICE).long()

            # Remove the last token from each target sequence (used as input to the decoder)
            self.trg = trg[:, :-1]

            # Remove the first token from each target sequence (used as ground truth for prediction)
            self.trg_y = trg[:, 1:]

            # Create a target mask to prevent attention to future tokens and ignore padding
            self.trg_mask = make_std_mask(self.trg, pad)

            # Count the number of non-padding tokens in the target output
            self.ntokens = (self.trg_y != pad).data.sum()

# An encoder-decoder Transformer model for sequence-to-sequence tasks (e.g., machine translation)
class Transformer(nn.Module):
    # Constructor to initialize the Transformer with encoder, decoder, embeddings, and generator
    def __init__(self, encoder, decoder, src_embed, tgt_embed, generator):
        super().__init__()

        # Encoder module: processes the source sequence into contextual representations
        self.encoder = encoder

        # Decoder module: generates the target sequence using encoder output and previous tokens
        self.decoder = decoder

        # Source embedding: maps source token indices to dense vectors and applies positional encoding
        self.src_embed = src_embed

        # Target embedding: maps target token indices to dense vectors and applies positional encoding
        self.tgt_embed = tgt_embed

        # Generator: projects decoder output to vocabulary logits for prediction
        self.generator = generator

    # Method to encode the source sequence using the encoder
    def encode(self, src, src_mask):
        # Apply source embedding and pass through the encoder with source mask
        return self.encoder(self.src_embed(src), src_mask)

    # Method to decode the target sequence using the decoder and encoder memory
    def decode(self, memory, src_mask, tgt, tgt_mask):
        # Apply target embedding and pass through the decoder with memory and masks
        return self.decoder(self.tgt_embed(tgt), memory, src_mask, tgt_mask)

    # Forward method to run the full encoder-decoder pipeline
    def forward(self, src, tgt, src_mask, tgt_mask):
        # Encode the source sequence
        memory = self.encode(src, src_mask)

        # Decode the target sequence using the encoder output
        output = self.decode(memory, src_mask, tgt, tgt_mask)

        # Return the final decoder output (before projection by the generator)
        return output

# Create an encoder composed of N identical layers
class Encoder(nn.Module):
    # Constructor to initialize the encoder with a base layer and number of repetitions
    def __init__(self, layer, N):
        super().__init__()

        # Create a list of N deep-copied encoder layers (to ensure independent weights)
        self.layers = nn.ModuleList([deepcopy(layer) for i in range(N)])

        # Final layer normalization applied after all encoder layers
        self.norm = LayerNorm(layer.size)

    # Forward pass through the encoder
    def forward(self, x, mask):
        # Pass the input through each encoder layer sequentially
        for layer in self.layers:
            x = layer(x, mask)

        # Apply layer normalization to the final output
        output = self.norm(x)

        # Return the normalized encoder output (memory)
        return output

# A single layer of the Transformer encoder, consisting of self-attention and feed-forward sublayers
class EncoderLayer(nn.Module):
    # Constructor to initialize the encoder layer with attention, feed-forward, and dropout
    def __init__(self, size, self_attn, feed_forward, dropout):
        super().__init__()

        # Multi-head self-attention mechanism
        self.self_attn = self_attn

        # Position-wise feed-forward network
        self.feed_forward = feed_forward

        # Two sublayer connections: one for self-attention, one for feed-forward
        # Each sublayer includes residual connection + layer normalization + dropout
        self.sublayer = nn.ModuleList([
            deepcopy(SublayerConnection(size, dropout)) for i in range(2)
        ])

        # Dimensionality of the model (d_model)
        self.size = size

    # Forward pass through the encoder layer
    def forward(self, x, mask):
        # Apply the first sublayer: self-attention with residual connection and normalization
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))

        # Apply the second sublayer: feed-forward network with residual connection and normalization
        output = self.sublayer[1](x, self.feed_forward)

        # Return the output of the encoder layer
        return output

# Implements a residual connection followed by layer normalization and dropout
class SublayerConnection(nn.Module):
    # Constructor to initialize normalization and dropout layers
    def __init__(self, size, dropout):
        super().__init__()

        # Layer normalization applied before the sublayer
        self.norm = LayerNorm(size)

        # Dropout layer for regularization
        self.dropout = nn.Dropout(dropout)

    # Forward pass through the sublayer connection
    def forward(self, x, sublayer):
        # Apply layer normalization to the input,
        # then pass it through the sublayer (e.g., attention or feed-forward),
        # apply dropout, and add the result back to the original input (residual connection)
        output = x + self.dropout(sublayer(self.norm(x)))

        # Return the output of the residual block
        return output

# Implements Layer Normalization as described in the Transformer architecture
class LayerNorm(nn.Module):
    # Constructor to initialize learnable parameters and epsilon for numerical stability
    def __init__(self, features, eps=1e-6):
        super().__init__()

        # Learnable gain parameter (scales normalized output)
        self.a_2 = nn.Parameter(torch.ones(features))

        # Learnable bias parameter (shifts normalized output)
        self.b_2 = nn.Parameter(torch.zeros(features))

        # Small constant to prevent division by zero during normalization
        self.eps = eps

    # Forward pass for layer normalization
    def forward(self, x):
        # Compute mean across the last dimension (features) while keeping dimensions for broadcasting
        mean = x.mean(-1, keepdim=True)

        # Compute standard deviation across the last dimension
        std = x.std(-1, keepdim=True)

        # Normalize input: subtract mean and divide by standard deviation (z-score normalization)
        x_zscore = (x - mean) / torch.sqrt(std ** 2 + self.eps)

        # Scale and shift the normalized values using learnable parameters
        output = self.a_2 * x_zscore + self.b_2

        # Return the normalized and transformed output
        return output

# Transformer decoder composed of N identical layers
class Decoder(nn.Module):
    # Constructor to initialize the decoder with a base layer and number of repetitions
    def __init__(self, layer, N):
        super().__init__()

        # Create a stack of N deep-copied decoder layers
        self.layers = nn.ModuleList([deepcopy(layer) for i in range(N)])

        # Final layer normalization applied after all decoder layers
        self.norm = LayerNorm(layer.size)

    # Forward pass through the decoder
    def forward(self, x, memory, src_mask, tgt_mask):
        # Pass the input through each decoder layer sequentially
        for layer in self.layers:
            x = layer(x, memory, src_mask, tgt_mask)

        # Apply layer normalization to the final output
        output = self.norm(x)

        # Return the normalized decoder output
        return output

# A single layer of the Transformer decoder, consisting of:
# - masked self-attention
# - encoder-decoder attention
# - feed-forward network
class DecoderLayer(nn.Module):
    def __init__(self, size, self_attn, src_attn, feed_forward, dropout):
        super().__init__()

        # Dimensionality of the model (d_model)
        self.size = size

        # Masked multi-head self-attention for decoding previous tokens
        self.self_attn = self_attn

        # Cross-attention over encoder output (memory)
        self.src_attn = src_attn

        # Position-wise feed-forward network
        self.feed_forward = feed_forward

        # Three sublayer connections with residual, normalization, and dropout
        self.sublayer = nn.ModuleList([
            deepcopy(SublayerConnection(size, dropout)) for i in range(3)
        ])

    # Forward pass through the decoder layer
    def forward(self, x, memory, src_mask, tgt_mask):
        # Apply masked self-attention to the target sequence
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, tgt_mask))

        # Apply encoder-decoder attention using encoder memory
        x = self.sublayer[1](x, lambda x: self.src_attn(x, memory, memory, src_mask))

        # Apply feed-forward network
        output = self.sublayer[2](x, self.feed_forward)

        # Return the final output of the decoder layer
        return output

# Embedding layer that maps token indices to dense vectors and scales them
class Embeddings(nn.Module):
    def __init__(self, d_model, vocab):
        super().__init__()

        # Lookup table: maps each token index to a d_model-dimensional vector
        self.lut = nn.Embedding(vocab, d_model)

        # Dimensionality of the model (used for scaling)
        self.d_model = d_model

    def forward(self, x):
        # Retrieve embeddings and scale them by sqrt(d_model) for stability
        out = self.lut(x) * math.sqrt(self.d_model)
        return out

# Implements sinusoidal positional encoding for Transformer models
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout, max_len=5000, DEVICE="CPU"):
        super().__init__()

        # Dropout layer applied after adding positional encodings
        self.dropout = nn.Dropout(p=dropout)

        # Create a zero tensor to hold positional encodings: shape [max_len, d_model]
        pe = torch.zeros(max_len, d_model, device=DEVICE)

        # Create a tensor of positions [0, 1, 2, ..., max_len-1] with shape [max_len, 1]
        position = torch.arange(0., max_len, device=DEVICE).unsqueeze(1)

        # Compute the denominator term for the sinusoidal functions
        # This ensures different frequencies for each dimension
        div_term = torch.exp(torch.arange(0., d_model, 2, device=DEVICE) * -(math.log(10000.0) / d_model))

        # Compute the positional encodings for even and odd dimensions
        pe_pos = torch.mul(position, div_term)
        pe[:, 0::2] = torch.sin(pe_pos)  # Apply sine to even indices
        pe[:, 1::2] = torch.cos(pe_pos)  # Apply cosine to odd indices

        # Add a batch dimension: shape becomes [1, max_len, d_model]
        pe = pe.unsqueeze(0)

        # Register the positional encoding tensor as a buffer (not a model parameter)
        self.register_buffer('pe', pe)

    def forward(self, x):
        # Add positional encoding to the input embeddings (no gradient needed for pe)
        x = x + self.pe[:, :x.size(1)].requires_grad_(False)

        # Apply dropout for regularization
        out = self.dropout(x)

        # Return the position-enhanced embeddings
        return out

# Implements Multi-Head Attention mechanism used in Transformers
class MultiHeadedAttention(nn.Module):
    def __init__(self, h, d_model, dropout=0.1):
        super().__init__()

        # Ensure the model dimension is divisible by the number of heads
        assert d_model % h == 0

        # Dimensionality of each attention head
        self.d_k = d_model // h

        # Number of attention heads
        self.h = h

        # Four linear layers:
        # - 3 for projecting query, key, value
        # - 1 for final output projection
        self.linears = nn.ModuleList([
            deepcopy(nn.Linear(d_model, d_model)) for i in range(4)
        ])

        # Placeholder to store attention weights (for visualization/debugging)
        self.attn = None

        # Dropout layer for regularization
        self.dropout = nn.Dropout(p=dropout)

    # Scaled dot-product attention with optional masking and dropout
    def attention(self, query, key, value, mask=None, dropout=None):
        d_k = query.size(-1)

        # Compute scaled dot-product attention scores
        scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)

        # Apply mask (if provided) to prevent attention to certain positions
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        # Normalize scores to probabilities
        p_attn = nn.functional.softmax(scores, dim=-1)

        # Apply dropout to attention weights (if specified)
        if dropout is not None:
            p_attn = dropout(p_attn)

        # Compute weighted sum of values
        return torch.matmul(p_attn, value), p_attn

    # Forward pass through multi-head attention
    def forward(self, query, key, value, mask=None):
        if mask is not None:
            # Expand mask to apply across all heads
            mask = mask.unsqueeze(1)

        nbatches = query.size(0)

        # Apply linear projections and split into h heads
        query, key, value = [
            l(x).view(nbatches, -1, self.h, self.d_k).transpose(1, 2)
            for l, x in zip(self.linears, (query, key, value))
        ]

        # Apply attention on all projected vectors in parallel
        x, self.attn = self.attention(query, key, value, mask=mask, dropout=self.dropout)

        # Concatenate heads and apply final linear projection
        x = x.transpose(1, 2).contiguous().view(nbatches, -1, self.h * self.d_k)
        output = self.linears[-1](x)

        return output

# Generator module: projects model outputs to vocabulary logits and applies log softmax
class Generator(nn.Module):
    def __init__(self, d_model, vocab):
        super().__init__()

        # Linear layer to map from model's hidden dimension to vocabulary size
        self.proj = nn.Linear(d_model, vocab)

    def forward(self, x):
        # Apply the linear projection to get raw logits over the vocabulary
        out = self.proj(x)

        # Apply log softmax to obtain log-probabilities for each token
        probs = nn.functional.log_softmax(out, dim=-1)

        return probs

# Implements the position-wise feed-forward network used in each Transformer layer
class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # Apply first linear transformation followed by ReLU activation
        h1 = F.relu(self.w_1(x))

        # Apply dropout to the activated output
        h2 = self.dropout(h1)

        # Apply second linear transformation
        return self.w_2(h2)

# Implements label smoothing to regularize the model and prevent overconfidence
class LabelSmoothing(nn.Module):
    def __init__(self, size, padding_idx, smoothing=0.1):
        super().__init__()

        # KL divergence loss is used to compare predicted log-probabilities with smoothed targets
        self.criterion = nn.KLDivLoss(reduction='sum')

        # Index of the padding token (to be ignored in loss computation)
        self.padding_idx = padding_idx

        # Confidence assigned to the correct class (1 - smoothing)
        self.confidence = 1.0 - smoothing

        # Smoothing factor: how much probability mass to distribute to incorrect classes
        self.smoothing = smoothing

        # Vocabulary size (number of classes)
        self.size = size

        # For debugging or visualization: stores the smoothed target distribution
        self.true_dist = None

    def forward(self, x, target):
        # Ensure the prediction dimension matches the vocabulary size
        assert x.size(1) == self.size

        # Clone the input tensor to build the smoothed target distribution
        true_dist = x.data.clone()

        # Fill all entries with the smoothing value for incorrect classes
        true_dist.fill_(self.smoothing / (self.size - 2))

        # Assign the confidence value to the correct class index
        true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)

        # Zero out the probability for the padding index
        true_dist[:, self.padding_idx] = 0

        # Identify positions where the target is padding
        mask = torch.nonzero(target.data == self.padding_idx)

        # If any padding tokens are found, zero out their entire row in the target distribution
        if mask.dim() > 0:
            true_dist.index_fill_(0, mask.squeeze(), 0.0)

        # Store the smoothed distribution for inspection
        self.true_dist = true_dist

        # Compute the KL divergence loss between predicted log-probs and smoothed targets
        output = self.criterion(x, true_dist.clone().detach())

        return output

# Utility class to compute loss and perform backpropagation and optimization
class SimpleLossCompute:
    def __init__(self, generator, criterion, optimizer=None):
        # generator: the model's output projection layer (e.g., Generator)
        self.generator = generator

        # criterion: loss function (e.g., LabelSmoothing or nn.NLLLoss)
        self.criterion = criterion

        # optional optimizer (e.g., from torch.optim)
        self.optimizer = optimizer

    # Callable interface to compute loss and optionally update model parameters
    def __call__(self, x, y, norm):
        # Apply the generator to get log-probabilities over the vocabulary
        x = self.generator(x)

        # Flatten predictions and targets for loss computation
        # x: [batch_size * seq_len, vocab_size]
        # y: [batch_size * seq_len]
        loss = self.criterion(
            x.contiguous().view(-1, x.size(-1)),
            y.contiguous().view(-1)
        ) / norm  # Normalize loss (e.g., by number of non-padding tokens)

        # Backpropagate the loss
        loss.backward()

        # If an optimizer is provided, perform a step and reset gradients
        if self.optimizer is not None:
            self.optimizer.step()
            # Try to zero gradients from the wrapped optimizer if it exists
            if hasattr(self.optimizer, 'optimizer'):
                self.optimizer.optimizer.zero_grad()
            else:
                self.optimizer.zero_grad()

        # Return the scaled loss value (for logging or tracking)
        return loss.data.item() * norm.float()

# Implements the Noam learning rate schedule from "Attention is All You Need"
class NoamOpt:
    def __init__(self, model_size, factor, warmup, optimizer):
        # Wrapped optimizer (e.g., Adam)
        self.optimizer = optimizer

        # Internal step counter
        self._step = 0

        # Number of warmup steps before decay begins
        self.warmup = warmup

        # Scaling factor for the learning rate
        self.factor = factor

        # Model dimensionality (d_model), used in the learning rate formula
        self.model_size = model_size

        # Current learning rate (for logging or inspection)
        self._rate = 0

    # Perform an optimization step with updated learning rate
    def step(self):
        # Increment the step counter
        self._step += 1

        # Compute the new learning rate
        rate = self.rate()

        # Update the learning rate for all parameter groups in the optimizer
        for p in self.optimizer.param_groups:
            p['lr'] = rate

        # Store the current rate
        self._rate = rate

        # Perform the optimizer step (i.e., update parameters)
        self.optimizer.step()

    # Compute the learning rate at a given step using the Noam schedule
    def rate(self, step=None):
        if step is None:
            step = self._step

        # Formula: factor * (model_size^-0.5) * min(step^-0.5, step * warmup^-1.5)
        output = self.factor * (
            self.model_size ** (-0.5) *
            min(step ** (-0.5), step * self.warmup ** (-1.5))
        )
        return output

# Creates a mask to hide future tokens in a sequence (used in decoder self-attention)
def subsequent_mask(size):
    # Shape: [1, size, size] — for broadcasting across batches and heads
    attn_shape = (1, size, size)

    # Create an upper-triangular matrix filled with 1s above the main diagonal
    # This masks out future positions (i.e., tokens the model shouldn't attend to yet)
    subsequent_mask = np.triu(np.ones(attn_shape), k=1).astype('uint8')

    # Convert to a PyTorch boolean tensor: True where attention is allowed, False where it's masked
    output = torch.from_numpy(subsequent_mask) == 0

    return output

# Creates a standard mask for the target sequence:
# - Masks out padding tokens
# - Prevents attention to future tokens (causal masking)
def make_std_mask(tgt, pad):
    # Create a padding mask: True where tgt is not equal to pad
    # Shape: [batch_size, 1, seq_len]
    tgt_mask = (tgt != pad).unsqueeze(-2)

    # Create a subsequent mask to block future positions
    # Shape: [1, seq_len, seq_len]
    # Convert it to the same type as tgt_mask for compatibility
    output = tgt_mask & subsequent_mask(tgt.size(-1)).type_as(tgt_mask.data)

    # Return the combined mask: True where attention is allowed
    return output