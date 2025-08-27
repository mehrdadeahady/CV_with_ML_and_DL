# Import Essential Libraries
from utilities.ScrollableMessageBox import show_scrollable_message
import os
from os.path import isfile, join
import sys
import time
import threading
import urllib.request
import urllib.error
import hashlib
import json
import traceback
try:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    import tensorflow as tf
    from keras.applications import VGG16
    from keras.applications.vgg16 import VGG16
    from keras.applications import imagenet_utils
    from keras.preprocessing.image import img_to_array, load_img
    from keras.models import load_model
    from keras.utils import get_file
    import urllib.request
except:
    print("Check instalation of Tensorflow and Keras for Compatibility with OS and HardWare!")
try:
    import numpy as np
except:
    print("You Should Install numpy Library")
try:
    import cv2
except:
    print("You Should Install OpenCV-Python and cv2_enumerate_cameras Libraries")
try:    
    from PyQt6.QtCore import QObject, pyqtSignal,QTimer, Qt, QThread,QUrl
    from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
    from PyQt6.QtWidgets import QProgressBar,QMessageBox, QFileDialog, QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton,QWidget,QLabel
except:
    print("You Should Install PyQt6 Library!")
        
class DeepLearningFoundationOperations(QObject):
    def __init__(self,ImagesAndColorsHandler,CreateSimpleCNNHandler,parent=None):
        super().__init__()
        # Internal Variable to Access Images, Videos and Cameras inside All Functions in the Class      
        self.camera = None
        self.ImagesAndColorsHandler = ImagesAndColorsHandler
        self.CreateSimpleCNNHandler = CreateSimpleCNNHandler
        self.DownloadLogPopup = None
        self._is_running = False
        self.downloadResult = None
        self.log_emitter = LogEmitter()
        self.log_emitter.log_signal.connect(self.Append_Log)       
        self.log_emitter.progressbar_signal.connect(self.Update_Progress)  
        self.log_emitter.finished_signal.connect(self.On_Finished)
        
    # Consider|Attention: 
    # Loading_Model_Operation Function Contains Computer Vision Functions with Comments and Explanation
    # Rest of Functions are Pre-Processor and Helpers

    # Updating Logs After Download Finished
    def On_Finished(self, success, info ,modelType,filepath, imagePath):
        if not success:
            log = "Download Failed.\n" + str(info)
            if not "Download Cancelled" in str(info):
                log += "\nCheck Internet Connectivity!\nTry by VPN"

            self.DownloadLogPopup.Append_Log(log)
                                             
        else:
            self.DownloadLogPopup.Append_Log("Download Success.\nDownload Complete.")   
            self.Loading_Model_Operation(modelType, filepath, imagePath)

    # Loading Downloaded or Existing Model and Complete the Operation
    def Loading_Model_Operation(self,modelType, filepath, imagePath):
            self.log_emitter.log_signal.emit("Loading model weights...")
            match modelType:
                case "VGGNet16":
                    # This is a command for Download/Load with Tracing only in Console Not UI
                    # model = VGG16(weights="imagenet") 
                    '''             
                    model.load_weights() is a function used in deep learning frameworks like Keras and TensorFlow to load pre-trained weights into a neural network model. 
                    This function is particularly useful in scenarios such as: 

                    Resuming training:
                    If training is interrupted or needs to be continued from a specific point, load_weights() allows the model to pick up where it left off without starting from scratch.
                    Transfer learning:
                    Pre-trained weights from a model trained on a large dataset can be loaded into a new model, which is then fine-tuned on a smaller, related dataset, leveraging the learned features.
                    Deployment for inference:
                    Once a model is trained, its weights can be saved and then loaded into a new model instance for making predictions without needing to re-train. 

                    Key considerations when using model.load_weights():

                    Architectural compatibility:
                    The model receiving the weights must have the exact same architecture (layer types, order, and configurations) as the model from which the weights were saved. TensorFlow and Keras match weights based on layer order and naming.
                    File format:
                    Weights are typically saved in formats like HDF5 (.h5) or TensorFlow's native format. The load_weights() function expects the path to the saved weights file.
                    Optimizer state:
                    When loading weights, the optimizer's state (e.g., learning rate, momentum) is typically reset. If resuming training and preserving the optimizer state is crucial, saving and loading the entire model (including the optimizer) might be necessary using model.save() and tf.keras.models.load_model().
                    by_name and skip_mismatch arguments:
                    These optional arguments can be used to control how weights are loaded, particularly when dealing with minor architectural differences or partial weight loading. by_name=True loads weights based on layer names, while skip_mismatch=True allows loading even if some layers don't have matching weights. 
                    '''
                    # Creating an empty VGG16 Model
                    model = VGG16(weights=None)
                    # Loding Weights into the Model
                    model.load_weights(filepath)
                    self.log_emitter.log_signal.emit("Model loaded successfully.")
                    time.sleep(1)
                    # Close Download/Load Log Window
                    self.DownloadLogPopup.close()
                    # Show Model Architecture in A new Popup
                    show_scrollable_message("Model Summary:", self.CreateSimpleCNNHandler.ModelSummaryCapture(model))
                    # If Selected Image not Closed Bring it to Top
                    imageName = self.ImagesAndColorsHandler.imageName or self.ImagesAndColorsHandler.tempImageName
                    if imageName is not None:
                       print(imageName, cv2.getWindowProperty(imageName, cv2.WND_PROP_VISIBLE))
                       if cv2.getWindowProperty(imageName, cv2.WND_PROP_VISIBLE) >= 1:
                          cv2.setWindowProperty(imageName, cv2.WND_PROP_TOPMOST, 1)          
                    # Loading the Image to Predict
                    img = load_img(imagePath)          
                    # Resize the Image to 224x224 Square Shape
                    img = img.resize((224,224))
                    # Convert the Image to Array
                    img_array = img_to_array(img)
                    # Convert the Image into a 4 Dimensional Tensor
                    # Convert from (Height, Width, Channels), (Batchsize, Height, Width, Channels)
                    img_array = np.expand_dims(img_array, axis=0)
                    '''                  
                    The keras.applications.imagenet_utils.preprocess_input function is a utility designed to preprocess image data before it is fed into 
                    Keras models that have been pre-trained on the ImageNet dataset. These models, such as VGG16, ResNet50, MobileNet, etc., 
                    expect input images to be preprocessed in a specific way that matches the preprocessing applied during their original training.
                    Functionality:
                    This function takes a tensor or NumPy array representing a batch of images as input and applies transformations based on the specified mode. 
                    The available modes are: 
                        caffe:
                        This mode converts images from RGB to BGR and then zero-centers each color channel with respect to the ImageNet dataset's channel means, 
                        without scaling the pixel values.
                        tf:
                        This mode scales pixel values to be between -1 and 1, on a sample-wise basis.
                        torch:
                        This mode scales pixel values between 0 and 1 and then normalizes each channel using the ImageNet dataset's channel means and standard deviations.
                    '''
                    # Preprocess the Input Image Array
                    img_array = imagenet_utils.preprocess_input(img_array)
                    '''                    
                    The model.predict() method in machine learning is used to generate predictions from a trained model on new, unseen input data.
                    Functionality:
                        Input: It takes input data (often in the form of NumPy arrays or tf.data.Dataset objects in frameworks like TensorFlow/Keras) 
                        that the model has not previously encountered during training.
                    Processing: 
                        The input data is passed through the layers of the trained model.
                    Output: 
                        It returns the model's output, which represents the predictions for the given input. The format of the output depends on the type of model: 
                        Classification Models: 
                              For classification tasks, model.predict() often returns probabilities for each class (e.g., a vector of probabilities 
                              for a multi-class classification, or a single probability for binary classification if a sigmoid activation is used in the output layer)
                        Regression Models: 
                              For regression tasks, it returns the predicted numerical values.
                    Usage:
                        The primary purpose of model.predict() is to apply a trained model to new data to obtain its predictions, enabling tasks such as forecasting, 
                        classification of new instances, or generating recommendations.
                    '''
                    # Predict Using Predict() method (New Method)
                    prediction = model.predict(img_array)
                    '''                    
                    The keras.imagenet_utils.decode_predictions function is a utility within Keras (now primarily integrated with TensorFlow as tf.keras) 
                    designed to interpret the raw predictions generated by models trained on the ImageNet dataset.
                    Purpose:
                    This function translates the numerical output (typically a 1000-dimensional vector of probabilities) from a pre-trained ImageNet model into 
                    human-readable class labels and their corresponding confidence scores.
                    Usage:
                    The function takes two main arguments:

                        preds:
                        A NumPy array representing a batch of predictions from an ImageNet-trained model. This array should have a shape of (samples, 1000), 
                        where samples is the number of images in the batch and 1000 corresponds to the 1000 ImageNet classes.
                        top:
                        An optional integer specifying how many top-ranking predictions (classes) to return for each sample. The default value is typically 5. 

                    Output:
                    It returns a list of lists. Each inner list corresponds to a sample in the input batch and contains a list of tuples. Each tuple represents 
                    a top prediction and consists of:

                        class_name: The ImageNet class identifier (e.g., 'n02129165').
                        class_description: A human-readable description of the class (e.g., 'lion').
                        score: The confidence score (probability) assigned to that class by the model.
                    '''
                    # Decode the Prediction
                    actual_prediction = imagenet_utils.decode_predictions(prediction)
                    # Display the Result of Prediction on Top of Image
                    msgBox = QMessageBox(parent=None)
                    msgBox.setWindowTitle("Detection Result:")
                    msgBox.setText("Predicted Object is:\n" + str(actual_prediction[0][0][1]).title() + "\nWith Accuracy:\n" + str(actual_prediction[0][0][2]*100))
                    msgBox.setWindowFlags(msgBox.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                    msgBox.exec()
                                            
    # Updating ProgressBar
    def Update_Progress(self, percent):
        if self._is_running:
           self.DownloadLogPopup.Update_Progress(percent)

    # Updating Logs
    def Append_Log(self,message):
        if self._is_running:
           self.DownloadLogPopup.Append_Log(message)

    # Selecting Desired Operation
    def SelectDeepLearningOperations(self,text,imagePath):
        self.DownloadLogPopup = None
        match text.strip():
            case "Image Recognition using Pre-Trained VGGNet16 Model":
                if self.ImagesAndColorsHandler.image is not None and self.ImagesAndColorsHandler.imageName is not None:
                    modelType = text.strip().split(" ")[4]
                    
                    models = {}
                    self.DownloadLogPopup = DownloadLogPopup(self.log_emitter)   
                    self.DownloadLogPopup.show()
                    self._is_running = True         
                    try:
                        with open('models.json', 'r') as f:
                            models = json.load(f)
                    except FileNotFoundError:
                        self.log_emitter.log_signal.emit("Error: 'models.json' not found. Please ensure the file exists in the correct directory.")
                    except json.JSONDecodeError:
                        self.log_emitter.log_signal.emit("Error: Could not decode JSON from 'models.json'. Check the file's format.")
                    if len(models) > 0:                           
                        self.log_emitter.log_signal.emit("Checking for existing model file...")
                        url =  models[modelType]["url"] 
                        filename = models[modelType]["name"] 
                        expected_hash = models[modelType]["md5hash"] 
                        folder = os.path.normpath(join("resources","models"))
                        filepath = os.path.join(folder, filename)
                        if os.path.exists(filepath):
                            if self.File_Hash_Validation("md5",filepath, expected_hash,self.log_emitter,True):
                                self.log_emitter.log_signal.emit(str(models[modelType]["name"]) + "\nModel file found locally with valid hash.\nLoading from cache...")
                            else:
                                self.log_emitter.log_signal.emit(str(models[modelType]["name"]) + 
                                                                 "\nModel file found but hash mismatch.\nRe-downloading from internet...\n" +
                                                                 "Make Sure your System Connected to the Internet\n"+
                                                                 "File is Approximately 530 MB\n"+
                                                                 "It takes a while Depending on the Speed of your System and Internet!")
                        else:
                            self.log_emitter.log_signal.emit(str(models[modelType]["name"]) + 
                                                             "\nModel file not found. \nDownloading from internet...\n" + 
                                                             "Make Sure your System Connected to the Internet\n"+
                                                             "File is Approximately 530 MB\n"+
                                                             "It takes a while Depending on the Speed of your System and Internet!")
                            
                            self.log_emitter.log_signal.emit("Download Url: \n" + str(models[modelType]["url"]))           
                        
                        # Only Download if File is missing or Hash is Invalid
                        if not os.path.exists(filepath) or not self.File_Hash_Validation("md5",filepath, expected_hash,self.log_emitter, False) and self._is_running:      
                            self.downloader = Downloader(url, filepath, modelType,imagePath,self.log_emitter)
                            self.DownloadLogPopup.set_downloader(self.downloader)
                            self.downloader.start()   
                          
                        else:
                            self.Loading_Model_Operation(modelType, filepath,imagePath)
                                     
                else:
                    QMessageBox.warning(None, "No Image Selected","First, Select an Image!")

            case "Image Recognition using Pre-Trained VGGNet19 Model":
                print(text)
            case "Image Recognition using Pre-Trained ResNet Model":
                print(text)
            case "Image Recognition using Pre-Trained Inception Model":
                print(text)
            case "Image Recognition using Pre-Trained Xception Model":
                print(text)
            case "Object Detection by Pre-Trained Mobilenet SSD Model on Images":
                print(text)
            case "Object Detection by Pre-Trained Mobilenet SSD Model on Pre-Saved Video":
                print(text)
            case "Object Detection by Pre-Trained Mobilenet SSD Model on Realtime Video":
                print(text)
            case "Object Mask Implementation by Pre-Trained MaskRCNN Model on Images":
                print(text)
            case "Bounding Box Implementation by Pre-Trained MaskRCNN Model on Images":
                print(text)
            case "Object Detection by Pre-Trained MaskRCNN Model on Pre-Saved Video":
                print(text)
            case "Object Detection by Pre-Trained MaskRCNN Model on Realtime Video":
                print(text)
            case "Object Detection by Pre-Trained Tiny YOLO Model on Images":
                print(text)
            case "Object Detection by Pre-Trained Tiny YOLO Model on Pre-Saved Video":
                print(text)
            case "Object Detection by Pre-Trained Tiny YOLO Model on Realtime Video":
                print(text)
            case "Object Detection by Pre-Trained YOLO Model on Images":
                print(text)
            case "Object Detection by Pre-Trained Optimized YOLO Model on Images":
                print(text)
            case "Object Detection by Pre-Trained YOLO Model on Pre-Saved Video":
                print(text)
            case "Object Detection by Pre-Trained Optimized YOLO Model on Pre-Saved Video":
                print(text)
            case "Object Detection by Pre-Trained YOLO Model on Realtime Video":
                print(text)
            case "Object Detection by Pre-Trained Optimized YOLO Model on Realtime Video":
                print(text)

        self.WaitKeyCloseWindows()       

    # Selecting Active Camera
    def SelectDeepLearningCamera(self,text):
        if text.strip() != "":
           self.camera = int((text.split(",")[0]).split(":")[1].strip())

    # Validating Hash of Files
    def File_Hash_Validation(self,type,path, expected_hash,log_emitter,check):
        """Check if the file's SHA256 or MD5 hash matches the expected value."""
        match type:
            case "sha256":
                sha256 = hashlib.sha256()
                try:
                    with open(path, "rb") as f:
                        for chunk in iter(lambda: f.read(8192), b""):
                            sha256.update(chunk)
                            actual_hash = sha256.hexdigest()
                            if check:
                                log_emitter.log_signal.emit("Expected Hash: " + str(expected_hash))
                                log_emitter.log_signal.emit("Actual    Hash: " + str(actual_hash))
                    return actual_hash == expected_hash
                except Exception as e:
                    print("Error:", e)
                    return False
                
            case "md5":
                md5 = hashlib.md5()
                try:
                    with open(path, "rb") as f:
                        for chunk in iter(lambda: f.read(8192), b""):
                            md5.update(chunk)
                    actual_hash = md5.hexdigest()
                    if check:
                        log_emitter.log_signal.emit("Expected Hash: " + str(expected_hash))
                        log_emitter.log_signal.emit("Actual    Hash: " + str(actual_hash))
                    return actual_hash == expected_hash
                except Exception as e:
                    print("Error:", e)
                    return False

    # Wait for Clicking a Key on Keyboard to Close All cv2 Windows
    def WaitKeyCloseWindows(self):
        # Wait until Clicking a Key on Keyboard
        cv2.waitKey(0)
        # Close All cv2 Windows
        cv2.destroyAllWindows()

# Signal emitter for Thread-Safe logging
class LogEmitter(QObject):
    log_signal = pyqtSignal(str) # All Communications, Updates and Text Messages
    progressbar_signal = pyqtSignal(int) #  Percent: ProgressBar Update
    finished_signal = pyqtSignal(bool, str, str , str, str) # success ,message info [error, cancel, success, fail] ,modelType , filepath, imagePath

# Dialog for showing logs During Model Download/Load and cancel Download/Load Operation
class DownloadLogPopup(QDialog):
    def __init__(self, log_emitter):
        super().__init__()
        self.downloader = None
        self.log_emitter = log_emitter
        self.setWindowTitle("Model Download/Loading Log")
        self.setFixedSize(800, 400)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.layout = QVBoxLayout(self)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)
        self.cancel_button = QPushButton("Cancel Download")
        self.layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.cancel_download)

    def set_downloader(self, downloader):
        self.downloader = downloader

    def Append_Log(self, message):
        if str(message).startswith("Progress"):
            ChangedContent = ""
            lines = self.log_output.toPlainText().splitlines()
            for line in lines:
                if not line.strip().startswith("Progress"):
                    ChangedContent += line + "\n"
            ChangedContent += message
            self.log_output.setText(ChangedContent)
        else:
            self.log_output.append(message)
        QApplication.processEvents()

    def Update_Progress(self, percent):
        self.progress_bar.setValue(percent)
        QApplication.processEvents()

    def cancel_download(self):
        self.downloader.cancel()
        self.Append_Log("Download Cancelled by User!")

    def closeEvent(self, event):
        if self.downloader:
            response = QMessageBox.warning(None,"Warning!","If Download has not completed, it will be aborted!",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if response == QMessageBox.StandardButton.Yes:
                self.cancel_download()
                event.accept()
            elif response == QMessageBox.StandardButton.No:
                event.ignore()

# Downloader for Required Models   
class Downloader(QObject):
    def __init__(self, url: str, filepath: str,modelType: str,imagePath: str ,log_emitter, parent=None):
        super().__init__(parent)
        self.url = QUrl(url)
        self.filepath = filepath
        self.log_emitter = log_emitter
        self.manager = QNetworkAccessManager(self)
        self.start_time = None
        self.reply = None
        self.cancelled = False
        self.modelType = modelType
        self.imagePath = imagePath

    def start(self):
        request = QNetworkRequest(self.url)
        self.reply = self.manager.get(request)
        self.start_time = time.time()
        # Connect signals from QNetworkReply, not QNetworkAccessManager
        self.reply.downloadProgress.connect(self.on_progress)
        self.reply.finished.connect(self.On_Finished)

    def cancel(self):
        self.cancelled = True
        if self.reply:
            self.reply.abort()

    def on_progress(self, downloaded: int, total_size: int):
        if self.cancelled:
            self.log_emitter.finished_signal.emit(False, "Download Cancelled.","","","")
            return

        elapsed = time.time() - self.start_time
        percent = int(downloaded * 100 / total_size) if total_size > 0 else 0
        speed = downloaded / (1024 * 1024) / elapsed if elapsed > 0 else float('inf')
        speed_text = f"{speed:.2f} MB/s" if speed > 1 else f"{speed * 1024:.2f} KB/s"
        time_str = time.strftime("%M:%S", time.gmtime(elapsed))
        bar = '=' * (percent // 5) + '-' * (20 - (percent // 5))
        progress_text = f"Progress: {downloaded}/{total_size} B [{bar}] {time_str} {speed_text}"

        self.log_emitter.progressbar_signal.emit(percent)
        self.log_emitter.log_signal.emit(progress_text)

    def On_Finished(self):
        if self.cancelled:
            self.log_emitter.finished_signal.emit(False, "Download Cancelled.","","","")
            return

        if self.reply.error() != QNetworkReply.NetworkError.NoError:
            self.log_emitter.finished_signal.emit(False, self.reply.errorString(),"","","")
            return

        data = self.reply.readAll().data()
        with open(self.filepath, 'wb') as f:
            f.write(data)
        self.log_emitter.finished_signal.emit(True, "Download Success.", self.modelType, self.filepath, self.imagePath)
