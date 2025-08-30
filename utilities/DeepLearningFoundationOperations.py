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
import random
import requests
from urllib3.exceptions import IncompleteRead
try:
    os.environ["KERAS_BACKEND"] = "tensorflow"  # or "jax", "torch"
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1' # '0' or '1' 1 activate intel speed support
    from keras.applications import VGG16
    from keras.applications import VGG19
    from keras.applications import ResNet50
    from keras.applications import InceptionV3
    from keras.applications import Xception
    from keras.applications.vgg16 import VGG16
    from keras.applications.vgg19 import VGG19
    from keras.applications.resnet50 import ResNet50
    from keras.applications.inception_v3 import InceptionV3
    from keras.applications.xception import Xception
    from keras.applications import imagenet_utils
    from keras.applications.imagenet_utils import preprocess_input
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
    from PyQt6.QtWidgets import QScrollArea,QProgressBar,QMessageBox, QFileDialog, QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton,QWidget,QLabel
except:
    print("You Should Install PyQt6 Library!")
        
class DeepLearningFoundationOperations(QObject):
    def __init__(self,ImagesAndColorsHandler,CreateSimpleCNNHandler,parent=None):
        super().__init__()
        # Internal Variable to Access Images, Videos and Cameras inside All Functions in the Class 
        self.models = {}     
        self.ImagesAndColorsHandler = ImagesAndColorsHandler
        self.CreateSimpleCNNHandler = CreateSimpleCNNHandler
        self.DownloadLogPopup = None
        self._is_running = False
        self.downloadResult = None
        self.log_emitter = LogEmitter()
        self.log_emitter.log_signal.connect(self.Append_Log)       
        self.log_emitter.progressbar_signal.connect(self.Update_Progress)  
        self.log_emitter.finished_signal.connect(self.On_Finished)
        self.LoadModelDetails()
        
    # Consider|Attention: 
    # Process Functions Contains Computer Vision Functions with Comments and Explanations
    # Rest of Functions are Pre-Processor and Helpers
    
    # Processing the Operation on Pre-Trained Model
    def ProcessImage(self,model,imagePath,newSize,processMode):
        # Show Model Architecture in A new Popup
        show_scrollable_message("Model Summary:", self.CreateSimpleCNNHandler.ModelSummaryCapture(model))
        self.log_emitter.log_signal.emit("Do not Close the Log Window.\nWait for Prediction Result:\n")
        # ***If Selected Image not Closed Bring it to the Top***
        # imageName = self.ImagesAndColorsHandler.imageName or self.ImagesAndColorsHandler.tempImageName
        # if imageName is not None:
        #     print(imageName, cv2.getWindowProperty(imageName, cv2.WND_PROP_VISIBLE))
        #     if cv2.getWindowProperty(imageName, cv2.WND_PROP_VISIBLE) >= 1:
        #         cv2.setWindowProperty(imageName, cv2.WND_PROP_TOPMOST, 1)   
               
        # Loading the Image to Predict
        img = load_img(imagePath)          
        # Resize the Image to X * Y Square Shape Required for Specific Pre-Trained Model
        img = img.resize(newSize)
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
        img_array = imagenet_utils.preprocess_input(img_array, mode=processMode)
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
         # Loading the Image to Predict
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
        # Display the Result of Prediction in a Window on Top of Image
        if self.DownloadLogPopup:
           self.log_emitter.log_signal.emit("***********************\nDetection Result\n\nPredicted Object: \t" + str(actual_prediction[0][0][1]).title() + "\nStated Accuracy: \t" + str(actual_prediction[0][0][2]*100) +"\n***********************")
        # Display the Result of Prediction in a Log Window
        msgBox = QMessageBox(parent=None)
        msgBox.setWindowTitle("Detection Result")
        msgBox.setText("Predicted Object: \t" + str(actual_prediction[0][0][1]).title() + "\nStated Accuracy: \t" + str(actual_prediction[0][0][2]*100))
        msgBox.setWindowFlags(msgBox.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        msgBox.exec()
       
    # Processing the Operation on Mobilenet SSD Pre-Trained Model   
    def ProcessMobilenetSSD(self,img_to_detect,mobilenetssd,class_labels):
        # Get width, height of Image 
        img_height , img_width = img_to_detect.shape[0:2]

        # Resize to Match Input Size
        resized_img_to_detect = cv2.resize(img_to_detect,(300,300))

        # Convert to Blob to Pass into Model
        # Recommended Scale Factor is 0.007843, width,height of blob is 300,300, mean of 255 is 127.5
        img_blob = cv2.dnn.blobFromImage(resized_img_to_detect,0.007843,(300,300),127.5)

        # Pass Blob into Model
        mobilenetssd.setInput(img_blob)

        '''
        The mobilenetssd.forward() function is typically used in object detection pipelines involving the MobileNet-SSD model. Here's a breakdown of what it does and how it's used:
        🧠 What forward() Does
        - It performs inference: This method runs a forward pass through the MobileNet-SSD neural network.
        - It returns detection results: These are usually bounding boxes, class labels, and confidence scores for objects detected in the input image.
        
        🛠️ Typical Usage in Python (OpenCV + Caffe)
        net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        
        📦 Output Format
        The detections variable is usually a 4D array with shape [1, 1, N, 7], where:
        - N is the number of detected objects
        - Each detection has 7 values: [image_id, label, confidence, x_min, y_min, x_max, y_max]
        
        🔍 Example Interpretation
        You can loop through the detections like this:
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                # Draw box or label

        If you're using a different framework like PyTorch or TensorFlow, the method and output might vary slightly. Want help adapting this to your specific setup?
        '''
        obj_detections = mobilenetssd.forward()

        # Returned obj_detections[0, 0, index, 1]:
        # 1 => will have the Prediction Class Index
        # 2 => will have Confidence
        # 3 to 7 => will have the Bounding Box Co-Ordinates
        no_of_detections = obj_detections.shape[2]

        # loop over the detections
        for index in np.arange(0, no_of_detections):

            prediction_confidence = obj_detections[0, 0, index, 2]

            # Take only Predictions with Confidence more than 20%
            if prediction_confidence > 0.20:

                # Get the Predicted Label
                predicted_class_index = int(obj_detections[0, 0, index, 1])
                predicted_class_label = class_labels[predicted_class_index]     

                # Obtain the Bounding Box Co-Oridnates for Actual Image from Resized Image Size
                bounding_box = obj_detections[0, 0, index, 3:7] * np.array([img_width, img_height, img_width, img_height])
                (start_x_pt, start_y_pt, end_x_pt, end_y_pt) = bounding_box.astype("int")

                # Create Prediction Label
                predicted_class_label = "{}: {:.2f}%".format(class_labels[predicted_class_index], prediction_confidence * 100)

                # Display the Result of Prediction in Log Window if not Closed
                if self.DownloadLogPopup:    
                   self.log_emitter.log_signal.emit("predicted object {}: {} \t Stated Accuracy: {}".format(index +1 ,class_labels[predicted_class_index], prediction_confidence * 100) )           
                
                # Draw Rectangle Around Detected Object in the Image
                cv2.rectangle(img_to_detect, (start_x_pt, start_y_pt), (end_x_pt, end_y_pt), (0,255,0), 2)
               
                # Put the Result of Prediction as Text on Detected Object in the Image
                cv2.putText(img_to_detect, predicted_class_label, (start_x_pt, start_y_pt-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        
        # Display the Image
        cv2.imshow("Detection Output", img_to_detect)
                
    # Loading Downloaded or Existing Mobilenet SSD Pre-Trained Model
    def PreProcessMobilenetSSD(self,imagePath,filepath,MobileNetSSD_PrototextPath,operationType):
        '''
        The MobileNetSSD Caffe model is a lightweight deep learning model designed for real-time object detection. 
        It combines the efficient MobileNet architecture with the SSD (Single Shot MultiBox Detector) framework,
          making it ideal for deployment on devices with limited computational power like Raspberry Pi or mobile platforms.
        🔍 Key Features
        - MobileNet: Uses depthwise separable convolutions to reduce computation.
        - SSD: Detects objects in a single forward pass, enabling fast inference.
        - Caffe Format: Compatible with the Caffe deep learning framework, often used in embedded systems.
        📦 Common Files
        - MobileNetSSD_deploy.caffemodel: Pre-trained weights.
        - MobileNetSSD_deploy.prototxt: Network architecture definition.
        🛠️ Use Cases
        - Real-time object detection on edge devices.
        - Integration with OpenVINO for Intel hardware acceleration.
        - Robotics, surveillance, and smart cameras.
        '''
        MobileNetSSD_CaffeModel = filepath
        '''
        📄 MobileNetSSD_Prototext
        The MobileNetSSD deploy.prototxt file—sometimes casually referred to as "MobileNetSSD_Prototext" is the architectural script that defines 
        how the MobileNetSSD model operates within the Caffe deep learning framework. It outlines the neural network’s structure, layer by layer, 
        and is essential for pairing with the trained weights (.caffemodel) during inference.
        🔧 Key Components
        - Input Layer: Accepts images, typically sized 300x300x3 (RGB).
        - Depthwise Separable Convolutions: Core of MobileNet's efficiency, reducing computation.
        - BatchNorm & ReLU: Stabilizes and activates the network after each convolution.
        - SSD Detection Layers: Multi-scale feature maps for detecting objects of various sizes.
        - PriorBox Layers: Defines anchor boxes for bounding box predictions.
        - Softmax & DetectionOutput: Final layers that classify objects and output bounding boxes.

        📦 Common Usage
        - Used with MobileNetSSD_deploy.caffemodel for object detection tasks.
        - Compatible with OpenCV's dnn module for fast inference.
        - Can be customized for different input sizes or object classes.

        🛠️ Example Applications
        - Real-time detection on mobile and embedded platforms.
        - Edge AI deployments using OpenVINO or TensorRT.
        - Robotics, smart cameras, and IoT vision systems.
        '''
        # Cleaning MobileNetSSD_Prototext File
        MobileNetSSD_Prototext = self.Clean_MobileNetSSD_Prototext(MobileNetSSD_PrototextPath)
        
        # Loading Pretrained Model from Prototext and Caffemodel files
        mobilenetssd = cv2.dnn.readNetFromCaffe(MobileNetSSD_Prototext, MobileNetSSD_CaffeModel) 
        self.log_emitter.log_signal.emit("Pre-Trained Weight Loaded into the Model successfully.")

         # Set of 21 Class Labels in Alphabetical Order
        class_labels = ["background", "aeroplane", "bicycle", "bird", "boat","bottle", "bus", "car", "cat", "chair", "cow", "diningtable","dog", "horse", "motorbike", "person", "pottedplant", "sheep","sofa", "train", "tvmonitor"]
        
        cv2.destroyAllWindows()
        if self.DownloadLogPopup:
           self.log_emitter.log_signal.emit("***********************\nDetection Results\n")
        img_to_detect = None

        match operationType:
            case "Images":
                # Load the Image to Detect
                img_to_detect = cv2.imread(imagePath)
                self.ProcessMobilenetSSD(img_to_detect,mobilenetssd,class_labels)
                
            case "Pre-Saved":
                # Get the Saved Video File as Stream
                self.ImagesAndColorsHandler.videoCapturer = cv2.VideoCapture(self.ImagesAndColorsHandler.video)

                # Create a While Loop until Video Still Streaming
                while (self.ImagesAndColorsHandler.videoCapturer.isOpened):
                    # Wait for Pressing a Keyboard Key to Exit
                    if cv2.waitKey(1) in range(0,255):
                            self.ImagesAndColorsHandler.videoCapturer.release()
                            break
                    # Get the Current Frame from Video Stream
                    ret,current_frame = self.ImagesAndColorsHandler.videoCapturer.read()
                    # Use Video Current Frame instead of Image
                    if current_frame is not None and len(current_frame.shape) > 1:
                        self.ProcessMobilenetSSD(current_frame,mobilenetssd,class_labels)             

            case "Realtime":
                # Get the Camera Video File as Stream
                self.ImagesAndColorsHandler.videoCapturer = cv2.VideoCapture(self.ImagesAndColorsHandler.camera)

                # Create a While Loop until Camera Still is Open and Video is Streaming
                while True:
                    # Wait for Pressing a Keyboard Key to Exit
                    if cv2.waitKey(1) in range(0,255):
                            self.ImagesAndColorsHandler.videoCapturer.release()
                            break
                    # Get the Current Frame from Camera Video Stream
                    ret,current_frame = self.ImagesAndColorsHandler.videoCapturer.read()
                    # Use Video Current Frame instead of Image
                    if current_frame is not None and len(current_frame.shape) > 1:
                        self.ProcessMobilenetSSD(current_frame,mobilenetssd,class_labels)
                          
        if self.DownloadLogPopup:            
            self.log_emitter.log_signal.emit("\n***********************")
            
    # Loading Downloaded or Existing Pre-Trained Model
    def Loading_Model_Operation(self,modelType, filepath, imagePath, operationType):
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
                    # Creating an empty VGGNet16 Model
                    model = VGG16(weights=None)
                    # Loding Pre-Trained Weights into the Model
                    model.load_weights(filepath)
                    self.log_emitter.log_signal.emit("Pre-Trained Weight Loaded into the Model successfully.")
                    # Resize the Image to 224x224 Square Shape
                    newSize = (224,224)
                    # Mode of Processing the Image in Keras
                    processMode = "caffe"
                    self.ProcessImage(model,imagePath,newSize,processMode)
                    
                case "VGGNet19":
                    # This is a command for Download/Load with Tracing only in Console Not UI
                    # model = VGG19(weights="imagenet") 

                    # Creating an empty VGGNet19 Model
                    model = VGG19(weights=None)
                    # Loding Pre-Trained Weights into the Model
                    model.load_weights(filepath)
                    self.log_emitter.log_signal.emit("Pre-Trained Weight Loaded into the Model successfully.")
                    # Resize the Image to 224x224 Square Shape
                    newSize = (224,224)
                    # Mode of Processing the Image in Keras
                    processMode = "caffe"
                    self.ProcessImage(model,imagePath,newSize,processMode)

                case "ResNet50":
                    # This is a command for Download/Load with Tracing only in Console Not UI
                    # model = ResNet50(weights="imagenet") 

                    # Creating an empty ResNet50 Model
                    model = ResNet50(weights=None)
                    # Loding Pre-Trained Weights into the Model
                    model.load_weights(filepath)
                    self.log_emitter.log_signal.emit("Pre-Trained Weight Loaded into the Model successfully.")
                    # Resize the Image to 224x224 Square Shape
                    newSize = (224,224)
                    # Mode of Processing the Image in Keras
                    processMode = "caffe"
                    self.ProcessImage(model,imagePath,newSize,processMode)

                case "Inception_v3":
                    # This is a command for Download/Load with Tracing only in Console Not UI
                    # model = InceptionV3(weights="imagenet") 

                    # Creating an empty Inception_v3 Model
                    model = InceptionV3(weights=None)
                    # Loding Pre-Trained Weights into the Model
                    model.load_weights(filepath)
                    self.log_emitter.log_signal.emit("Pre-Trained Weight Loaded into the Model successfully.")
                    # Resize the Image to 299x299 Square Shape
                    newSize = (299,299)
                    # Mode of Processing the Image in Keras
                    processMode = "tf"
                    self.ProcessImage(model,imagePath,newSize,processMode)
 
                case "Xception":
                    # This is a command for Download/Load with Tracing only in Console Not UI
                    # model = Xception(weights="imagenet") 

                    # Creating an empty Xception Model
                    model = Xception(weights=None)
                    # Loding Pre-Trained Weights into the Model
                    model.load_weights(filepath)
                    self.log_emitter.log_signal.emit("Pre-Trained Weight Loaded into the Model successfully.")
                    # Resize the Image to 299x299 Square Shape
                    newSize = (299,299)
                    # Mode of Processing the Image in Keras
                    processMode = "tf"
                    self.ProcessImage(model,imagePath,newSize,processMode)

                case "MobilenetSSD":      
                    # Check/Download required MobilenetSSD.prototxt File              
                    folder = os.path.normpath(join("resources","models"))
                    MobileNetSSD_Prototext_fileName = "MobilenetSSD.prototxt"
                    MobileNetSSD_PrototextPath = os.path.join(folder, MobileNetSSD_Prototext_fileName)
                    if not os.path.exists(MobileNetSSD_PrototextPath):
                       modelType = "MobileNetSSDPrototxt"
                       self.PreProcessImage(imagePath, modelType, operationType)
                    else:
                        self.PreProcessMobilenetSSD(imagePath,filepath,MobileNetSSD_PrototextPath,operationType)  

    # Check, Validation for Downloading Pre-Trained Model                
    def PreProcessImage(self, imagePath,modelType,operationType):
        ConditionToCheck = None
        ContentMessage = None
        TitleMessage = None
        match operationType:
            case "Images":
                ConditionToCheck = self.ImagesAndColorsHandler.image is not None and self.ImagesAndColorsHandler.imageName is not None
                ContentMessage = "First, Select an Image!"
                TitleMessage = "No Image Selected" 
                
            case "Pre-Saved":
                ConditionToCheck = self.ImagesAndColorsHandler.video is not None and self.ImagesAndColorsHandler.Check_Camera_Availability(self.ImagesAndColorsHandler.video)
                ContentMessage = "First, Select a Video!" 
                TitleMessage = "No Video Selected"

            case "Realtime":
                ConditionToCheck = self.ImagesAndColorsHandler.camera is not None and self.ImagesAndColorsHandler.Check_Camera_Availability(self.ImagesAndColorsHandler.camera)
                ContentMessage = "First, Select a Camera!" 
                TitleMessage = "No Camera Selected"

        if ConditionToCheck:              
            if self.DownloadLogPopup == None or not self.DownloadLogPopup:
                self.DownloadLogPopup = DownloadLogPopup(self.log_emitter)   
                self.DownloadLogPopup.show()
            self._is_running = True     
            # Get Model Info
            if len(self.models) > 0 and self.models.get(modelType): 
                self.log_emitter.log_signal.emit("Checking for existing model file...")
                url =  self.models[modelType]["url"] 
                filename = self.models[modelType]["name"] 
                fileSize = self.models[modelType]["size"] 
                expected_hash = self.models[modelType]["md5hash"] 
                expected_size = fileSize
                folder = os.path.normpath(join("resources","models"))
                filepath = os.path.join(folder, filename)
                if os.path.exists(filepath):
                   self.log_emitter.log_signal.emit(str(self.models[modelType]["name"]) + "\nModel file found locally\n Hash and Size are not Validated!\nLoading from cache...") 
                else:
                    self.log_emitter.log_signal.emit(str(self.models[modelType]["name"]) + 
                                                        "\nModel file not found. \nDownloading from internet...\n" + 
                                                        "Make Sure your System Connected to the Internet\n"+
                                                        "File is Approximately "+fileSize+"\n"+
                                                        "It takes a while Depending on the Speed of your System and Internet!")
                    
                    self.log_emitter.log_signal.emit("Download Url: \n" + str(self.models[modelType]["url"]))   

                # Only Download if File is Missing 
                if not os.path.exists(filepath):   
                    self.downloader = Downloader(url, filepath, modelType,imagePath,self.log_emitter, fileSize,operationType)
                    self.DownloadLogPopup.Set_Downloader(self.downloader)
                    self.downloader.Start()   
                    
                else:
                    # You can Remove below line and run File_Size_and_Hash_Validation in if Statement for Validation
                    self.File_Size_and_Hash_Validation("md5",filepath, expected_size,expected_hash,self.log_emitter,True)  

                    self.Loading_Model_Operation(modelType, filepath,imagePath,operationType)
            
            else:
                self.log_emitter.log_signal.emit("Error: 'models.json' not found or Not Contains Details for this Operation ( "+modelType+" ).\nPlease ensure the file exists in the root and contains Details for this Operation ( "+modelType+" ).")

        else:
            QMessageBox.warning(None, TitleMessage,ContentMessage)

    # Selecting Desired Operation
    def SelectDeepLearningOperations(self,operation,imagePath):
        self.DownloadLogPopup = None
        modelTypeString = operation.strip().split(" ")
        match operation.strip():
            case "Image Recognition using Pre-Trained VGGNet16 Model":
                modelType = modelTypeString[4]
                self.PreProcessImage(imagePath, modelType,None)

            case "Image Recognition using Pre-Trained VGGNet19 Model":
                modelType = modelTypeString[4]
                self.PreProcessImage(imagePath, modelType,None)
    
            case "Image Recognition using Pre-Trained ResNet50 Model":
                modelType = modelTypeString[4]
                self.PreProcessImage(imagePath, modelType,None)

            case "Image Recognition using Pre-Trained Inception_v3 Model":
                modelType = modelTypeString[4]
                self.PreProcessImage(imagePath, modelType,None)

            case "Image Recognition using Pre-Trained Xception Model":
                modelType = modelTypeString[4]
                self.PreProcessImage(imagePath, modelType,None)

            case "Object Detection by Pre-Trained Mobilenet SSD Model on Images":
                modelType = modelTypeString[4] + modelTypeString[5]
                operationType = modelTypeString[8]
                self.PreProcessImage(imagePath, modelType, operationType)

            case "Object Detection by Pre-Trained Mobilenet SSD Model on Pre-Saved Video":
                modelType = modelTypeString[4] + modelTypeString[5]
                operationType = modelTypeString[8]
                self.PreProcessImage(imagePath, modelType, operationType)

            case "Object Detection by Pre-Trained Mobilenet SSD Model on Realtime Video":
                modelType = modelTypeString[4] + modelTypeString[5]
                operationType = modelTypeString[8]
                self.PreProcessImage(imagePath, modelType, operationType)

            case "Object Mask Implementation by Pre-Trained MaskRCNN Model on Images":
                print(operation)
            case "Bounding Box Implementation by Pre-Trained MaskRCNN Model on Images":
                print(operation)
            case "Object Detection by Pre-Trained MaskRCNN Model on Pre-Saved Video":
                print(operation)
            case "Object Detection by Pre-Trained MaskRCNN Model on Realtime Video":
                print(operation)
            case "Object Detection by Pre-Trained Tiny YOLO Model on Images":
                print(operation)
            case "Object Detection by Pre-Trained Tiny YOLO Model on Pre-Saved Video":
                print(operation)
            case "Object Detection by Pre-Trained Tiny YOLO Model on Realtime Video":
                print(operation)
            case "Object Detection by Pre-Trained YOLO Model on Images":
                print(operation)
            case "Object Detection by Pre-Trained Optimized YOLO Model on Images":
                print(operation)
            case "Object Detection by Pre-Trained YOLO Model on Pre-Saved Video":
                print(operation)
            case "Object Detection by Pre-Trained Optimized YOLO Model on Pre-Saved Video":
                print(operation)
            case "Object Detection by Pre-Trained YOLO Model on Realtime Video":
                print(operation)
            case "Object Detection by Pre-Trained Optimized YOLO Model on Realtime Video":
                print(operation)

        self.ImagesAndColorsHandler.WaitKeyCloseWindows()       

    # Selecting Active Camera
    def SelectDeepLearningCamera(self,text):
        if text.strip() != "":
           self.ImagesAndColorsHandler.camera = int((text.split(",")[0]).split(":")[1].strip())
    
    # Updating Logs After Download Finished
    def On_Finished(self, success, info ,modelType,filepath, imagePath,operationType):
        if not success:
            log = "Download Failed.\n" + str(info)
            if not "Download Cancelled" in str(info):
                log += "\nCheck Internet Connectivity!"
            
            self.DownloadLogPopup.Append_Log(log)
            return
                                
        else:
            self.DownloadLogPopup.Append_Log(str(info)+"\nDownload Complete.")   
            self.Loading_Model_Operation(modelType, filepath, imagePath,operationType)              

    # Updating ProgressBar
    def Update_Progress(self, percent):
        if self._is_running:
           self.DownloadLogPopup.Update_Progress(percent)

    # Updating Logs
    def Append_Log(self,message):
        if self._is_running:
            self.DownloadLogPopup.Append_Log(message)

    # Validating Hash of Files
    def File_Size_and_Hash_Validation(self,type,path,expected_size, expected_hash,log_emitter,check):
        """Check if the file's SHA256 or MD5 hash matches the expected value."""
        if os.path.exists(path):
            fileSize = os.path.getsize(path) or os.stat(path).st_size
            expected_size = int(expected_size.split(" ")[0]) * (1024*1024)
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
                                    log_emitter.log_signal.emit("File Hash: " + str(actual_hash))
                                    log_emitter.log_signal.emit("Expected Size: " + str(expected_size) + "B")
                                    log_emitter.log_signal.emit("File Size: " + str(fileSize) + "B")
                        return str(actual_hash).lower() == str(expected_hash).lower() and fileSize == expected_size
                    except Exception as e:
                        log_emitter.log_signal.emit("Error:", str(e))
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
                            log_emitter.log_signal.emit("File Hash: " + str(actual_hash))
                            log_emitter.log_signal.emit("Expected Size: " + str(expected_size) + "B")
                            log_emitter.log_signal.emit("File Size: " + str(fileSize) + "B")
                        return str(actual_hash).lower() == str(expected_hash).lower() and fileSize == expected_size
                    except Exception as e:
                        log_emitter.log_signal.emit("Error:", str(e))
                        return False

    # Loading Model Details from models.json file in the Root
    def LoadModelDetails(self):
        if len(self.models) <= 0:    
            try:
                with open('models.json', 'r') as f:
                    self.models = json.load(f)
            except FileNotFoundError:
                self.log_emitter.log_signal.emit("Error: 'models.json' not found.\nPlease ensure the file exists in the root.")
            except json.JSONDecodeError:
                self.log_emitter.log_signal.emit("Error: Could not decode JSON from 'models.json'.\nCheck the file's format.")
        
    # Cleaning Downloaded MobileNetSSD Prototext file
    def Clean_MobileNetSSD_Prototext(self,path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip empty lines and HTML tags
            if stripped and not stripped.startswith("<") and not stripped.endswith(">"):
                cleaned_lines.append(stripped)

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(cleaned_lines))

        self.log_emitter.log_signal.emit(f"Cleaned MobileNetSSD Prototext file in: {path}")
        return path
   
# Signal emitter for Thread-Safe logging
class LogEmitter(QObject):
    log_signal = pyqtSignal(str) # All Communications, Updates and Text Messages
    progressbar_signal = pyqtSignal(int) #  Percent: ProgressBar Update
    finished_signal = pyqtSignal(bool, str, str , str, str, str) # success ,message info [error, Cancle, success, fail] ,modelType , filepath, imagePath, operationType

# Dialog for showing logs During Model Download/Load and Cancle Download/Load Operation
class DownloadLogPopup(QDialog):
    def __init__(self, log_emitter):
        super().__init__()
        self.downloader = None
        self.log_emitter = log_emitter
        self.setWindowTitle("Model Download/Loading Log")
        self.setFixedSize(800, 400)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        # Create a scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: transparent;
            }
        """)
        # Create a container widget for the scroll area
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Add QTextEdits to the layout
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)
        self.cancel_button = QPushButton("Cancel Download")
        self.layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.Cancel_Download)
         # Set the container as the scroll area's widget
        self.scroll_area.setWidget(container)
        # Final layout for the dialog
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)

    def Set_Downloader(self, downloader):
        self.downloader = downloader

    def Append_Log(self, message):
        if str(message).startswith("Progress") and not "[====================]" in message and not "Download Complete" in message:
            ChangedContent = ""
            lines = self.log_output.toPlainText().splitlines()
            for line in lines:
                if not line.strip().startswith("Progress"):
                    ChangedContent += line + "\n"
            ChangedContent += message
            self.log_output.setText(ChangedContent)
        else:
            self.log_output.append(message)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().minimum()) 
        QApplication.processEvents()  

    def Update_Progress(self, percent):
        self.progress_bar.setValue(percent)
        QApplication.processEvents()

    def Cancel_Download(self):
        if self.downloader:
            self.downloader.Cancle()
            self.Append_Log("Download Cancelled by User!")

    def closeEvent(self, event):
        log = self.log_output.toPlainText()
        if self.downloader and not "Download Success" in log and not "Download Complete" in log and not "Download Cancelled" in log  and not "Download Failed" in log:
            response = QMessageBox.warning(None,"Warning!","If Download has not completed, it will be aborted!",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if response == QMessageBox.StandardButton.Yes:
                self.Cancel_Download()
                event.accept()
            elif response == QMessageBox.StandardButton.No:
                event.ignore()

# Downloader for Required Models   
class Downloader(QObject):
    def __init__(self, url: str, filepath: str,modelType: str,imagePath: str ,log_emitter,fileSize: str,operationType: str, parent=None):
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
        self.fileSize = fileSize
        self.operationType = operationType
        self.fallback_attempts = 0
        self.max_fallback_attempts = 3
        self.user_agents = [
            # Windows
            b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            
            # macOS
            b"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            
            # Linux
            b"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            
            # Android
            b"Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36",
            
            # iOS
            b"Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/134.0.0.0 Mobile/15E148 Safari/604.1",
            
            # Chrome on iPad
            b"Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/134.0.0.0 Mobile/15E148 Safari/604.1",
            
            # Chrome on Chromebook
            b"Mozilla/5.0 (X11; CrOS x86_64 14526.83.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        ]
    
    def Start(self):
        request = QNetworkRequest(self.url)
        random_user_agent = random.choice(self.user_agents)
        #
        #request.setRawHeader(b"User-Agent", b"MyDownloader/1.0")
        request.setRawHeader(b"User-Agent", random_user_agent)
        self.reply = self.manager.get(request)
        #
        self.reply.sslErrors.connect(lambda errors: self.reply.ignoreSslErrors())
        self.start_time = time.time()
        # Connect signals from QNetworkReply, not QNetworkAccessManager
        self.reply.downloadProgress.connect(self.On_Progress)
        self.reply.finished.connect(self.On_Finished)

    def Cancle(self):
        self.cancelled = True
        if self.reply:
            self.reply.abort()

    def On_Progress(self, downloaded: int, total_size: int):
        if self.cancelled:
            self.log_emitter.finished_signal.emit(False, "Download Cancelled.","","","",self.operationType)
            return

        elapsed = time.time() - self.start_time
        percent = int(downloaded * 100 / total_size) if total_size > 0 else 0
        speed = downloaded / (1024 * 1024) / elapsed if elapsed > 0 else float('inf')
        speed_text = f"{speed:.2f} MB/s" if speed > 1 else f"{speed * 1024:.2f} KB/s"
        time_str = time.strftime("%M:%S", time.gmtime(elapsed))
        bar = '=' * (percent // 5) + '-' * (20 - (percent // 5))
        progress_text = f"Progress: {downloaded} B from {total_size} B [{bar}] {time_str} {speed_text}"

        self.log_emitter.progressbar_signal.emit(percent)
        self.log_emitter.log_signal.emit(progress_text)

    def On_Finished(self):
        if self.cancelled:
            self.log_emitter.finished_signal.emit(False, "Download Cancelled.","","","",self.operationType)
            return

        if self.reply.error() != QNetworkReply.NetworkError.NoError:
            self.log_emitter.finished_signal.emit(False, self.reply.errorString(),"","","",self.operationType)
            # Fallback to requests with streaming
            self.Fallback_Download()
            return

        data = self.reply.readAll().data()
        with open(self.filepath, 'wb') as f:
            f.write(data)
       
        # validate file size with 10 mb telorance
        actual_size = os.path.getsize(self.filepath)
        expected_size = int(self.fileSize.split(" ")[0]) -10 * (1024*1024)
        if self.modelType == "MobilenetSSD":
            expected_size = int(self.fileSize.split(" ")[0]) -10 * (1024)
        if actual_size < expected_size:  # reject files smaller than fileSize
            self.log_emitter.log_signal.emit(
                f"Downloaded file too small ({actual_size} < {expected_size}). Attempt {self.fallback_attempts + 1}/{self.max_fallback_attempts}"
            )
            os.remove(self.filepath)
            self.fallback_attempts += 1

            if self.fallback_attempts < self.max_fallback_attempts:
                self.Fallback_Download()

            else:
                self.log_emitter.finished_signal.emit(False, "Download failed after multiple fallback attempts.", "", "", "",self.operationType)

            return

        self.log_emitter.finished_signal.emit(True, "Download Success.", self.modelType, self.filepath, self.imagePath,self.operationType)
        return

    def Fallback_Download(self):
        headers = { "User-Agent": random.choice(self.user_agents).decode("utf-8") }
        while self.fallback_attempts < self.max_fallback_attempts:
            self.fallback_attempts += 1
            self.log_emitter.log_signal.emit(f"Fallback attempt {self.fallback_attempts}/{self.max_fallback_attempts}")
            try:
                with requests.get(self.url.toString(), headers=headers, stream=True, timeout=60) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get("Content-Length", 0))
                    downloaded = 0
                    start_time = time.time()
                    with open(self.filepath, "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if self.cancelled:
                                self.log_emitter.finished_signal.emit(False, "Download Cancelled.", "", "", "",self.operationType)
                                return
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)

                                percent = int(downloaded * 100 / total_size) if total_size else 0
                                elapsed = time.time() - start_time
                                speed = downloaded / (1024 * 1024) / elapsed if elapsed > 0 else float('inf')
                                speed_text = f"{speed:.2f} MB/s" if speed > 1 else f"{speed * 1024:.2f} KB/s"
                                time_str = time.strftime("%M:%S", time.gmtime(elapsed))
                                bar = '=' * (percent // 5) + '-' * (20 - (percent // 5))
                                progress_text = f"Progress: {downloaded} B from {total_size} B [{bar}] {time_str} {speed_text}"

                                self.log_emitter.progressbar_signal.emit(percent)
                                self.log_emitter.log_signal.emit(progress_text)

                # validate file size with 10 mb telorance
                actual_size = os.path.getsize(self.filepath)
                expected_size = int(self.fileSize.split(" ")[0]) -10  * (1024 * 1024)
                if self.modelType == "MobilenetSSD":
                   expected_size = int(self.fileSize.split(" ")[0]) -10 * (1024)
                if actual_size < expected_size:
                    self.log_emitter.log_signal.emit(
                        f"Fallback file too small ({actual_size} < {expected_size}). Retrying..."
                    )
                    os.remove(self.filepath)
                    time.sleep(2)
                    continue  # retry

                # Success
                self.log_emitter.finished_signal.emit(True, "Download Success (via fallback).", self.modelType, self.filepath, self.imagePath,self.operationType)
                return

            except Exception as e:
                self.log_emitter.log_signal.emit(f"Fallback error:\n {str(e)}. Retrying...")
                if os.path.exists(self.filepath):
                    os.remove(self.filepath)
                time.sleep(2)
                continue  # retry

        # Final failure after all retries
        self.log_emitter.finished_signal.emit(False, "Download failed after multiple fallback attempts.", "", "", "",self.operationType)
        return