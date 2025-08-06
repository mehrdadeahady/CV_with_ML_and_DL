# Import Essential Libraries
import cv2 # Import Main Computer Vision Library in Python
import numpy as np
import os
from os import path, listdir
from os.path import isfile, join
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QFileDialog

class ImagesAndColors(QObject):
    valueChanged = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__()
        # Internal Variable to Access Image inside All Functions in the Class 
        self.image = None
        self.imageName = None
        self.imageConversion = None

    # Wait for Clicking a Key on Keyboard to Close All cv2 Windows
    def WaitKeyCloseWindows(self):
        # Wait until Clicking a Key on Keyboard
        cv2.waitKey(0)
        # Close All cv2 Windows
        cv2.destroyAllWindows()

    # Reading and Showing an Image from the Path
    def ReadShowImage(self,ImageName):
        cv2.destroyAllWindows()
        self.image = None
        self.imageName = None
        self.imageConversion = None
        path = "resources/images/" + ImageName
        # Check if the path exist and it is a file
        if isfile(path): 
                 # imread is Reading Image Function in OpenCV that takes 1 parameter = Path to Image            
                 self.image = cv2.imread(path)
                 self.imageName = ImageName
                 self.valueChanged.emit("")
                 # imshow is Displaying Image Function in OpenCV that takes 2 parameter:
                 # cv2.imshow(Parameter1 = Desired Name for Image, Parameter2 = Image has obtained from imread Function )
                 cv2.imshow(self.imageName,self.image)
                 self.WaitKeyCloseWindows()

    # Conversion of Color Channels to each other
    def ConvertColorSpace(self,text):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
           if text.strip() != "":
               ConvertedImage = None
               ImageNameTemp = ""
               RightImageConversion = None
               LeftImageConversion = None
               if self.imageConversion is None:
                     ImageNameTemp = self.imageName
                     RightImageConversion = text.strip().split(" ")[0]
                     LeftImageConversion = text.strip()[:3]
               else:
                     ImageNameTemp = self.imageName.split("_")[1]
                     RightImageConversion = self.imageConversion.split("2")[1]
                     LeftImageConversion = self.imageConversion.split("2")[0]
               # cvtColor is Conversion Function in OpenCV that takes 2 Parameters:
               # cv2.cvtColor(Parameter1 = Image, Parameter2 = Requested Conversion ) 
               match text.strip(): 
                   case "BGR Channel to Gray Scale Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Already Gray:", "Conversion not required. Already Image is Gray!")
                           pass
                        elif RightImageConversion != "BGR":
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be BGR!") 
                           pass                        
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "BGR2GRAY"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
                              self.image = ConvertedImage
                              self.imageName = "GRAY_" + ImageNameTemp
                              self.valueChanged.emit("BGR2GRAY")
                              cv2.imshow(self.imageName, ConvertedImage)
                              self.WaitKeyCloseWindows()

                   case "BGR Channel to RGB Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "BGR":
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be BGR!")
                           pass  
                        else:
                             cv2.destroyAllWindows()
                             self.imageConversion = "BGR2RGB"
                             ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
                             self.image = ConvertedImage
                             self.imageName = "RGB_" + ImageNameTemp
                             self.valueChanged.emit("BGR2RGB")
                             cv2.imshow(self.imageName,ConvertedImage)                          
                             self.WaitKeyCloseWindows()
                             
                   case "BGR Channel to HSV Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "BGR":
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be BGR!")  
                           pass
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "BGR2HSV"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
                              self.image = ConvertedImage
                              self.imageName = "HSV_" + ImageNameTemp
                              self.valueChanged.emit("BGR2HSV")
                              cv2.imshow(self.imageName,ConvertedImage)                         
                              self.WaitKeyCloseWindows()

                   case "RGB Channel to Gray Scale Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Already Gray:", "Conversion not required. Already Image is Gray!")
                           pass
                        elif RightImageConversion != "RGB" or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be RGB!")  
                           pass
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "RGB2GRAY"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_RGB2GRAY)
                              self.image = ConvertedImage
                              self.imageName = "GRAY_" + ImageNameTemp
                              self.valueChanged.emit("RGB2GRAY")
                              cv2.imshow(self.imageName,ConvertedImage)                          
                              self.WaitKeyCloseWindows()

                   case "RGB Channel to BGR Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "RGB"  or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be RGB!")
                           pass  
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "RGB2BGR"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_RGB2BGR)
                              self.image = ConvertedImage
                              self.imageName = "BGR_" + ImageNameTemp
                              self.valueChanged.emit("RGB2BGR")
                              cv2.imshow(self.imageName,ConvertedImage)                             
                              self.WaitKeyCloseWindows()

                   case "RGB Channel to HSV Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "RGB"  or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be RGB!") 
                           pass 
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "RGB2HSV"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_RGB2HSV)
                              self.image = ConvertedImage
                              self.imageName = "HSV_" + ImageNameTemp
                              self.valueChanged.emit("RGB2HSV")
                              cv2.imshow(self.imageName,ConvertedImage)
                              self.WaitKeyCloseWindows()

                   case "HSV Channel to BGR Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "HSV"  or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be HSV!")  
                           pass
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "HSV2BGR"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_HSV2BGR)
                              self.image = ConvertedImage
                              self.imageName = "BGR_" + ImageNameTemp
                              self.valueChanged.emit("HSV2BGR")
                              cv2.imshow(self.imageName,ConvertedImage)
                              self.WaitKeyCloseWindows()

                   case "HSV Channel to RGB Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "HSV"  or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be HSV!")
                           pass  
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "HSV2RGB"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_HSV2RGB)
                              self.image = ConvertedImage
                              self.imageName = "RGB_" + ImageNameTemp
                              self.valueChanged.emit("HSV2RGB")
                              cv2.imshow(self.imageName,ConvertedImage) 
                              self.WaitKeyCloseWindows()
                                                                   
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

    # Saving the Image
    def SaveImage(self):
        if self.image is not None and self.imageName is not None: 
           file_path, _ = QFileDialog.getSaveFileName(None, "Save File", self.imageName)
           if file_path:
               # imwrite is Saving Image Function in OpenCV that takes 2 parameter
               # cv2.imwrite(Parameter1 = Name of Image, Parameter2 = Path to Image ) 
               cv2.imwrite(file_path,self.image)
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
        
    #   Activate or Deactivate Color Channels   
    def ColorChannelSelection(self,channels):
        print(channels)
        if self.image is not None and self.imageName is not None:
          cv2.destroyAllWindows()
          # Assume all channels are None by Default then check the Conversion
          B, G, R, H, S, V = None, None, None, None, None, None
          # Let's create a matrix of zeros with dimensions of the image h x w  
          # Zeros are for removing a channel from Image
          zeros = np.zeros(self.image.shape[:2], dtype = "uint8")
          if self.imageConversion is not None:
               # merge is a Function in OpenCV for Creating Image from Desired Selected Channels
               # merge takes 1 Parameter type of Array containing Desired Selected Channels:
               # channel = [R,G,B] or channel = [B,G,R] or channel = [H,S,V] or or channel = [B,zeros,R]
               # Order of Channels inside Channel Array is important
               # cv2.merge(channel) 
               # Existed Channels based on the Image Conversion
               match self.imageConversion:
                     case "BGR2GRAY"|"RGB2GRAY":
                           QMessageBox.warning(None, "No Channels", "There is no channel in Gray Scale Image!")
                           pass
                     case "BGR2RGB"|"HSV2RGB":
                           R, G, B = cv2.split(self.image)
                           ImageNameTemp = "_" + self.imageName.split("_")[1]  if "_" in self.imageName else "_" + self.imageName
                           channel = []
                           if channels["RedChannel"]: 
                              ImageNameTemp = "R" + ImageNameTemp
                              channel.append(R)
                           else: channel.append(zeros)
                           if channels["GreenChannel"]: 
                              ImageNameTemp = "G" + ImageNameTemp
                              channel.append(G)
                           else: channel.append(zeros)                          
                           if channels["BlueChannel"]: 
                              ImageNameTemp = "B" + ImageNameTemp
                              channel.append(B)
                           else: channel.append(zeros) 

                           self.image = cv2.merge(channel)
                           self.imageName = ImageNameTemp
                           cv2.imshow(self.imageName,self.image)
                           self.WaitKeyCloseWindows()

                     case "BGR2HSV"|"RGB2HSV":
                           H, S, V = cv2.split(self.image)
                           ImageNameTemp = "_" + self.imageName.split("_")[1]  if "_" in self.imageName else "_" + self.imageName
                           channel = []
                           if channels["HSVHueChannel"]: 
                              ImageNameTemp = "H" + ImageNameTemp
                              channel.append(H)
                           else: channel.append(zeros)
                           if channels["HSVSaturation"]: 
                              ImageNameTemp = "S" + ImageNameTemp
                              channel.append(S)
                           else: channel.append(zeros)                          
                           if channels["HSVValue"]: 
                              ImageNameTemp = "V" + ImageNameTemp
                              channel.append(V)
                           else: channel.append(zeros) 

                           self.image = cv2.merge(channel)
                           self.imageName = ImageNameTemp
                           cv2.imshow(self.imageName,self.image)
                           self.WaitKeyCloseWindows()

                     case "RGB2BGR"|"HSV2BGR":
                           B, G, R = cv2.split(self.image)
                           ImageNameTemp = "_" + self.imageName.split("_")[1]  if "_" in self.imageName else "_" + self.imageName
                           channel = []
                           if channels["BlueChannel"]: 
                              ImageNameTemp = "B" + ImageNameTemp
                              channel.append(B)
                           else: channel.append(zeros) 
                           if channels["GreenChannel"]: 
                              ImageNameTemp = "G" + ImageNameTemp
                              channel.append(G)
                           else: channel.append(zeros)
                           if channels["RedChannel"]: 
                              ImageNameTemp = "R" + ImageNameTemp
                              channel.append(R)
                           else: channel.append(zeros)

                           self.image = cv2.merge(channel)
                           self.imageName = ImageNameTemp
                           cv2.imshow(self.imageName,self.image)
                           self.WaitKeyCloseWindows()
                    
          else:
               # If Image not Converted then Default Channel is BGR
               B, G, R = cv2.split(self.image)
               ImageNameTemp = "_" + self.imageName.split("_")[1]  if "_" in self.imageName else "_" + self.imageName
               channel = []
               if channels["BlueChannel"]: 
                   ImageNameTemp = "B" + ImageNameTemp
                   channel.append(B)
               else: channel.append(zeros) 
               if channels["GreenChannel"]: 
                   ImageNameTemp = "G" + ImageNameTemp
                   channel.append(G)
               else: channel.append(zeros)
               if channels["RedChannel"]: 
                   ImageNameTemp = "R" + ImageNameTemp
                   channel.append(R)
               else: channel.append(zeros)

               self.image = cv2.merge(channel)
               self.imageName = ImageNameTemp
               cv2.imshow(self.imageName,self.image)
               self.WaitKeyCloseWindows()

                           
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

