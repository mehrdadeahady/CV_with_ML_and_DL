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

# This class manages the setup and execution of text generation using a GPT-2 XL Transformer.
# It combines PyTorch for model operations and PyQt's QObject for signal-slot integration.
# The class initializes tokenizers, model configurations, and placeholders for attention mechanism components.
class GeneratingTextByGPT2xlTransformer(QObject):

    # Constructor method: initializes the transformer, tokenizer, model config, and placeholders.
    # Also sets a fixed seed for reproducibility and prepares components for attention computation.
    def __init__(self, parent=None):
        """
        Initialize the GeneratingTextByGPT2xlTransformer instance.

        Parameters:
        parent (QObject, optional): Optional parent object for Qt signal-slot hierarchy.
        """
        # Initialize the base QObject to enable signal-slot communication
        super().__init__()

        # Set a fixed seed for PyTorch to ensure reproducible results across runs
        torch.manual_seed(0)

        # Instantiate the Byte Pair Encoding tokenizer for input text processing
        self.tokenizer = BPETokenizer()

        # Placeholder for the generated response text
        self.response = None

        # Initialize attention mechanism components (query, key, value tensors)
        self.q = None  # Query tensor used in attention
        self.k = None  # Key tensor used in attention
        self.v = None  # Value tensor used in attention

        # Initialize dimensions used in attention calculations
        self.B = None  # Batch size
        self.T = None  # Sequence length (time steps)
        self.C = None  # Embedding dimension (channels)

        # Intermediate tensors for attention score computation
        self.scaled_att = None           # Scaled dot-product attention scores
        self.masked_scaled_att = None    # Masked attention scores for causal masking
        self.att = None                  # Final attention output tensor

        # Load model configuration settings (e.g., layer sizes, dropout rates)
        self.config = Config()

        # Placeholders for model and tokenizer instances
        self.model = None           # Custom GPT-2 XL model instance
        self.model_hf = None        # Hugging Face GPT-2 XL model instance
        self.tokenizer_hf = None    # Hugging Face tokenizer for input/output formatting
        self.sd_hf = None           # State dictionary from Hugging Face model (for weight transfer)

        # Flag indicating whether weights have been transferred from Hugging Face model
        self.WeightsTransfered = False

    # Demonstrates how to project an input tensor into query (Q), key (K), and value (V) vectors
    # using a linear transformation. Also displays the resulting tensor shapes in a message box.
    def demonstrate_qkv_projection(self):
        """
        Projects a sample input tensor into Q, K, and V vectors using a linear layer.
        Stores the resulting tensors and their dimensions as instance variables.
        Displays the shapes of Q, K, and V using a message box.
        """

        # Generate a random input tensor with shape:
        # batch size = 1, sequence length = 4, embedding dimension = 1600
        x = torch.randn((1, 4, 1600))

        # Create a linear layer that maps the input from 1600 to 3 × 1600 dimensions
        # This will be split into Q, K, and V vectors
        c_attn = nn.Linear(1600, 1600 * 3)

        # Extract the input tensor's dimensions:
        # B = batch size, T = sequence length, C = embedding dimension
        B, T, C = x.size()

        # Apply the linear layer to the input tensor
        # Then split the output into three equal parts along the last dimension
        # Each part corresponds to Q (query), K (key), and V (value)
        q, k, v = c_attn(x).split(1600, dim=2)

        # Store the resulting tensors and dimensions as instance variables
        self.q = q
        self.k = k
        self.v = v
        self.B = B
        self.T = T
        self.C = C

        # Format a message string showing the shapes of Q, K, and V tensors
        result = (
            "QKV Projection Results:\n"
            f"• Q shape: {q.size()}\n"
            f"• K shape: {k.size()}\n"
            f"• V shape: {v.size()}"
        )

        # Display the tensor shapes in an informational message box
        QMessageBox.information(
            None,
            "QKV Projection Demonstration",
            result
        )

    # Reshapes the Q, K, and V tensors into multiple attention heads and displays their new shapes.
    # This is a common step in multi-head self-attention to allow parallel attention computations.
    def reshape_into_heads_and_print(self):
        """
        Reshapes the stored Q, K, and V tensors into multi-head format.
        Each tensor is reshaped to (B, 25, T, hs), where 25 is the number of attention heads
        and hs is the hidden size per head. Displays the new shapes in a message box.
        """

        # Check if required tensors and dimensions are initialized
        if self.q is None or self.k is None or self.v is None or \
           self.B is None or self.T is None or self.C is None:
            # Show warning if tensors are not ready
            QMessageBox.warning(None, "Missing Tensors", "Please run the QKV projection step first.")
            return

        # Retrieve stored tensors and dimensions
        q = self.q
        k = self.k
        v = self.v
        B = self.B
        T = self.T
        C = self.C

        # Define the number of attention heads
        num_heads = 25

        # Compute the hidden size per head
        hs = C // num_heads

        # Reshape and transpose the key tensor to shape (B, num_heads, T, hs)
        k = k.view(B, T, num_heads, hs).transpose(1, 2)

        # Reshape and transpose the query tensor to shape (B, num_heads, T, hs)
        q = q.view(B, T, num_heads, hs).transpose(1, 2)

        # Reshape and transpose the value tensor to shape (B, num_heads, T, hs)
        v = v.view(B, T, num_heads, hs).transpose(1, 2)

        # Format the result message with the new tensor shapes
        result = (
            "Multi-Head Attention Reshape Results:\n"
            f"• Q shape: {q.size()}\n"
            f"• K shape: {k.size()}\n"
            f"• V shape: {v.size()}"
        )

        # Display the reshaped tensor shapes in an informational message box
        QMessageBox.information(None, "QKV Multi-Head Shapes", result)

    # Computes scaled dot-product attention scores between query and key tensors.
    # Displays the attention matrices for the first and second heads in the first batch.
    def compute_scaled_dot_product_attention(self):
        """
        Computes the scaled dot-product attention scores using the stored Q and K tensors.
        The attention scores are calculated as Q × Kᵀ / √d_k, where d_k is the key dimension.
        The result is stored and a preview of the attention matrices is shown in a message box.
        """

        # Ensure that all required tensors and dimensions are initialized
        if self.q is None or self.k is None or self.v is None or \
           self.B is None or self.T is None or self.C is None:
            # Show warning if tensors are not ready
            QMessageBox.warning(None, "Missing Tensors", "Please run the QKV projection step first.")
            return

        # Retrieve stored tensors and dimensions
        q = self.q
        k = self.k
        v = self.v
        B = self.B
        T = self.T
        C = self.C

        # Compute scaled dot-product attention:
        # Multiply Q by the transpose of K, then scale by 1 / sqrt(d_k)
        scaled_att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))

        # Store the computed attention scores
        self.scaled_att = scaled_att

        # Format a message showing attention scores for the first and second heads in the first batch
        result = (
            "Scaled Dot-Product Attention Scores:\n"
            f"• Head 1 (Batch 0):\n{scaled_att[0, 0]}\n\n"
            f"• Head 2 (Batch 0):\n{scaled_att[0, 1]}"
        )

        # Display the attention matrices in an informational message box
        QMessageBox.information(None, "Scaled Attention Scores", result)

    # Applies a causal mask to the scaled attention scores to prevent attention to future tokens.
    # Displays the masked attention matrix for the first head in the first batch.
    def apply_causal_mask_and_print(self):
        """
        Applies a causal (lower triangular) mask to the scaled attention scores.
        This ensures that each token can only attend to itself and previous tokens.
        Displays the masked attention matrix and the mask used.
        """

        # Check if scaled attention scores are available
        if self.scaled_att is None:
            # Show warning if attention scores haven't been computed yet
            QMessageBox.warning(None, "Computation Not Ready", "Please compute scaled attention scores first.")
            return

        # Retrieve the previously computed scaled attention tensor
        scaled_att = self.scaled_att

        # Create a 4x4 lower triangular matrix to serve as the causal mask
        # This allows each token to attend only to itself and previous tokens
        mask = torch.tril(torch.ones(4, 4))

        # Apply the causal mask:
        # Positions where mask == 0 are filled with -inf to block attention
        masked_scaled_att = scaled_att.masked_fill(mask == 0, float('-inf'))

        # Store the masked attention scores
        self.masked_scaled_att = masked_scaled_att

        # Format the result message showing masked scores and the mask matrix
        result = (
            "Masked Attention Scores (Head 1, Batch 0):\n"
            f"{masked_scaled_att[0, 0]}\n\n"
            "Causal Mask Matrix (1 = allowed, 0 = blocked):\n"
            f"{mask}"
        )

        # Display the masked attention scores and mask in a message box
        QMessageBox.information(None, "Causal Mask Applied", result)

    # Applies the softmax function to the masked attention scores to obtain attention weights.
    # Displays the attention weights for the first and last heads in the first batch.
    def apply_softmax_and_print(self):
        """
        Applies the softmax function to the masked attention scores to produce attention weights.
        This converts raw scores into probabilities that sum to 1 across each row.
        Displays the attention weights for the first and last attention heads in the first batch.
        """

        # Ensure that masked attention scores are available
        if self.masked_scaled_att is None:
            # Show warning if the causal mask hasn't been applied yet
            QMessageBox.warning(
                None,
                "Causal Mask Not Applied",
                "Please apply the causal mask to the scaled attention scores first."
            )
            return

        # Retrieve the masked attention scores
        masked_scaled_att = self.masked_scaled_att

        # Apply softmax along the last dimension to convert scores into attention probabilities
        att = F.softmax(masked_scaled_att, dim=-1)

        # Store the resulting attention weights
        self.att = att

        # Format the result message showing attention weights for selected heads
        result = (
            "Attention Weights (Softmax Output):\n"
            f"• Head 1 (Batch 0):\n{att[0, 0]}\n\n"
            f"• Last Head (Batch 0):\n{att[0, -1]}"
        )

        # Display the attention weights in an informational message box
        QMessageBox.information(None, "Attention Weights", result)

    # Applies attention weights to the value tensor to compute the final context vectors.
    # Reshapes the result back to the original input shape and displays its dimensions.
    def apply_attention_and_reshape(self):
        """
        Computes the final output of the attention mechanism by applying attention weights to the value tensor.
        The result is reshaped from multi-head format back to the original input shape (B, T, C).
        Displays the final tensor shape in a message box.
        """

        # Check if all required tensors and attention weights are available
        if self.q is None or self.k is None or self.v is None or \
           self.B is None or self.T is None or self.C is None or self.att is None:
            # Show warning if prerequisites are missing
            QMessageBox.warning(
                None,
                "Missing Data",
                "Please ensure QKV tensors are initialized and softmax has been applied."
            )
            return

        # Retrieve stored tensors and dimensions
        q = self.q
        k = self.k
        v = self.v
        B = self.B
        T = self.T
        C = self.C
        att = self.att

        # Apply attention weights to the value tensor to compute context vectors
        y = att @ v  # Shape: (B, num_heads, T, hs)

        # Transpose to move the head dimension after sequence length
        # Resulting shape: (B, T, num_heads, hs)
        y = y.transpose(1, 2)

        # Ensure the tensor is contiguous in memory before reshaping
        y = y.contiguous()

        # Reshape from (B, T, num_heads, hs) back to (B, T, C)
        # by merging the last two dimensions
        y = y.view(B, T, C)

        # Format the result message showing the final output shape
        result = f"Final output tensor shape: {y.shape}"

        # Display the final tensor shape in an informational message box
        QMessageBox.information(None, "Attention Output Shape", result)

    # Demonstrates how to tokenize a sample text using a Byte Pair Encoding (BPE) tokenizer.
    # Displays the resulting tokens and their corresponding BPE indices.
    def demonstrate_bpe_tokenization(self):
        """
        Uses a Byte Pair Encoding (BPE) tokenizer to tokenize a sample input string.
        Shows both the final tokens and their corresponding BPE indices in a message box.
        """

        # Define the input text to be tokenized
        example = "This is the original text."

        # Initialize the BPE encoder (e.g., GPT-2's tokenizer)
        bpe_encoder = get_encoder()

        # Encode the input text and retrieve tokenization details
        # The response includes both the token strings and their BPE indices
        response = bpe_encoder.encode_and_show_work(example)

        # Store the response for potential later use
        self.response = response

        # Format the result message with tokenization output
        result = (
            "BPE Tokenization Example:\n"
            f"• Input Text:\n{example}\n\n"
            f"• Tokens:\n{response['tokens']}\n\n"
            f"• BPE Indices:\n{response['bpe_idx']}"
        )

        # Display the tokenization results in an informational message box
        QMessageBox.information(None, "BPE Tokenization Result", result)

    # Decodes a list of BPE token indices back into human-readable text using the BPETokenizer.
    # Displays the decoded output in a message box.
    def decode_bpe_indices(self):
        """
        Converts the stored list of BPE token indices back into the original text.
        Uses the BPETokenizer's decode method and displays the result.
        """

        # Check if tokenization has been performed and response is available
        if self.response is None:
            # Show warning if BPE token indices are not ready
            QMessageBox.warning(None, "Tokenization Required", "Please tokenize the input text using BPE first.")
            return

        # Convert BPE indices to a PyTorch LongTensor and decode them back to text
        out = self.tokenizer.decode(torch.LongTensor(self.response['bpe_idx']))

        # Format the result message with the decoded text
        result = f"Decoded Text:\n{out}"

        # Display the decoded output in an informational message box
        QMessageBox.information(None, "BPE Decoding Result", result)

    # Tokenizes a phrase using Byte Pair Encoding (BPE), maps tokens to indices,
    # and decodes them back into the original text. Displays all steps in a message box.
    def tokenize_and_decode_bpe(self):
        """
        Demonstrates the full BPE tokenization and decoding cycle:
        1. Tokenizes a sample phrase using a BPE encoder.
        2. Maps the tokens to their corresponding BPE indices.
        3. Decodes the indices back into the original text.
        Displays all intermediate and final results in a message box.
        """

        # Define the input phrase to be tokenized
        example = "this is a prompt"

        # Initialize the BPE encoder (e.g., GPT-2's tokenizer)
        bpe_encoder = get_encoder()

        # Encode the phrase and retrieve tokenization details
        # Includes both token strings and their BPE indices
        response = bpe_encoder.encode_and_show_work(example)

        # Decode the BPE indices back into the original phrase
        out = self.tokenizer.decode(torch.LongTensor(response['bpe_idx']))

        # Format the result message with tokenization and decoding output
        result = (
            "BPE Tokenization and Decoding:\n"
            f"• Input Text:\n{example}\n\n"
            f"• Tokens:\n{response['tokens']}\n\n"
            f"• BPE Indices:\n{response['bpe_idx']}\n\n"
            f"• Decoded Text:\n{out}"
        )

        # Display the full tokenization and decoding process in a message box
        QMessageBox.information(None, "BPE Tokenization & Decoding", result)

    # Plots and compares the ReLU and GELU activation functions over a range of input values.
    # Useful for visualizing the differences in behavior between these two nonlinearities.
    def plot_relu_vs_gelu(self):
        """
        Defines and compares the ReLU and GELU activation functions by plotting them
        over a range of input values. ReLU is defined manually, while GELU uses a standard implementation.
        The plot highlights how GELU smooths transitions compared to ReLU's sharp cutoff.
        """

        # Instantiate the GELU activation function
        genu = GELU()

        # Define the ReLU activation function manually
        def relu(x):
            # Initialize output tensor with zeros
            y = torch.zeros(len(x))
            # Apply ReLU: set y[i] = x[i] if x[i] > 0
            for i in range(len(x)):
                if x[i] > 0:
                    y[i] = x[i]
            return y

        # Generate 300 input values evenly spaced between -6 and 6
        xs = torch.linspace(-6, 6, 300)

        # Apply ReLU to the input values
        ys = relu(xs)

        # Apply GELU to the input values
        gs = genu(xs)

        # Create a plot to compare ReLU and GELU
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        # Set x and y axis limits for better visualization
        plt.xlim(-3, 3)
        plt.ylim(-0.5, 3.5)

        # Plot ReLU in solid blue
        plt.plot(xs, ys, color='blue', label="ReLU")

        # Plot GELU in dashed red
        plt.plot(xs, gs, "--", color='red', label="GELU")

        # Add legend and axis labels
        plt.legend(fontsize=12)
        plt.xlabel("Input values (x)")
        plt.ylabel("Activation output")

        # Add a descriptive title
        plt.title("Comparison of ReLU and GELU Activation Functions")

        # Display the plot
        plt.show()

    # Creates an instance of the GPT-2 XL model using the current configuration.
    # Displays progress and model summary, including total parameter count.
    def CreateGPT2xlModel(self):
        """
        Instantiates the GPT-2 XL model using the provided configuration.
        If a model already exists, it prevents re-creation and notifies the user.
        Displays a message while initializing and shows the model summary upon completion.
        """

        # Check if the model has already been created
        if self.model is not None:
            # Warn the user that the model already exists
            QMessageBox.warning(None, "Model Already Exists", "A GPT-2 XL model has already been created.")
            return

        # Inform the user that model creation is starting and may take time
        QMessageBox.information(
            None,
            "Creating Model...",
            "Initializing the GPT-2 XL model.\n\nThis may take up to a minute.\nPlease close this window and wait..."
        )

        # Instantiate the GPT-2 XL model using the current configuration
        self.model = GPT2XL(self.config)

        # Calculate the total number of parameters in the model
        num = sum(p.numel() for p in self.model.transformer.parameters())

        # Display a scrollable message with the model summary and parameter count
        show_scrollable_message(
            "Model Created Successfully",
            f"Total Parameters in the Model: {num / 1e6:.2f} million\n\nModel Architecture:\n{self.model}"
        )

    # Warns the user that training GPT-2 XL from scratch is resource-intensive and time-consuming.
    # Recommends using pre-trained weights instead.
    def TrainModel(self):
        """
        Displays a warning that training GPT-2 XL requires specialized hardware and is computationally expensive.
        Suggests downloading and using pre-trained weights instead of training from scratch.
        """

        # Show a warning message discouraging training due to high resource requirements
        QMessageBox.warning(
            None,
            "Attention",
            "Training GPT-2 XL requires specialized hardware and is extremely time-consuming.\n\n"
            "It is strongly recommended to download and use pre-trained weights instead."
        )

    # Downloads and loads GPT-2 XL weights from Hugging Face if available locally.
    # If weights are missing, provides instructions for manual download.
    def DownloadLoadGPT2XLWeights(self):
        """
        Loads GPT-2 XL model weights and tokenizer from Hugging Face if they exist locally.
        If the model is already loaded, warns the user.
        If the required files are missing, provides instructions for downloading them manually.
        """

        # Check if the Hugging Face model is already loaded
        if self.model_hf is not None:
            QMessageBox.warning(None, "Model Already Loaded", "The Hugging Face GPT-2 XL model is already loaded.")
            return

        # Internal function to load weights and tokenizer from Hugging Face
        def LoadWeights():
            self.model_hf = GPT2LMHeadModel.from_pretrained("gpt2xl")
            self.tokenizer_hf = GPT2Tokenizer.from_pretrained("gpt2xl")
            self.sd_hf = self.model_hf.state_dict()
            show_scrollable_message(
                "Weights Loaded Successfully",
                f"Hugging Face GPT-2 XL Model:\n\n{self.model_hf}"
            )

        # Check if all required files exist in the local 'gpt2xl' folder
        if (
            os.path.exists("gpt2xl") and
            os.path.exists("gpt2xl/config.json") and
            os.path.exists("gpt2xl/link.txt") and
            os.path.exists("gpt2xl/merges.txt") and
            os.path.exists("gpt2xl/pytorch_model.bin") and
            os.path.exists("gpt2xl/tokenizer_config.json") and
            os.path.exists("gpt2xl/vocab.json")
        ):
            QMessageBox.information(
                None,
                "Loading Model...",
                "Loading the GPT-2 XL model.\n\nThis may take up to 2 minutes.\nPlease close this window and wait..."
            )
            LoadWeights()
            return

        # Show instructions for downloading the required files manually
        QMessageBox.warning(
            None,
            "Download Required",
            "GPT-2 XL weights are not found locally.\n\n"
            "To download them directly in code:\n"
            "  from transformers import GPT2LMHeadModel\n"
            "  model_hf = GPT2LMHeadModel.from_pretrained('gpt2-xl')\n"
            "  sd_hf = model_hf.state_dict()\n\n"
            "Or download manually from Hugging Face:\n"
            "  https://huggingface.co/openai-community/gpt2-xl/tree/main\n\n"
            "Steps:\n"
            "1. Create a folder named 'gpt2xl' in your project root.\n"
            "2. Download the following files into that folder:\n"
            "   • config.json\n"
            "   • link.txt\n"
            "   • merges.txt\n"
            "   • pytorch_model.bin\n"
            "   • tokenizer_config.json\n"
            "   • vocab.json\n\n"
            "Once downloaded, rerun this function to load the weights."
        )

    # Transfers weights from a pretrained Hugging Face GPT-2 XL model to a custom GPT2XL model.
    # Handles transpositions for Conv1D-style layers and displays key tensor shapes before transfer.
    def transfer_gpt2xl_weights(self):
        """
        Transfers pretrained weights from a Hugging Face GPT-2 XL model to a custom GPT2XL model.
        Displays the shape of a key tensor before transfer and handles necessary transpositions
        for Conv1D-style layers. Skips unnecessary keys like 'attn.masked_bias'.
        """

        # Ensure that both models and the Hugging Face state dictionary are available
        if self.model_hf is None or self.model is None or self.sd_hf is None:
            QMessageBox.warning(
                None,
                "Models and Weights Not Ready",
                "Please create the custom model and load the Hugging Face weights first."
            )
            return

        # Display the shape of a key tensor before weight transfer for verification
        QMessageBox.information(
            None,
            "Inspecting Tensor Shapes",
            "Shape of 'c_fc' weight in Hugging Face model:\n"
            f"{self.model_hf.transformer.h[0].mlp.c_fc.weight.shape}\n\n"
            "Shape of corresponding tensor in custom GPT2XL model:\n"
            f"{self.model.transformer.h[0].mlp.c_fc.weight.shape}\n\n"
            "Transferring weights...\nThis may take up to 3 minutes.\nPlease close this window and wait."
        )

        # Filter out keys that are not needed for weight transfer
        keys = [k for k in self.sd_hf if not k.endswith('attn.masked_bias')]

        # Get the state dictionary of the custom model
        sd = self.model.state_dict()

        # List of weight keys that require transposition due to layout differences
        transposed = [
            'attn.c_attn.weight',
            'attn.c_proj.weight',
            'mlp.c_fc.weight',
            'mlp.c_proj.weight'
        ]

        # Iterate over all relevant keys and copy weights into the custom model
        for k in keys:
            if any(k.endswith(w) for w in transposed):
                # Transpose weights for Conv1D-style layers before copying
                with torch.no_grad():
                    sd[k].copy_(self.sd_hf[k].t())
            else:
                # Directly copy weights for all other layers
                with torch.no_grad():
                    sd[k].copy_(self.sd_hf[k])

        # Mark that weights have been successfully transferred
        self.WeightsTransfered = True

        # Notify the user of successful transfer
        QMessageBox.information(None, "Weights Transferred", "Weights have been transferred successfully.")

    # Autoregressively generates tokens from the model using temperature and top-k sampling.
    def sample(self, idx, max_new_tokens, temperature=1.0, top_k=None):
        # Loop to generate one token at a time.
        for _ in range(max_new_tokens):

            # Trim input to model's block size if needed.
            if idx.size(1) <= self.config.block_size:
                idx_cond = idx
            else:
                idx_cond = idx[:, -self.config.block_size:]

            # Get logits from the model.
            logits, _ = self.model(idx_cond)

            # Select logits for the last token and apply temperature scaling.
            logits = logits[:, -1, :] / temperature

            # Apply top-k filtering if specified.
            if top_k is not None:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = -float('Inf')

            # Convert logits to probabilities.
            probs = F.softmax(logits, dim=-1)

            # Sample next token from the distribution.
            idx_next = torch.multinomial(probs, num_samples=1)

            # Stop if end-of-text token is generated.
            if idx_next.item() == self.tokenizer.encoder.encoder['<|endoftext|>']:
                break

            # Append new token to the sequence.
            idx = torch.cat((idx, idx_next), dim=1)

        # Return the full generated sequence.
        return idx

    # Generates text from a given prompt using the GPT-2 XL model and displays the result.
    # Supports temperature and top-k sampling for controlled generation.
    def generate(self, prompt, max_new_tokens, temperature=1.0, top_k=None):
        """
        Generates text based on a user-provided prompt using the GPT-2 XL model.
        Applies temperature and optional top-k sampling to control randomness.
        Displays the prompt, generation settings, and the generated text in a message box.

        Parameters:
        prompt (str): The input text to begin generation from.
        max_new_tokens (int): Number of tokens to generate.
        temperature (float): Sampling temperature; higher = more random.
        top_k (int, optional): If set, restricts sampling to top-k most probable tokens.
        """

        # If the prompt is empty, start with the end-of-text token
        if prompt == '':
            x = torch.tensor([[self.tokenizer.encoder.encoder['<|endoftext|>']]], dtype=torch.long)
        else:
            # Tokenize the input prompt
            x = self.tokenizer(prompt)

        # Generate new tokens using the sampling method
        y = self.sample(x, max_new_tokens, temperature, top_k)

        # Decode the generated token sequence into text
        out = self.tokenizer.decode(y.squeeze())

        # Format the result message with prompt, settings, and generated text
        result = (
            "Prompt and Generated Text:\n\n"
            f"Prompt:\n{prompt}\n\n"
            f"Settings:\n"
            f"• max_new_tokens: {max_new_tokens}\n"
            f"• temperature: {temperature}\n"
            f"• top_k: {top_k}\n\n"
            f"Generated Text:\n{out}"
        )

        # Display the result in an informational message box
        QMessageBox.information(None, "Text Generation Result", result)

    '''
    the differences between these generate calls by focusing on how the prompt, temperature, top_k, and random seed affect the output of the sample and generate functions.

    🔍 Key Parameters That Influence Output
    | Parameter | Description | 
    | prompt | The initial text given to the model to condition its generation. An empty prompt means the model starts from scratch. | 
    | temperature | Controls randomness. Lower values (e.g. 0.7) make the model more confident and deterministic; higher values (e.g. 1.2) make it more creative and diverse. | 
    | top_k | Limits sampling to the top-k most probable tokens. Lower values make the output more focused and conservative. | 
    | torch.manual_seed() | Sets the random seed for reproducibility. Same seed = same output (if other parameters are the same). | 

    🧪 Breakdown of Each Code Block
    1. Empty Prompt, Temperature = 1.0, No Top-k
    prompt = ""
    torch.manual_seed(42)
    generate(prompt, max_new_tokens=100, temperature=1.0, top_k=None)

    - Unconstrained generation from scratch.
    - Temperature = 1.0 allows moderate randomness.
    - No top-k means sampling from the full distribution.
    - Seed = 42 ensures reproducibility.
    2. Empty Prompt, Temperature = 0.9, Top-k = 40
    prompt = ""
    torch.manual_seed(42)
    generate(prompt, max_new_tokens=100, temperature=0.9, top_k=40)

    - Still generating from scratch.
    - Lower temperature and top_k = 40 make the output more focused and less surprising.
    - Same seed, but different sampling constraints → different output from #1.
    3. Prompted Generation with Varying Seeds
    prompt = "I went to the kitchen and"
    for i in range(5):
        torch.manual_seed(i)
        generate(prompt, max_new_tokens=10, temperature=1.0, top_k=None)

    - Fixed prompt provides context.
    - Temperature = 1.0, no top-k → open-ended generation.
    - Different seeds (0-4) produce different continuations of the same prompt.
    - Great for exploring diversity in model responses.
    4. Factual Prompt, Temperature = 1.0, No Top-k
    prompt = "Lexington is the second largest city in the state of Kentucky"
    torch.manual_seed(42)
    generate(prompt, max_new_tokens=100, temperature=1.0, top_k=None)

    - Prompt is factual and specific.
    - Temperature = 1.0 allows some creativity, but the model may stay on-topic.
    - No top-k → full vocabulary sampling.
    5. Same Prompt, Lower Temperature and Top-k
    prompt = "Lexington is the second largest city in the state of Kentucky"
    torch.manual_seed(42)
    generate(prompt, max_new_tokens=100, temperature=0.9, top_k=50)

    - Same prompt as #4.
    - Lower temperature and top-k make the output more focused and factual.
    - Should yield a more coherent and less surprising continuation.
    6. Same Prompt, Higher Temperature
    torch.manual_seed(42)
    generate(prompt, max_new_tokens=100, temperature=1.2, top_k=None)

    - Higher temperature = more randomness.
    - Expect more creative or erratic output, possibly drifting off-topic.
    - Useful for brainstorming or generating unexpected ideas.

    🧠 Summary of Differences
    | Scenario | Prompt | Temperature | Top-k | Seed | Expected Behavior | 
    | 1 | "" | 1.0 | None | 42 | Creative, open-ended text | 
    | 2 | "" | 0.9 | 40 | 42 | More focused, less random | 
    | 3 | "I went to the kitchen and" | 1.0 | None | 0-4 | Diverse completions of same prompt | 
    | 4 | "Lexington..." | 1.0 | None | 42 | Creative but grounded in prompt | 
    | 5 | "Lexington..." | 0.9 | 50 | 42 | More factual and constrained | 
    | 6 | "Lexington..." | 1.2 | None | 42 | More surprising or imaginative output | 

    Each variation gives you a different flavor of generation—ranging from deterministic and focused to wild and exploratory. 
    '''

    # Handles text generation based on which UI button was clicked.
    # Ensures model and weights are ready, then generates text using predefined settings.
    def GenerateTextByModel(self):
        """
        Generates text using the custom GPT-2 XL model based on the sender button's configuration.
        Ensures that the model, Hugging Face weights, and weight transfer are complete before proceeding.
        Displays a warning about generation time and invokes the appropriate generation settings.
        """

        # Ensure model and weights are ready before generating text
        if self.model is None or self.model_hf is None or not self.WeightsTransfered:
            QMessageBox.warning(
                None,
                "Models and Weights Not Ready",
                "Please ensure the following steps are completed:\n"
                "1. Create the custom model\n"
                "2. Download and load Hugging Face weights\n"
                "3. Transfer weights to the custom model"
            )
            return

        # Notify the user that generation is starting and may take time
        QMessageBox.information(
            None,
            "Generating Text",
            "Text generation is in progress.\n\nThis may take up to 5 minutes.\nPlease close this window and wait..."
        )

        # Identify which button triggered the generation
        sender = self.sender().objectName()

        # Set the model to evaluation mode
        self.model.eval()

        # Match the sender to a predefined generation setting
        match sender:
            case "pushButton_GenerateTextBySetting1_GeneratingTextByGPT2xlTransformer":
                prompt = ""
                self.generate(prompt, max_new_tokens=100, temperature=1.0, top_k=None)

            case "pushButton_GenerateTextBySetting2_GeneratingTextByGPT2xlTransformer":
                prompt = ""
                self.generate(prompt, max_new_tokens=100, temperature=0.9, top_k=40)

            case "pushButton_GenerateTextBySetting3_GeneratingTextByGPT2xlTransformer":
                prompt = "I went to the kitchen and"
                # Generate multiple outputs with different random seeds
                for i in range(5):
                    torch.manual_seed(i)
                    self.generate(prompt, max_new_tokens=10, temperature=1.0, top_k=None)

            case "pushButton_GenerateTextBySetting4_GeneratingTextByGPT2xlTransformer":
                prompt = "Lexington is the second largest city in the state of Kentucky"
                self.generate(prompt, max_new_tokens=100, temperature=1.0, top_k=None)

            case "pushButton_GenerateTextBySetting5_GeneratingTextByGPT2xlTransformer":
                prompt = "Lexington is the second largest city in the state of Kentucky"
                self.generate(prompt, max_new_tokens=100, temperature=0.9, top_k=50)

            case "pushButton_GenerateTextBySetting6_GeneratingTextByGPT2xlTransformer":
                prompt = "Lexington is the second largest city in the state of Kentucky"
                self.generate(prompt, max_new_tokens=100, temperature=1.2, top_k=None)

