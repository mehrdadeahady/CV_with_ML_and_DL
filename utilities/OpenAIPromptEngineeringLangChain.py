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
import traceback
from typing import Optional
from copy import deepcopy
from collections import Counter
import json
import pickle
import webbrowser
import xml.etree.ElementTree as ET
import regex as re
from functools import lru_cache
from utilities.DeepLearningFoundationOperations import DownloadLogPopup, LogEmitter
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
    import langchain
    from langchain.chat_models import init_chat_model
    from langchain.tools import BaseTool
    from langchain_classic.agents import  Tool, AgentExecutor, create_react_agent
    from langchain_core.prompts import PromptTemplate
    from langchain_core.messages import AIMessage
    from langchain_classic.chains import LLMChain
    from langchain_classic import hub
except:
    print("You Should Install langchain Library!")
try:
    import langchain_openai
    from langchain_openai import ChatOpenAI
except:
     print("You Should Install langchain_openai Library!")
try:
    import wolframalpha
except:
     print("You Should Install wolframalpha Library!")
try:
    import langchainhub
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
except:
    print("You Should Install langchainhub Library!")
try:
    from langchain_community.agent_toolkits.load_tools import load_tools
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
    from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
    from langchain_community.llms import GPT4All #, OpenAI
except:
     print("You Should Install langchain_community Library!")
try:
   from langchain_ollama.llms import OllamaLLM
   from langchain_ollama.chat_models import ChatOllama
except:
     print("You Should Install langchain_ollama Library!")
try:
   import wikipedia
except:
     print("You Should Install wikipedia Library!")
try: 
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
    from PyQt6.QtGui import  QTextCursor   
    from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt, QUrl
    from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QTextEdit,QScrollArea,QMainWindow,QApplication
except:
    print("You Should Install PyQt6 Library!")

