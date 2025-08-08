# Import Essential Libraries
import time
import cv2 # Import Main Computer Vision Library in Python
import numpy as np
import os
from os import path, listdir
from os.path import isfile, join
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QFileDialog

class ImagesAndColors(QObject):
    ResetParams = pyqtSignal(int)
    valueChanged = pyqtSignal(str)
    ImageSizeChanged = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__()
        # Internal Variable to Access Image inside All Functions in the Class 
        self.image = None
        self.imageName = None
        self.imageConversion = None
        self.tempImage = None

    # Wait for Clicking a Key on Keyboard to Close All cv2 Windows
    def WaitKeyCloseWindows(self):
        # Wait until Clicking a Key on Keyboard
        cv2.waitKey(0)
        # Close All cv2 Windows
        cv2.destroyAllWindows()
        self.tempImage = None
        self.ResetParams.emit(0)
        if cv2.getWindowProperty(self.imageName, cv2.WND_PROP_VISIBLE) == -1:
           self.ResetParams.emit(0)
           self.tempImage = None

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
               RightImageConversion = None
               if self.imageConversion is None:
                     RightImageConversion = text.strip().split(" ")[0]
               else:
                     RightImageConversion = self.imageConversion.split("2")[1]
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
                              self.imageName = "GRAY_" + self.imageName
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
                             self.imageName = "RGB_" + self.imageName
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
                              self.imageName = "HSV_" + self.imageName
                              self.valueChanged.emit("BGR2HSV")
                              cv2.imshow(self.imageName,ConvertedImage)                         
                              self.WaitKeyCloseWindows()

                   case "RGB Channel to Gray Scale Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Already Gray:", "Conversion not required. Already Image is Gray!")
                           pass
                        elif RightImageConversion != "RGB": #or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be RGB!")  
                           pass
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "RGB2GRAY"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_RGB2GRAY)
                              self.image = ConvertedImage
                              self.imageName = "GRAY_" + self.imageName
                              self.valueChanged.emit("RGB2GRAY")
                              cv2.imshow(self.imageName,ConvertedImage)                          
                              self.WaitKeyCloseWindows()

                   case "RGB Channel to BGR Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "RGB":  #or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be RGB!")
                           pass  
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "RGB2BGR"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_RGB2BGR)
                              self.image = ConvertedImage
                              self.imageName = "BGR_" + self.imageName
                              self.valueChanged.emit("RGB2BGR")
                              cv2.imshow(self.imageName,ConvertedImage)                             
                              self.WaitKeyCloseWindows()

                   case "RGB Channel to HSV Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "RGB":  #or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be RGB!") 
                           pass 
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "RGB2HSV"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_RGB2HSV)
                              self.image = ConvertedImage
                              self.imageName = "HSV_" + self.imageName
                              self.valueChanged.emit("RGB2HSV")
                              cv2.imshow(self.imageName,ConvertedImage)
                              self.WaitKeyCloseWindows()

                   case "HSV Channel to BGR Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "HSV":  #or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be HSV!")  
                           pass
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "HSV2BGR"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_HSV2BGR)
                              self.image = ConvertedImage
                              self.imageName = "BGR_" + self.imageName
                              self.valueChanged.emit("HSV2BGR")
                              cv2.imshow(self.imageName,ConvertedImage)
                              self.WaitKeyCloseWindows()

                   case "HSV Channel to RGB Channel":
                        if RightImageConversion == "GRAY":
                           QMessageBox.warning(None, "Color Channel is Empty:", "Can't Convert Gray Scale Image to Colored Image!")
                           pass
                        elif RightImageConversion != "HSV":  #or self.imageConversion is None:
                           QMessageBox.warning(None, "Color Channels are not Same:", "For this Conversion Current Image must be HSV!")
                           pass  
                        else:
                              cv2.destroyAllWindows()
                              self.imageConversion = "HSV2RGB"
                              ConvertedImage = cv2.cvtColor(self.image,cv2.COLOR_HSV2RGB)
                              self.image = ConvertedImage
                              self.imageName = "RGB_" + self.imageName
                              self.valueChanged.emit("HSV2RGB")
                              cv2.imshow(self.imageName,ConvertedImage) 
                              self.WaitKeyCloseWindows()
                                                                   
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

    # Saving the Image
    def SaveImage(self):
        if self.image is not None and self.imageName is not None:
           file_path = None 
           if self.tempImage is not None:
               file_path, _ = QFileDialog.getSaveFileName(None, "Save File", self.imageName)
               if file_path:
                     # imwrite is Saving Image Function in OpenCV that takes 2 parameter
                     # cv2.imwrite(Parameter1 = Name of Image, Parameter2 = Path to Image ) 
                     cv2.imwrite(file_path,self.tempImage)
           else: 
               file_path, _ = QFileDialog.getSaveFileName(None, "Save File", self.imageName)         
               if file_path:
                     # imwrite is Saving Image Function in OpenCV that takes 2 parameter
                     # cv2.imwrite(Parameter1 = Name of Image, Parameter2 = Path to Image ) 
                     cv2.imwrite(file_path,self.image)
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
        
    # Remove Color Channels   
    def ColorChannelRemove(self,channels):
        #print(channels)
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
          cv2.destroyAllWindows()
          # Assume all channels are None by Default then check the Conversion
          B, G, R, H, S, V = None, None, None, None, None, None
          # Let's create a matrix of zeros with dimensions of the image h x w  
          # Zeros are for removing a channel from Image
          zeros = np.zeros(self.image.shape[:2], dtype = "uint8")
          if self.imageConversion is not None:
               # merge is a Function in OpenCV for Combining Desired Selected Channels FOR cREATING an Image  
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
                           channel = []
                           if channels["RedChannel"]: 
                              self.imageName = "R_" + self.imageName
                              channel.append(R)
                           else: channel.append(zeros)
                           if channels["GreenChannel"]: 
                              self.imageName = "G_" + self.imageName
                              channel.append(G)
                           else: channel.append(zeros)                          
                           if channels["BlueChannel"]: 
                              self.imageName = "B_" + self.imageName
                              channel.append(B)
                           else: channel.append(zeros) 

                           self.image = cv2.merge(channel)
                           cv2.imshow(self.imageName,self.image)
                           self.WaitKeyCloseWindows()

                     case "BGR2HSV"|"RGB2HSV":
                           H, S, V = cv2.split(self.image)
                           channel = []
                           if channels["HSVHueChannel"]: 
                              self.imageName = "H_" + self.imageName
                              channel.append(H)
                           else: channel.append(zeros)
                           if channels["HSVSaturation"]: 
                              self.imageName = "S_" + self.imageName
                              channel.append(S)
                           else: channel.append(zeros)                          
                           if channels["HSVValue"]: 
                              self.imageName = "V_" + self.imageName
                              channel.append(V)
                           else: channel.append(zeros) 

                           self.image = cv2.merge(channel)
                           cv2.imshow(self.imageName,self.image)
                           self.WaitKeyCloseWindows()

                     case "RGB2BGR"|"HSV2BGR":
                           B, G, R = cv2.split(self.image)
                           channel = []
                           if channels["BlueChannel"]: 
                              self.imageName = "B_" + self.imageName
                              channel.append(B)
                           else: channel.append(zeros) 
                           if channels["GreenChannel"]: 
                              self.imageName = "G_" + self.imageName
                              channel.append(G)
                           else: channel.append(zeros)
                           if channels["RedChannel"]: 
                              self.imageName = "R_" + self.imageName
                              channel.append(R)
                           else: channel.append(zeros)

                           self.image = cv2.merge(channel)
                           cv2.imshow(self.imageName,self.image)
                           self.WaitKeyCloseWindows()
                    
          else:
               # If Image not Converted then Default Channel is BGR
               B, G, R = cv2.split(self.image)
               channel = []
               if channels["BlueChannel"]: 
                   self.imageName = "B_" + self.imageName
                   channel.append(B)
               else: channel.append(zeros) 
               if channels["GreenChannel"]: 
                   self.imageName = "G_" + self.imageName
                   channel.append(G)
               else: channel.append(zeros)
               if channels["RedChannel"]: 
                   self.imageName = "R_" + self.imageName
                   channel.append(R)
               else: channel.append(zeros)

               self.image = cv2.merge(channel)
               cv2.imshow(self.imageName,self.image)
               self.WaitKeyCloseWindows()
                  
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
    
    # Skew is Asymmetric by Resizing only 1 Dimention
    def SkewImage(self,name,value):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
            cv2.destroyAllWindows()
            # resize is a Function in OpenCV for Changing Dimentions of an Image
            # resize takes several Parameters -> for Skew here:
            # Parameter 1 = Image, Parameter 2 = new Dimentions, Parameter 3 = Interpolation TO Calculate new Pixel Values (Optional)
            # If no Interpolation is specified cv.INTER_LINEAR is used as default
            # New Dimensions is a Tuple (width, height)
            match name:
                  case "SkewHeight":
                     self.image = cv2.resize(self.image, (self.image.shape[1],value)) # interpolation = cv2.INTER_AREA
                  case "SkewWidth":
                     self.image = cv2.resize(self.image, (value,self.image.shape[0])) #, interpolation = cv2.INTER_AREA

            self.imageName = name + "_" + self.imageName
            self.ImageSizeChanged.emit(name)
            cv2.imshow(self.imageName,self.image)
            self.WaitKeyCloseWindows()
        
    # Resizing all Dimentions with saving Accept Ratio (Coefficient of Dimensions to Each Other) is Symmetric
    def ResizeImage(self,name,value):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
            cv2.destroyAllWindows()
            # resize is a Function in OpenCV for Changing Dimentions of an Image
            # resize can be Symmetric or Asymmetric
            # resize takes several Parameters -> here Symmetric:
            # Parameter 1 = Image, Parameter 2 = new Dimentions, Parameter 3 = Interpolation TO Calculate new Pixel Values (Optional)
            # New Dimensions is a tuple (width, height) by Saving Accept Ratio
            match name:
                  case "ResizeHeight":
                     self.image = cv2.resize(self.image, (int((self.image.shape[1]/self.image.shape[0])*value),value)) 
                  case "ResizeWidth":
                     self.image = cv2.resize(self.image, (value,int((self.image.shape[1]/self.image.shape[0])*value))) 
           
            self.imageName = name + "_" + self.imageName
            self.ImageSizeChanged.emit(name)
            cv2.imshow(self.imageName,self.image)
            self.WaitKeyCloseWindows()
            # There are other OverLoads (Same Method Name with Different Parameters) for Resize:
            # Double the size of an image:
            # Parameters: 1) Image 2) None for dsize 3) fx > Coefficient for Width 4) fy > Coefficient for Height 5) Interpolation TO Calculate new Pixel Values (Optional)
            # cv2.resize(image, None, fx=2, fy=2)
            # Interpolations: INTER_LINEAR(default), INTER_CUBIC, INTER_NEAREST, INTER_AREA
        
    # Scaling Image
    def PyrUpDown(self,name):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
            # pyrUp and pyrDown are Scaling Funcions in OpenCV, They take only 1 Parameter: Image.
            # They have an Internal Coefficient and Multiplying Dimensions to 2 in each Execution.
            match name:
                  case "LargerPyrUp":
                        if self.image.shape[0] * 2 <= 2000:
                           self.image = cv2.pyrUp(self.image)
                        else:
                              QMessageBox.warning(None, "Size Error", "Dimention limited between 50 and 2000!")

                  case "SmallerPyrDown":
                           if self.image.shape[0] / 2 >= 50:
                              self.image = cv2.pyrDown(self.image)
                           else:
                              QMessageBox.warning(None, "Size Error", "Dimention limited between 50 and 2000!")

            self.imageName = name + "_" + self.imageName
            self.ImageSizeChanged.emit(name)
            cv2.imshow(self.imageName,self.image)
            self.WaitKeyCloseWindows()
        
     # Scaling Image
    
    # Scaling Screen behind the Image with Coefficient
    def ScaleByCoefficient(self,coefficient):
        if coefficient != 0 and self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
            height, width = self.image.shape[:2]         
            # getRotationMatrix2D is a Function for Rotation in OpenCV
            # Look in Rotation, here Parameters set for no Rotation
            Rotation_Matrix2D = cv2.getRotationMatrix2D((width/2, height/2), 0, 1)
            _width_ = int(width*(1*coefficient))
            _height_ = int(height*(1*coefficient))
            try:
                  # if self.image.shape[0] * coefficient <= 2000 and self.image.shape[0] / coefficient >= 50:
                  # warpAffine is a Function in OpenCV for Scaling, Rotation, Translation and etc.
                  # There are several Overload for warpAffine Function based on Functionality needed.
                  ScaledImage = cv2.warpAffine(self.image, Rotation_Matrix2D, ( _width_, _height_ ))
                  name = "Scaled" + str(coefficient) + "Times"
                  ScaledImageName = name + "_" + self.imageName
                  self.ImageSizeChanged.emit(name)
                  cv2.imshow(self.imageName,self.image)
                  cv2.imshow(ScaledImageName,ScaledImage)
                  self.WaitKeyCloseWindows()

            except:
                QMessageBox.warning(None, "Parameter Error", "Value errors in parameters!")

     # Scaling Screen behind the Image with Coefficient
    
    # Rotate Image around its center by Angle
    def RotationByAngle(self,angle):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
            height, width = self.image.shape[:2]         
            # getRotationMatrix2D is a Function for Rotation in OpenCV
            # Parameters: 1) Tuple containing Center Point for Rotation 2) Angle 3) Scale Coefficient
            # Dimensions in Tuple Divided by two to Rotate the image around its centre
            # Scale is 1 for Displaying Image in Same Size
            Rotation_Matrix2D = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
            try:
                  # if self.image.shape[0] * coefficient <= 2000 and self.image.shape[0] / coefficient >= 50:
                  # warpAffine is a Function in OpenCV for Scaling, Rotation, Translation and etc.
                  # There are several Overload for warpAffine Function based on Functionality needed.
                  # Scaling screen Dimentions 2 Times to see the Rotation better
                  RotatedImage = cv2.warpAffine(self.image, Rotation_Matrix2D, (width*2,height*2))
                  name = "Rotated" + str(angle) + "Degree"
                  RotatedImageName = name + "_" + self.imageName
                  self.ImageSizeChanged.emit(name)
                  cv2.imshow(self.imageName,self.image)
                  cv2.imshow(RotatedImageName,RotatedImage)
                  self.WaitKeyCloseWindows()

            except:
                QMessageBox.warning(None, "Parameter Error", "Value errors in parameters!")  

    # Translation Image
    def TranslateImage(self,name,value,Diff_Array):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray) and isinstance(Diff_Array, np.ndarray):
            # Store height and width of the Image
            height, width = self.image.shape[:2]
            # MainArray is a Sample of an Image Array for Comparison with DiffArray
            MainArray = np.float32([[50, 50],[200, 50], [50, 200]])
            # DiffArray is an Array with Shape Same as MainArray With slightly Different Values
            # Translation Implements the Difference between MainArray and DiffArray on the Image
            M = cv2.getAffineTransform(MainArray, Diff_Array)
            TranslatedImage = cv2.warpAffine(self.image, M, (height, width))
            TranslatedImageName = name + "_" + self.imageName
            self.ImageSizeChanged.emit(name)
            self.tempImage = TranslatedImage
            cv2.imshow(TranslatedImageName,TranslatedImage)
            cv2.imshow(self.imageName,self.image)
            self.WaitKeyCloseWindows()
            self.tempImage = None

    # Flip or UnFlip Image Vetically or Horisantally
    def Flip(self,name):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
            match name:
                  case "FlipHorizantal":
                          # Horizontal Flip with Code 2
                          self.image = cv2.flip(self.image, 2)
                  case "FlipVertical":
                          # Vertical Flip with Code 0
                          self.image = cv2.flip(self.image, 0)

            self.imageName = name + "_" + self.imageName
            self.ImageSizeChanged.emit(name)
            cv2.imshow(self.imageName,self.image)
            self.WaitKeyCloseWindows()

    # Transpose Image Swapping Rows value with Columns values (90 Degree Rotation)
    def Transpose(self):
         if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):  
            # transpose Function for 90 Degree Rotation has only Image Parameter
            self.image = cv2.transpose(self.image)       
            self.imageName = "Transposed_" + self.imageName
            self.ImageSizeChanged.emit("Transpose")
            cv2.imshow(self.imageName,self.image)
            self.WaitKeyCloseWindows()
        