# Custom implementation of the GELU (Gaussian Error Linear Unit) activation function.
# This version uses the tanh-based approximation commonly used in transformer models like GPT.
class GELU(nn.Module):
    
    # Defines the forward pass of the GELU activation function.
    def forward(self, x):
        # Compute the GELU activation using the tanh-based approximation:
        # GELU(x) ≈ 0.5 * x * (1 + tanh(√(2/π) * (x + 0.044715 * x³)))
        return 0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x.pow(3))))
 
# Configuration class defining the hyperparameters for the GPT-2 XL model.
# These values control the architecture and regularization behavior of the model.
class Config():
    def __init__(self):
        # Number of transformer layers (blocks)
        self.n_layer = 48

        # Number of attention heads per layer
        self.n_head = 25

        # Dimensionality of the embedding and hidden states
        self.n_embd = 1600

        # Size of the vocabulary (number of unique tokens)
        self.vocab_size = 50257

        # Maximum sequence length (context window)
        self.block_size = 1024

        # Dropout probability for the embedding layer
        self.embd_pdrop = 0.1

        # Dropout probability for the residual connections
        self.resid_pdrop = 0.1

        # Dropout probability for the attention weights
        self.attn_pdrop = 0.1

# Implements causal (masked) multi-head self-attention as used in GPT-style transformers.
# Ensures that each token only attends to previous tokens (no future leakage).
class CausalSelfAttention(nn.Module):

    # Constructor initializes layers and parameters for attention.
    def __init__(self, config):
        super().__init__()

        # Linear layer to compute concatenated Q, K, V from input embeddings.
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)

        # Linear layer to project attention output back to embedding space.
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)

        # Dropout applied to attention weights.
        self.attn_dropout = nn.Dropout(config.attn_pdrop)

        # Dropout applied to final output of attention block.
        self.resid_dropout = nn.Dropout(config.resid_pdrop)

        # Causal mask to prevent attention to future tokens.
        self.register_buffer("bias", torch.tril(torch.ones(
            config.block_size, config.block_size)).view(1, 1, config.block_size, config.block_size))

        # Number of attention heads.
        self.n_head = config.n_head

        # Embedding dimension.
        self.n_embd = config.n_embd

    # Forward pass computes masked multi-head attention.
    def forward(self, x):
        # Extract batch size (B), sequence length (T), and embedding dim (C).
        B, T, C = x.size()

        # Compute Q, K, V by splitting the output of c_attn.
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)

        # Compute head size.
        hs = C // self.n_head

        # Reshape and transpose K for multi-head attention.
        k = k.view(B, T, self.n_head, hs).transpose(1, 2)

        # Reshape and transpose Q.
        q = q.view(B, T, self.n_head, hs).transpose(1, 2)

        # Reshape and transpose V.
        v = v.view(B, T, self.n_head, hs).transpose(1, 2)

        # Compute scaled dot-product attention scores.
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))

        # Apply causal mask to prevent attending to future positions.
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float('-inf'))

        # Convert scores to probabilities.
        att = F.softmax(att, dim=-1)

        # Apply dropout to attention weights.
        att = self.attn_dropout(att)

        # Compute weighted sum of values.
        y = att @ v

        # Reshape output back to original format.
        y = y.transpose(1, 2).contiguous().view(B, T, C)

        # Apply final projection and dropout.
        y = self.resid_dropout(self.c_proj(y))

        # Return the attention output.
        return y