# Define a class for managing OpenAI prompt engineering using LangChain tools
# Inherits from QObject to integrate with PyQt signal-slot mechanisms
class OpenAIPromptEngineeringLangChain(QObject):

    # Constructor method to initialize the class instance
    # Parameter:
    # - parent: Optional parent object for Qt object hierarchy (default is None)
    def __init__(self, parent=None):     
        # Call the constructor of the base QObject class
        super().__init__()

        # Instantiate a custom log emitter to handle and emit log messages
        self.log_emitter = LogEmitter()

        # Create a popup window to display logs related to download or processing steps
        # Pass the log emitter to allow real-time updates in the popup
        self.DownloadLogPopup = DownloadLogPopup(
            self.log_emitter
        )

    # Define a method to generate different types of content using OpenAI's API
    # Parameters:
    # - text: the type of output to generate ("Text", "Image", "Speech", or "Code")
    # - openai_api_key: the API key used to authenticate with OpenAI services
    # - systemRole: the system-level instruction to guide the assistant's behavior
    # - prompt: the user input or task description to be processed
    def GenerateByLLM(self, text, openai_api_key, systemRole, prompt):
        # Initialize the OpenAI client with the provided API key
        client = OpenAI(api_key=openai_api_key)

        try:
            # Disable the cancel button to prevent interruption during generation
            self.DownloadLogPopup.cancel_button.setEnabled(False)

            # Display the log popup to inform the user that processing has started
            self.DownloadLogPopup.show()

            # Append a log message indicating that the prompt has been sent and processing is underway
            self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

            # Use a match-case structure to handle different types of generation based on the 'text' parameter
            match text:

                # Case 1: Generate a text-based response using ChatGPT
                case "Text":
                    # Send a chat completion request to OpenAI with system and user messages
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": systemRole},
                            {"role": "user", "content": prompt}
                        ]
                    )

                    # Append the generated response to the log popup
                    self.DownloadLogPopup.Append_Log("Response:\n" + str(completion.choices[0].message.content))

                # Case 2: Generate an image using DALL·E
                case "Image":
                    # Send an image generation request to OpenAI's DALL·E model
                    response = client.images.generate(
                        model="dall-e-2",
                        prompt=prompt,
                        size="auto",
                        n=1,
                    )

                    # Extract the image URL from the response and open it in the default web browser
                    image_url = response.data[0].url
                    webbrowser.open(image_url)

                # Case 3: Generate speech audio using OpenAI's TTS model
                case "Speech":
                    try:
                        # Attempt to import the pygame library for audio playback
                        import pygame
                    except:
                        # If pygame is not installed, notify the user via console
                        print("You Should Install pygame Library!")

                    # Send a speech synthesis request to OpenAI's TTS model
                    response = client.audio.speech.create(
                        model="tts-1-hd",
                        voice="shimmer",
                        input=prompt
                    )

                    # Save the generated audio to a temporary MP3 file
                    response.stream_to_file("temp/speech.mp3")

                    # Initialize the pygame mixer for audio playback
                    pygame.mixer.init()

                    # Load and play the MP3 file
                    pygame.mixer.music.load("temp/speech.mp3")
                    pygame.mixer.music.play()

                    # Keep the script running until the audio finishes playing
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

                # Case 4: Generate and execute Python code
                case "Code":
                    # Send a chat completion request to generate Python code
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": systemRole},
                            {"role": "user", "content": prompt}
                        ]
                    )

                    # Extract the generated code from the response
                    code = completion.choices[0].message.content

                    # Execute the generated code (⚠️ use with caution — this can be dangerous)
                    exec(code)

        # Handle any exceptions that occur during generation or execution
        except Exception as e:
            # Display a critical error message box with the exception details
            QMessageBox.critical(
                None,                      # No parent widget
                "Generation Failed",       # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

    # Define a method to invoke a simple OpenAI language model using LangChain
    # Parameters:
    # - openai_api_key: the API key used to authenticate with OpenAI
    # - prompt: the user-provided input prompt to be processed by the model
    def OpenAIinLangChain(self, openai_api_key, prompt):
        try:
            # Disable the cancel button in the log popup to prevent user interruption during processing
            self.DownloadLogPopup.cancel_button.setEnabled(False)

            # Display the log popup window to inform the user that processing has started
            self.DownloadLogPopup.show()

            # Append a log message indicating that the prompt has been sent and processing is underway
            self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

            # Initialize the OpenAI language model using LangChain's OpenAI wrapper
            # This uses the provided API key to authenticate with OpenAI's API
            llm = langchain_openai.OpenAI(openai_api_key=openai_api_key)

            # Invoke the model with the user prompt and store the response
            res = llm.invoke(prompt)

            # Append the model's response to the log popup for user visibility
            self.DownloadLogPopup.Append_Log("Response:\n" + str(res))

        # Handle any exceptions that occur during model invocation or UI updates
        except Exception as e:
            # Display a critical error message box with the exception details
            QMessageBox.critical(
                None,                      # No parent widget
                "Operation Failed",        # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

    # Define a method to query Wolfram Alpha using LangChain's WolframAlphaTool
    # Parameters:
    # - WolframAlpha_api_key: API key used to authenticate with the Wolfram Alpha API
    # - prompt: the user-provided query to be sent to Wolfram Alpha
    def WolframAlphaInLangChain(self, WolframAlpha_api_key, prompt):
        try:
            # Disable the cancel button in the log popup to prevent user interruption during processing
            self.DownloadLogPopup.cancel_button.setEnabled(False)

            # Display the log popup window to inform the user that processing has started
            self.DownloadLogPopup.show()

            # Append a log message indicating that the prompt has been sent and processing is underway
            self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

            # Initialize the Wolfram Alpha tool with the provided API key
            wolfram = WolframAlphaTool(appid=WolframAlpha_api_key)

            # Run the user's prompt through the Wolfram Alpha tool and store the result
            result = wolfram.run(prompt)

            # Append the result to the log popup so the user can see the answer
            self.DownloadLogPopup.Append_Log("Response:\n" + str(result))

        # Handle any exceptions that occur during tool initialization or execution
        except Exception as e:
            # Capture and print the full traceback for debugging purposes
            error_details = traceback.format_exc()
            print("Full error traceback:\n", error_details)

            # Display a critical error message box with the exception details
            QMessageBox.critical(
                None,                      # No parent widget
                "Operation Failed",        # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

    # Define a method to query Wikipedia using LangChain's Wikipedia tool
    # Parameter:
    # - prompt: the user-provided query string to search for on Wikipedia
    def WikipediaQueryInLangChain(self, prompt):   
        try:
            # Disable the cancel button in the log popup to prevent user interruption during processing
            self.DownloadLogPopup.cancel_button.setEnabled(False)

            # Display the log popup window to inform the user that processing has started
            self.DownloadLogPopup.show()

            # Append a log message indicating that the prompt has been sent and processing is underway
            self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

            # Initialize the Wikipedia query tool using LangChain's WikipediaAPIWrapper
            wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

            # Execute the Wikipedia search using the provided prompt and store the result
            res = wikipedia.run(prompt)

            # Append the retrieved result to the log popup for user visibility
            self.DownloadLogPopup.Append_Log("Response:\n" + str(res))

        # Handle any exceptions that occur during tool initialization or execution
        except Exception as e:
            # Capture and print the full traceback for debugging purposes
            error_details = traceback.format_exc()
            print("Full error traceback:\n", error_details)

            # Display a critical error message box with the exception details
            QMessageBox.critical(
                None,                      # No parent widget
                "Operation Failed",        # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

    # Define a method to run a LangChain ReAct agent using OpenAI and external tools
    # Parameters:
    # - WolframAlpha_api_key: API key for Wolfram Alpha tool integration
    # - LangChain_api_key: API key for accessing LangChain Hub (LangSmith)
    # - openai_api_key: API key for OpenAI's GPT models
    # - user_prompt: the user-provided input to be processed by the agent
    def AgentInLangChain(self, WolframAlpha_api_key, LangChain_api_key, openai_api_key, user_prompt):
        try:
            # Disable the cancel button in the log popup to prevent user interruption during processing
            self.DownloadLogPopup.cancel_button.setEnabled(False)

            # Display the log popup window to inform the user that processing has started
            self.DownloadLogPopup.show()

            # Append a log message indicating that the prompt has been sent and processing is underway
            self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

            # Set the OpenAI API key in the environment for use by LangChain's OpenAI wrapper
            os.environ['OPENAI_API_KEY'] = openai_api_key

            # Set the Wolfram Alpha App ID in the environment for use by the Wolfram Alpha tool
            os.environ["WOLFRAM_ALPHA_APPID"] = WolframAlpha_api_key

            # Set the LangChain API key in the environment to enable access to LangChain Hub
            os.environ['LANGCHAIN_API_KEY'] = LangChain_api_key

            # Enable LangChain tracing for debugging and observability (optional but useful)
            os.environ['LANGCHAIN_TRACING_V2'] = 'true'

            # Pull a predefined ReAct-style agent prompt from the LangChain Hub
            agent_prompt = hub.pull("hwchase17/react")

            # Initialize the OpenAI language model using the GPT-3.5-turbo model
            llm = ChatOpenAI(model_name='gpt-3.5-turbo')

            # Define a list of tool names to be loaded into the agent
            tool_names = ["wolfram-alpha"]  # Add Wolfram Alpha tool
            tool_names += ["wikipedia"]     # Add Wikipedia tool

            # Load the specified tools using the language model
            tools = load_tools(tool_names, llm=llm)

            # Create a ReAct-style agent using the language model, tools, and the pulled prompt
            agent = create_react_agent(llm, tools, agent_prompt)

            # Wrap the agent in an executor to manage tool usage and handle parsing errors
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                handle_parsing_errors=True,
                verbose=True
            )

            # Invoke the agent with the user's input and store the result
            res = agent_executor.invoke({"input": user_prompt})

            # Append the agent's final output to the log popup for user visibility
            self.DownloadLogPopup.Append_Log(str(res["output"]))

        # Handle any exceptions that occur during setup or execution
        except Exception as e:
            # Capture and print the full traceback for debugging purposes
            error_details = traceback.format_exc()
            print("Full error traceback:\n", error_details)

            # Display a critical error message box with the exception details
            QMessageBox.critical(
                None,                      # No parent widget
                "Operation Failed",        # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

    # Define a method to generate different types of outputs using LangChain tools and OpenAI
    # Parameters:
    # - WolframAlpha_api_key: API key for Wolfram Alpha integration
    # - LangChain_api_key: API key for accessing LangChain Hub (LangSmith)
    # - kind: the type of output to generate ("Text", "Code", or "Image")
    # - openai_api_key: API key for OpenAI's GPT models
    # - user_input: the user-provided prompt to be processed by the agent
    def GenerateByLangChain(self, WolframAlpha_api_key, LangChain_api_key, kind, openai_api_key, user_input):
        try:
            # Disable the cancel button to prevent user interruption during processing
            self.DownloadLogPopup.cancel_button.setEnabled(False)

            # Show the log popup window to inform the user that processing has started
            self.DownloadLogPopup.show()

            # Append a log message indicating that the prompt has been sent and processing is underway
            self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

            # Set required environment variables for OpenAI, Wolfram Alpha, and LangChain
            os.environ['OPENAI_API_KEY'] = openai_api_key
            os.environ["WOLFRAM_ALPHA_APPID"] = WolframAlpha_api_key
            os.environ['LANGCHAIN_API_KEY'] = LangChain_api_key
            os.environ['LANGCHAIN_TRACING_V2'] = 'true'

            # Load a predefined ReAct-style agent prompt from LangChain Hub
            agent_prompt = hub.pull("hwchase17/react")

            # Initialize the OpenAI language model using GPT-3.5-turbo
            llm = ChatOpenAI(model_name='gpt-3.5-turbo')

            # Load built-in tools: Wolfram Alpha and Wikipedia
            tool_names = ["wolfram-alpha", "wikipedia"]
            tools = load_tools(tool_names, llm=llm)

            # Add custom tools using LLMChains and prompt templates
            tools += [
                # Tool for summarizing text into one sentence
                Tool.from_function(
                    func=LLMChain(llm=llm, prompt=PromptTemplate(
                        input_variables=["text"],
                        template="Write a one sentence summary of the following text: {text}"
                    )).run,
                    name="Text Summarizer",
                    description="A tool for summarizing texts"
                ),
                # Tool for generating jokes based on a subject
                Tool.from_function(
                    func=LLMChain(llm=llm, prompt=PromptTemplate(
                        input_variables=["subject"],
                        template="Tell a joke on the following subject: {subject}"
                    )).run,
                    name="Joke Teller",
                    description="A tool for telling jokes"
                ),
                # Tool for classifying sentiment of a given text
                Tool.from_function(
                    func=LLMChain(llm=llm, prompt=PromptTemplate(
                        input_variables=["text"],
                        template="Classify the following text as positive, negative, or neutral: {text}"
                    )).run,
                    name="Sentiment Classifier",
                    description="A tool to classify sentiment"
                ),
                # Tool for generating Python code from a description
                Tool.from_function(
                    func=LLMChain(llm=llm, prompt=PromptTemplate(
                        input_variables=["text"],
                        template="Write a Python program based on the description in the following text: {text}"
                    )).run,
                    name="Code Generator",
                    description="A tool to generate code"
                ),
                # Tool for generating image prompts from text
                Tool.from_function(
                    func=LLMChain(llm=llm, prompt=PromptTemplate(
                        input_variables=["text"],
                        template="Create an image based on the following text: {text}"
                    )).run,
                    name="Text to image",
                    description="A tool for text to image"
                )
            ]

            # Create a ReAct-style agent using the language model, tools, and prompt
            agent = create_react_agent(llm, tools, agent_prompt)

            # Wrap the agent in an executor to manage execution and handle parsing errors
            agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)

            # Handle different output types based on the 'kind' parameter
            if kind == "Text":
                # Invoke the agent with the user input and display the textual result
                res = agent_executor.invoke({"input": user_input})
                self.DownloadLogPopup.Append_Log(str(res["output"]))

            elif kind == "Code":
                # Invoke the agent to generate code and attempt to execute it
                res = agent_executor.invoke({"input": user_input})
                code = res["output"]
                try:
                    exec(code)  # ⚠️ Use with caution — executing arbitrary code can be dangerous
                except Exception as exec_error:
                    self.DownloadLogPopup.Append_Log(f"Code execution error: {exec_error}")

            elif kind == "Image":
                # Invoke the agent to generate an image prompt and use DALL·E to create the image
                res = agent_executor.invoke({"input": user_input})
                image_prompt = res["output"]
                try:
                    image_url = DallEAPIWrapper().run(image_prompt)
                    webbrowser.open(image_url)
                except Exception as image_error:
                    self.DownloadLogPopup.Append_Log(f"Image generation error: {image_error}")

            else:
                # Handle unknown output types
                self.DownloadLogPopup.Append_Log(f"Unknown kind: {kind}")

        # Handle any exceptions that occur during setup or execution
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print("Full error traceback:\n", error_details)
            QMessageBox.critical(
                None,                      # No parent widget
                "Operation Failed",        # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

    # Define a private method to set an environment variable if it's not already set
    def _set_env(self, var: str):
        # Check if the environment variable is not already defined
        if not os.environ.get(var):
            # Create a new input dialog with no parent widget
            dialog = QInputDialog(None)
            # Set the dialog window title to prompt for the variable
            dialog.setWindowTitle(f"Enter {var}")
            # Set the label text to instruct the user to input the variable's value
            dialog.setLabelText(f"Please enter the value for {var}:")
            # Mask the input text for privacy (e.g., for passwords or tokens)
            dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
            # Resize the dialog to a fixed width while keeping the current height
            dialog.resize(700, dialog.height())
            # Execute the dialog and check if the user confirmed input
            if dialog.exec():
                # Retrieve the text entered by the user
                value = dialog.textValue()
                # If a value was entered, set it as an environment variable
                if value:
                    os.environ[var] = value

    # Define a method to send a prompt to an OpenAI chat model via LangChain and display the response
    def AddChatOpenAIModelToLangChain(self, prompt):
        # Ensure the OpenAI API key is set in the environment variables
        self._set_env("OPENAI_API_KEY")

        # Disable the cancel button in the log popup to prevent user interruption during processing
        self.DownloadLogPopup.cancel_button.setEnabled(False)

        # Show the log popup window to indicate that processing has started
        self.DownloadLogPopup.show()

        # Log a message to inform the user that the prompt has been sent and a response is pending
        self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

        try:
            # Initialize the OpenAI chat model using LangChain with the specified model name and provider
            llm = init_chat_model("gpt-4o-mini", model_provider="openai")

            # Send the prompt to the model and retrieve the response
            response = llm.invoke(prompt)

            # Display the model's response in the log popup for the user to see
            self.DownloadLogPopup.Append_Log("Response:\n" + str(response.content))

        # Handle any exceptions that occur during model interaction or UI updates
        except Exception as e:
            # Close the log popup window in case of an error
            self.DownloadLogPopup.close()
            # Show a critical error message box with the exception details
            QMessageBox.critical(
                None,                      # No parent widget
                "Operation Failed",        # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

    # Define a method to send a prompt to an Anthropic chat model via LangChain and display the response
    def AddChatAnthropicModelToLangChain(self, prompt):
        # Ensure the Anthropic API key is set in the environment variables
        self._set_env("ANTHROPIC_API_KEY")

        # Disable the cancel button in the log popup to prevent user interruption during processing
        self.DownloadLogPopup.cancel_button.setEnabled(False)

        # Show the log popup window to indicate that processing has started
        self.DownloadLogPopup.show()

        # Log a message to inform the user that the prompt has been sent and a response is pending
        self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

        try:
            # Initialize the Anthropic chat model using LangChain with the specified model name and provider
            llm = init_chat_model("claude-3-5-sonnet-latest", model_provider="anthropic")

            # Send the prompt to the model and retrieve the response
            response = llm.invoke(prompt)

            # Display the model's response in the log popup for the user to see
            self.DownloadLogPopup.Append_Log("Response:\n" + str(response.content))

        # Handle any exceptions that occur during model interaction or UI updates
        except Exception as e:
            # Close the log popup window in case of an error
            self.DownloadLogPopup.close()
            # Show a critical error message box with the exception details
            QMessageBox.critical(
                None,                      # No parent widget
                "Operation Failed",        # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

    # Define a method to send a prompt to an Ollama chat model via LangChain and display the response
    def AddChatOllamaModelToLangChain(self, prompt, systemRole):
        # Disable the cancel button in the log popup to prevent user interruption during processing
        self.DownloadLogPopup.cancel_button.setEnabled(False)

        # Show the log popup window to indicate that processing has started
        self.DownloadLogPopup.show()

        # Log a message to inform the user that the prompt has been sent and a response is pending
        self.DownloadLogPopup.Append_Log("Prompt sent.\nIt takes minutes\nPlease wait for answer...")

        try:
            # Initialize the Ollama chat model with specified parameters
            llm = ChatOllama(
                model="gemma3:1b",  # Specify the model to use
                temperature=0,      # Set temperature for deterministic output
                # other params...
            )

            # Construct the message sequence with system and user roles
            messages = [
                ("system", systemRole),  # Define the system's role or behavior
                ("human", prompt),       # Provide the user's prompt
            ]

            # Send the message sequence to the model and retrieve the response
            response = llm.invoke(messages)

            # Display the model's response in the log popup for the user to see
            self.DownloadLogPopup.Append_Log("Response:\n" + str(response.content))

        # Handle any exceptions that occur during model interaction or UI updates
        except Exception as e:
            # Close the log popup window in case of an error
            self.DownloadLogPopup.close()
            # Show a critical error message box with the exception details
            QMessageBox.critical(
                None,                      # No parent widget
                "Operation Failed",        # Title of the error message box
                f"An error occurred:\n{str(e)}"  # Display the error message
            )

# Define a custom LangChain tool for querying Wolfram Alpha
# Inherits from BaseTool to integrate with LangChain's tool interface
class WolframAlphaTool(BaseTool):
    # Name of the tool as it will be referenced by LangChain agents
    name: str = "wolfram_alpha"

    # Description of the tool's purpose, used by agents to decide when to invoke it
    description: str = "Useful for answering factual and mathematical questions using WolframAlpha"

    # Wolfram Alpha App ID required for API authentication
    appid: str

    # Synchronous method to execute the tool with a given query
    def _run(self, query: str) -> str:
        # Define the base URL for the Wolfram Alpha API
        url = "http://api.wolframalpha.com/v2/query"

        # Construct the query parameters including the user input, app ID, and response format
        params = {
            "input": query,
            "appid": self.appid,
            "format": "plaintext"
        }

        # Send a GET request to the Wolfram Alpha API with the specified parameters
        response = requests.get(url, params=params)

        # Raise an exception if the response status code indicates an error
        response.raise_for_status()

        # Parse the XML response returned by the API
        root = ET.fromstring(response.text)

        # Initialize a list to collect formatted result strings
        results = []

        # Iterate through all <pod> elements in the XML response
        for pod in root.findall(".//pod"):
            # Extract the title attribute of the pod (e.g., "Result", "Input interpretation")
            title = pod.attrib.get("title", "")

            # Find the first <plaintext> element within the pod
            plaintext = pod.find(".//plaintext")

            # If plaintext exists and contains text, format and append it to the results list
            if plaintext is not None and plaintext.text:
                results.append(f"{title}: {plaintext.text}")

        # Join all result strings with double line breaks, or return a fallback message if empty
        return "\n\n".join(results) if results else "No results found."

    # Asynchronous execution is not supported for this tool
    def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")