# Defines a transformer block: LayerNorm → Attention → Residual → LayerNorm → MLP → Residual.
class Block(nn.Module):

    # Constructor initializes normalization, attention, and MLP layers.
    def __init__(self, config):
        super().__init__()

        # Layer normalization before attention.
        self.ln_1 = nn.LayerNorm(config.n_embd)

        # Causal self-attention module.
        self.attn = CausalSelfAttention(config)

        # Layer normalization before MLP.
        self.ln_2 = nn.LayerNorm(config.n_embd)

        # Feed-forward network (MLP) with GELU activation and dropout.
        self.mlp = nn.ModuleDict(dict(
            # First linear layer expands dimensionality.
            c_fc   = nn.Linear(config.n_embd, 4 * config.n_embd),

            # Second linear layer projects back to original size.
            c_proj = nn.Linear(4 * config.n_embd, config.n_embd),

            # GELU activation function.
            act    = GELU(),

            # Dropout for regularization.
            dropout = nn.Dropout(config.resid_pdrop),
        ))

        # Define MLP forward pass as a lambda function.
        m = self.mlp
        self.mlpf = lambda x: m.dropout(m.c_proj(m.act(m.c_fc(x))))

    # Forward pass applies attention and MLP with residual connections.
    def forward(self, x):
        # Apply attention with residual connection.
        x = x + self.attn(self.ln_1(x))

        # Apply MLP with residual connection.
        x = x + self.mlpf(self.ln_2(x))

        # Return the transformed output.
        return x

# Defines the full GPT-2 XL model architecture.
# Includes token and positional embeddings, a stack of transformer blocks, and a language modeling head.
class GPT2XL(nn.Module):

    # Constructor initializes embeddings, transformer blocks, and output head.
    def __init__(self, config):
        super().__init__()

        # Store maximum sequence length.
        self.block_size = config.block_size

        # Transformer components stored in a ModuleDict.
        self.transformer = nn.ModuleDict(dict(

            # Token embedding layer.
            wte = nn.Embedding(config.vocab_size, config.n_embd),

            # Positional embedding layer.
            wpe = nn.Embedding(config.block_size, config.n_embd),

            # Dropout after embeddings.
            drop = nn.Dropout(config.embd_pdrop),

            # Stack of transformer blocks.
            h = nn.ModuleList([Block(config) for _ in range(config.n_layer)]),

            # Final layer normalization.
            ln_f = nn.LayerNorm(config.n_embd),
        ))

        # Output projection layer for language modeling.
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

    # Forward pass processes input tokens and optionally computes loss.
    def forward(self, idx, targets=None):
        # Get batch size and sequence length.
        b, t = idx.size()

        # Generate position indices.
        pos = torch.arange(0, t, dtype=torch.long).unsqueeze(0)

        # Look up token embeddings.
        tok_emb = self.transformer.wte(idx)

        # Look up positional embeddings.
        pos_emb = self.transformer.wpe(pos)

        # Add embeddings and apply dropout.
        x = self.transformer.drop(tok_emb + pos_emb)

        # Pass through each transformer block.
        for block in self.transformer.h:
            x = block(x)

        # Apply final layer normalization.
        x = self.transformer.ln_f(x)

        # Project to vocabulary logits.
        logits = self.lm_head(x)

        # Initialize loss to None.
        loss = None

        # If targets are provided, compute cross-entropy loss.
        if targets is not None:
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)),
                targets.view(-1),
                ignore_index=-1
            )

        # Return logits and loss.
        return logits, loss
    
