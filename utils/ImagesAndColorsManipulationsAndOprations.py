# Import Essential Libraries
import time
import cv2 # Import Main Computer Vision Library in Python
import numpy as np
import os
from os import path, listdir
from os.path import isfile, join
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QFileDialog

class ImagesAndColorsManipulationsAndOprations(QObject):
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
        self.tempImageName = None

    # Consider|Attention: 
    # Here all parameters Assigned have relation to Image Dimensions for Visibility of Changes > image.shape = (height,width,depth)
    # OpenCV Functions have several Overloads (Same Method Names with different Parameters some of them Mandatory and some Optional):
    # Here Mandatory Parameters with some Optional Parameters filled, in Practical RealWorld Projects use IDE IntelliJ IDEA by pressing Ctrl + Space:
    # This offers a broad range of suggestions relevant to the current context, including parameters, variables, methods, classes, and even closing braces.

    # Wait for Clicking a Key on Keyboard to Close All cv2 Windows
    def WaitKeyCloseWindows(self):
        # Wait until Clicking a Key on Keyboard
        cv2.waitKey(0)
        # Close All cv2 Windows
        cv2.destroyAllWindows()
        self.tempImage = None
        self.tempImageName = None
        self.ResetParams.emit(0)
        if cv2.getWindowProperty(self.imageName, cv2.WND_PROP_VISIBLE) == -1:
           self.ResetParams.emit(0)
           self.tempImage = None
           self.tempImageName = None

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
                 self.valueChanged.emit(ImageName)
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
                   case "BGR to Gray Scale":
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

                   case "BGR to RGB":
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
                             
                   case "BGR to HSV":
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

                   case "RGB to Gray Scale":
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

                   case "RGB to BGR":
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

                   case "RGB to HSV":
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

                   case "HSV to BGR":
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

                   case "HSV to RGB":
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
         file_path = None 
         if self.tempImage is not None and self.tempImageName is not None and isinstance(self.tempImage, np.ndarray):
            file_path, _ = QFileDialog.getSaveFileName(None, "Save File", self.tempImageName)
            if file_path:
                  # imwrite is Saving Image Function in OpenCV that takes 2 parameter
                  # cv2.imwrite(Parameter1 = Name of Image, Parameter2 = Path to Image ) 
                  cv2.imwrite(file_path,self.tempImage)
         elif self.image is not None and self.imageName is not None:
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
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
        
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
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
        
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
        
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
    
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
                  name = "BackScaled" + str(coefficient) + "Times"
                  ScaledImageName = name + "_" + self.imageName
                  self.tempImage = ScaledImage
                  self.tempImageName = ScaledImageName
                  self.ImageSizeChanged.emit(name)
                  cv2.imshow(self.imageName,self.image)
                  cv2.imshow(ScaledImageName,ScaledImage)
                  self.WaitKeyCloseWindows()
                  self.tempImage = None
                  self.tempImageName = None

            except:
                QMessageBox.warning(None, "Parameter Error", "Value errors in parameters!")
        
        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

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
                  self.tempImage = RotatedImage
                  self.tempImageName = RotatedImageName
                  self.ImageSizeChanged.emit(name)
                  cv2.imshow(self.imageName,self.image)
                  cv2.imshow(RotatedImageName,RotatedImage)
                  self.WaitKeyCloseWindows()
                  self.tempImage = None
                  self.tempImageName = None

            except:
                QMessageBox.warning(None, "Parameter Error", "Value errors in parameters!")  

        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

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
            TranslatedImageName = name + "Translation_" + self.imageName
            self.ImageSizeChanged.emit(name)
            self.tempImage = TranslatedImage
            self.tempImageName = TranslatedImageName
            cv2.imshow(self.imageName,self.image)
            cv2.imshow(TranslatedImageName,TranslatedImage)
            self.WaitKeyCloseWindows()
            self.tempImage = None
            self.tempImageName = None

        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

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

        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

    # Transpose Image Swapping Rows value with Columns values (90 Degree Rotation)
    def Transpose(self):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):  
            # transpose Function for 90 Degree Rotation has only Image Parameter
            self.image = cv2.transpose(self.image)       
            self.imageName = "Transposed_" + self.imageName
            self.ImageSizeChanged.emit("Transpose")
            cv2.imshow(self.imageName,self.image)
            self.WaitKeyCloseWindows()

        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
        
    # Crop Image by Coordinates: TopLeft and BottomRight
    def Crop(self,TopLeft,BottomRight):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):  
            # Image dimensions
            height, width = self.image.shape[:2]
            # Assign Starting Pixel Coordiantes (Top  Left for Cropping Rectangle)
            # Using TopLeft to get the x,y Position that is Down from the Top Left (0,0)
            start_row, start_col = int(height * TopLeft), int(width * TopLeft)
            # Assign Ending Pixel Coordinates (Bottom Right for Cropping Rectangle)
            end_row, end_col = int(height * BottomRight), int(width * BottomRight)
            # Crop out the Desired Rectangle by Indexes:
            # +3 and -3 to start and end is for removing Rectangle Tickness that is 3 
            croppedImage = self.image[start_row + 3 :end_row - 3 , start_col + 3 :end_col - 3]
            croppedImageName = "CroppedImage_" + self.imageName
            # cv2.rectangle Function draws a Rectangle over Image (in-place Operation)
            # Explained in Shapes Function
            cv2.rectangle(self.image, (start_col,start_row), (end_col,end_row), (0,255,255), 3)
            self.tempImage = croppedImage
            self.tempImageName = croppedImageName
            self.imageName = "CropedArea_" + self.imageName
            self.ImageSizeChanged.emit(str(BottomRight))
            cv2.imshow(self.imageName, self.image)
            cv2.imshow(croppedImageName, croppedImage) 
            self.WaitKeyCloseWindows()
            self.tempImage = None
            self.tempImageName = None

        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

    # Add Text to Image
    def AddText(self,text):
        # Check if Image does not Exist then Create a Colored Image
        if self.image is None or self.imageName is None or not isinstance(self.image, np.ndarray): 
           self.image = np.zeros((600,800,3), np.uint8) 
           self.imageName = "ExampleImage.jpg"
        # putText is a Function for Adding Text to Image
        # Parameters: 1) Image 2) DesiredText 3) Inser Point 4) Font 5) Font Scale 6) Color 7) Thickness
        if self.tempImage is not None and self.tempImageName is not None:
            cv2.putText(self.tempImage,text, (10,int(self.image.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (240,170,0) , 2)
            cv2.imshow(self.tempImageName,self.tempImage)
        else:
            cv2.putText(self.image,text, (10,int(self.image.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (240,170,0) , 2)
            cv2.imshow(self.imageName,self.image)
        
        self.WaitKeyCloseWindows()
        self.tempImage = None
        self.tempImageName = None
       
    # Draw Some Shapes
    def DrawShape(self,shape): 
        # Check if Image does not Exist then Create a Colored Image
        if self.image is None or self.imageName is None or not isinstance(self.image, np.ndarray): 
           self.image = np.zeros((600,800,3), np.uint8) 

        match shape:
              case "Line":
                   # Line Function to Draw a Line
                   # Parameters: 1) Image 2) Start Point Coordinate 3) End Point Coordinate 4) Color 5) Thickness
                   cv2.line(self.image, (0,0), (self.image.shape[1],self.image.shape[0]), (255,127,0), 5) 
              case "Rectangle":                   
                   TopLeft = (int(self.image.shape[1]/4) , int(self.image.shape[0]/4))
                   BottomRight = (int(self.image.shape[1]/4)*3 , int(self.image.shape[0]/4)*3)
                   Color = (127,50,127)
                   Thickness = 4
                   # cv2.rectangle is a Function for Drawing Rectangle
                   # Parameters: 1) Image 2) Top Left Point 3) Bottom Right Point 4) Color 5) Thickness
                   # Negative thickness means that it is filled instead Stroke (OutLine)
                   cv2.rectangle(self.image, TopLeft, BottomRight, Color, Thickness)
              case "Circle":                   
                   CenterPoint = (int(self.image.shape[1]/2), int(self.image.shape[0]/2))
                   Radius = 0
                   if self.image.shape[0] > self.image.shape[1]:
                      Radius = int((self.image.shape[1]/5)*2)
                   else:
                      Radius = int((self.image.shape[0]/5)*2)
                   Color = (15,75,50)
                   Thickness = -1
                   # cv2.circle is a Function for Drawing Circle
                   # Parameters: 1) Image 2) Center Point 3) Radius 4) Color 5) Thickness
                   # Negative thickness means that it is filled instead Stroke (OutLine)
                   cv2.circle(self.image, CenterPoint, Radius, Color, Thickness)
              case "Ellipse":
                   # cv2.ellipse is a Function for Drawing Ellipse
                   # Parameters: 1) Image 2) Center Point 3) Axes Size 4) Angle 5) Start Angle 6) End Angle 7) Color 8) Thickness
                   # Negative thickness means that it is filled instead Stroke (OutLine)
                   CenterPoint = (int(self.image.shape[1]/2), int(self.image.shape[0]/2))
                   AxesSize = CenterPoint
                   Angle = 30
                   StartAngle = 0
                   EndAngle = 180
                   Color = 255
                   Thickness = -1
                   cv2.ellipse(self.image, CenterPoint, AxesSize, Angle, StartAngle, EndAngle, Color, Thickness)
              case "PolyLines":                   
                   # Define 4 Points
                   Points = np.array( [[10,5], 
                                       [self.image.shape[1]-5,self.image.shape[0]-10], 
                                       [int(self.image.shape[1]/3),int(self.image.shape[0]/4)],
                                       [20,int(self.image.shape[0]/2)]], 
                                       np.int32)
                   # cv2.polylines is a Function for Drawing PolyLines
                   # Parameters: 1) Image 2) Array of Points 3) isClosed Bool 4) Color 5) Thickness
                   cv2.polylines(self.image, [Points], True, (0,0,255), 3)
              
        cv2.imshow(self.imageName,self.image)
        self.WaitKeyCloseWindows()

    # Arithmetic and Bitwise Operations
    def Operations(self,operation):  
        match operation:
            case "Arithmetic Operations":
                  if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
                     cv2.destroyAllWindows()
                     cv2.imshow("Original", self.image)  
                     # Create a Matrix of Ones, then Multiply it by a Scaler of 100 
                     # This gives a Matrix with same Dimesions of Image with all Values being 100
                     Matrix = np.ones(self.image.shape, dtype = "uint8") * 100
                     # Difference Between Intelligenge Arithmetic Operations by OpenCV Functions and by Python Operators (+,-,*,/):
                     # For Example in BGR or RGB, Range of Color Values are Between 0 and 255:
                     # By Functions when Result Exceeds Color Value Maximum Range, It put The Max Value in the Result and Ignores Rest > 195 + 100 = 255 and Ignores 40
                     # By Operators when Result Exceeds Color Value Maximum Range, It Divide the Result to Max Value and Put Reminder as a Result > 195 + 100 = 295 % 255 = 40
                     # By Functions when Result is less than Color Value Minimum Range, It put The Min Value in the Result and Ignores Rest > 100 - 150 = 0 and Ignores 50
                     # By Operators when Result is less than Value Minimum Range, It Multiply the Result to -1 then Divide the Result to Max Value and Put Reminder as a Result > 100 - 150 = -50 * -1 = 50 % 255 = 50

                     # Add Matrix to Image
                     # Notice the Increase in Brightness
                     AddedByFunction = cv2.add(self.image, Matrix)
                     cv2.imshow("Added By Function", AddedByFunction)
                     AddedByPlusWithoutFunction = self.image + Matrix
                     cv2.imshow("Added By Plus Without Function", AddedByPlusWithoutFunction)
                     
                     # Subtract Matrix from Image
                     # Notice the Decrease in Brightness
                     SubtractedByFunction = cv2.subtract(self.image, Matrix)
                     cv2.imshow("Subtracted By Function", SubtractedByFunction)
                     SubtractedByMinusWithoutFunction = self.image - Matrix 
                     cv2.imshow("Subtracted By Minus Without Function", SubtractedByMinusWithoutFunction)
                     
                     # Multiply Matrix to Image
                     # Notice the Increase in Brightness
                     MultipliedByFunction = cv2.multiply(self.image, Matrix)
                     cv2.imshow("Multiplied By Function", MultipliedByFunction)
                     MultipliedByAsteriskWithoutFunction = self.image - Matrix 
                     cv2.imshow("Multiplied By Asterisk Without Function", MultipliedByAsteriskWithoutFunction)

                     # Divide Matrix from Image
                     # Notice the Decrease in Brightness
                     DividedByFunction = cv2.divide(self.image, Matrix)
                     cv2.imshow("Divided By Function", DividedByFunction)
                     DividedBySlashWithoutFunction = self.image - Matrix 
                     cv2.imshow("Divided By Slash Without Function", DividedBySlashWithoutFunction)

                     self.WaitKeyCloseWindows()
                   
                  else:
                       QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
 
            case "Bitwise Operations":
               cv2.destroyAllWindows()
               self.tempImage = None
               self.tempImageName = None
               self.ResetParams.emit(0)
               # First Create 2 GrayScale Images:
               # Black Areas are where are Empty (Part or Whole of Images or Screen are not Purpose of Show)
               # White Areas are where are Exist (Part or Whole of Images or Screen are Purpose of Show)

               # Making a Sqare
               BlankImage = np.zeros((400, 400), np.uint8)
               square = cv2.rectangle(BlankImage, (100, 100), (300, 300), 255, -1)
               cv2.imshow("Square", square)

               # Making an Circle
               BlankImage = np.zeros((400, 400), np.uint8)
               circle = cv2.circle(BlankImage, (100, 100), 100, 255, -1)
               cv2.imshow("Circle", circle) 

               # Shows only where they Intersect
               bitwise_And = cv2.bitwise_and(square, circle)
               cv2.imshow("AND", bitwise_And)

               # Shows where either Square or Circle is 
               bitwise_Or = cv2.bitwise_or(square, circle)
               cv2.imshow("OR", bitwise_Or)

               # Shows where either exist by itself
               bitwise_Xor = cv2.bitwise_xor(square, circle)
               cv2.imshow("XOR", bitwise_Xor)

               # Shows everything that isn't part of the Square
               bitwise_Not_Square = cv2.bitwise_not(square)
               cv2.imshow("NOT - Square", bitwise_Not_Square)

               # Shows everything that isn't part of the Circle
               bitwise_Not_Circle = cv2.bitwise_not(circle)
               cv2.imshow("NOT - Circle", bitwise_Not_Circle)

               self.WaitKeyCloseWindows() 

    # Filters (Bluring, De-Noising, Segmentation)
    def Filters(self,filter): 
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):  
            match filter.strip():
                  case "Bluring and Sharprning by Kernel":       
                        cv2.destroyAllWindows() 
                        cv2.imshow("Original", self.image)             
                        # Creating our 3 x 3 kernel
                        kernel_3x3 = np.ones((3, 3), np.float32) / 9
                        # Creating our 7 x 7 kernel
                        kernel_7x7 = np.ones((7, 7), np.float32) / 49

                        # cv2.fitler2D Conovlve the Kernal with an Image 
                        # Parameters: 1) Image 2) DDepth 3) Kernel Matrix
                        # wHEN ddepth is set to -1, the output image will have the same depth as the input (source) image
                        blurred_by_kernel_3x3 = cv2.filter2D(self.image, -1, kernel_3x3)
                        blurred_by_kernel_7x7 = cv2.filter2D(self.image, -1, kernel_7x7)
                        cv2.imshow('3x3 Kernel Blurring', blurred_by_kernel_3x3)
                        cv2.imshow('7x7 Kernel Blurring', blurred_by_kernel_7x7)

                        # Create a Shapening Kernel with below Rules:
                        # Sharpening kernels are designed to increase the intensity of the center pixel relative to its neighbors: 
                        # This is achieved by assigning a positive, relatively large weight to the center element of the kernel.
                        # To enhance edges and details, the kernel typically assigns negative weights to the surrounding pixels:
                        # This effectively subtracts the influence of the neighbors, amplifying the difference between the center pixel and its surroundings.
                        # For a sharpening kernel, the sum of all elements in the kernel should ideally be equal to 1. 
                        # This ensures that the overall brightness of the image is maintained after the sharpening operation. 
                        # If the sum is greater than 1, the image will appear brighter; if less than 1, it will appear darker.
                        kernel_sharpening = np.array([[-1,-1,-1], 
                                                      [-1, 9,-1],
                                                      [-1,-1,-1]])

                        # Applying the Sharpening Kernel to the Image
                        sharpened = cv2.filter2D(self.image, -1, kernel_sharpening)
                        cv2.imshow('Sharpened Image', sharpened)
                        
                  case "De-Noising by Filter": 
                        cv2.destroyAllWindows()
                        cv2.imshow("Original", self.image) 
                        # Bilateral is very effective in Noise Removal while keeping Edges Sharp, Result seems Bluring
                        # Parameters: 
                        # d: Diameter of each pixel neighborhood.
                        # sigmaColor: Value of σ in the color space. The greater the value, the colors farther to each other will start to get mixed.
                        # sigmaSpace: Value of σ in the coordinate space.
                        bilateral = cv2.bilateralFilter(self.image, 9, 75, 75)
                        cv2.imshow('Bilateral Denoising - Blurring', bilateral) 

                        # cv2.fastNlMeansDenoisingColored Function in OpenCV is used for Non-Local Means Denoising of colored images.
                        # Parameters: 1) src Image 2) dst 3) 
                        # dst: is The output image, which will have the same size and type as the input src. If None, a new image is allocated.
                        # h: A float value representing the filter strength for the luminance (grayscale) component. A larger h value applies stronger denoising but may also remove more image details.
                        # hColor: A float value representing the filter strength for the color components (chrominance). Similar to h, a larger hColor value applies stronger denoising to colors. For most images, a value of 10 is often sufficient to remove colored noise without significantly distorting colors.
                        # templateWindowSize: An integer representing the size in pixels of the square template patch used to compute weights. This value should be odd, and a recommended value is 7 pixels.
                        # searchWindowSize: An integer representing the size in pixels of the square window within which similar patches are searched to compute a weighted average for the current pixel. This value should also be odd, and a recommended value is 21 pixels. A larger searchWindowSize increases denoising time. 
                        # Default values: h: 3, hColor: 3, templateWindowSize: 7, and searchWindowSize: 21.
                        if len(self.image.shape) < 3:
                           QMessageBox.critical(None, "Image Shape Error", "For Fast Means Denoising, Select a Colored Image!")
                        else:
                           dst = cv2.fastNlMeansDenoisingColored(self.image, None, 6, 6, 7, 21)
                           cv2.imshow('Fast Means Denoising', dst)                   

                  case "Bluring by Filter":
                        cv2.destroyAllWindows()
                        cv2.imshow("Original", self.image) 
                        # cv2.blur() is a function within the OpenCV library used for image blurring.
                        # It applies a normalized box filter to smooth an image. This type of blurring is also known as averaging blur.
                        # Averaging done by convolving the image with a normalized box filter. 
                        # This takes the pixels under the box and replaces the central element
                        # Box size needs to be odd and positive 
                        blur = cv2.blur(self.image, (3,3))
                        cv2.imshow('Averaging', blur)

                        # Instead of box filter, gaussian kernel
                        Gaussian = cv2.GaussianBlur(self.image, (3,3), 0)
                        cv2.imshow('Gaussian Blurring', Gaussian)

                        # Takes median of all the pixels under kernel area and central 
                        # Element is replaced with this median value
                        median = cv2.medianBlur(self.image, 3)
                        cv2.imshow('Median Blurring', median) 

                  case "Segmenting by Threshold - Binarization":
                        cv2.destroyAllWindows()
                        cv2.imshow("Original", self.image) 
                        # The cv2.threshold() function in OpenCV is used for image thresholding
                        # A technique that converts a Grayscale image into a Binary image based on a specified Threshold value. 
                        # Pixels are categorized into two groups: those above the threshold and those below the threshold.
                        # '''                      
                        # Parameters:
                        #    src: The input grayscale image.
                        #    thresh: The threshold value. Pixels with intensity values above or below this value will be processed according to the type.
                        #    maxval: The maximum value to be assigned to pixels exceeding the threshold (or falling below it, depending on the type). 
                        #            Typically, this is 255 for an 8-bit image.
                        #    type: The type of thresholding to be applied. Common types include:
                        #       cv2.THRESH_BINARY: If a pixel's intensity is greater than thresh, it's set to maxval; otherwise, it's set to 0.
                        #       cv2.THRESH_BINARY_INV: If a pixel's intensity is greater than thresh, it's set to 0; otherwise, it's set to maxval.
                        #       cv2.THRESH_TRUNC: If a pixel's intensity is greater than thresh, it's set to thresh; otherwise, it remains unchanged.
                        #       cv2.THRESH_TOZERO: If a pixel's intensity is greater than thresh, it remains unchanged; otherwise, it's set to 0.
                        #       cv2.THRESH_TOZERO_INV: If a pixel's intensity is greater than thresh, it's set to 0; otherwise, it remains unchanged.
                        # 
                        # Return Values:
                        #    retval: In simple thresholding, this is the thresh value provided. 
                        #            In methods like Otsu's thresholding (which can be combined with cv2.threshold), 
                        #            it returns the optimal threshold value calculated by the algorithm.
                        #    dst: The thresholded output image.
                        # '''

                        # Values below 127 goes to 0 (black, everything above goes to 255 (white)
                        ReturnValues,thresh1 = cv2.threshold(self.image, 200, 255, cv2.THRESH_BINARY)
                        cv2.imshow('1 Threshold Binary', thresh1)

                        # Values below 127 go to 255 and values above 127 go to 0 (reverse of above)
                        ReturnValues,thresh2 = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY_INV)
                        cv2.imshow('2 Threshold Binary Inverse', thresh2)

                        # Values above 127 are truncated (held) at 127 (the 255 argument is unused)
                        ReturnValues,thresh3 = cv2.threshold(self.image, 127, 255, cv2.THRESH_TRUNC)
                        cv2.imshow('3 THRESH TRUNC', thresh3)

                        # Values below 127 go to 0, above 127 are unchanged  
                        ReturnValues,thresh4 = cv2.threshold(self.image, 127, 255, cv2.THRESH_TOZERO)
                        cv2.imshow('4 THRESH TOZERO', thresh4)

                        # Reverse of the above, below 127 is unchanged, above 127 goes to 0
                        ReturnValues,thresh5 = cv2.threshold(self.image, 127, 255, cv2.THRESH_TOZERO_INV)
                        cv2.imshow('5 THRESH TOZERO INV', thresh5)

                  case "Segmenting by Adaptive Threshold - Binarization":
                        # cv2.adaptiveThreshold Parameters:
                        # cv2.adaptiveThreshold**(src, maxValue, adaptiveMethod, thresholdType, blockSize, C[, dst]) → dst
                        # src – Source 8-bit single-channel image.
                        # dst – Destination image of the same size and the same type as src.
                        # maxValue – Non-zero value assigned to the pixels for which the condition is satisfied. See the details below.
                        # adaptiveMethod – Adaptive thresholding algorithm to use, ADAPTIVE_THRESH_MEAN_C or ADAPTIVE_THRESH_GAUSSIAN_C . See the details below.
                        # thresholdType – Thresholding type that must be either THRESH_BINARY or THRESH_BINARY_INV.
                        # blockSize – Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on.
                        # C – Constant subtracted from the mean or weighted mean. Normally, it is positive but may be zero or negative as well.
                        if len(self.image.shape) > 2:
                           QMessageBox.critical(None, "Image Shape Error", "For Adaptive Thresholding, First Convert the Image to GrayScale!")
                        else:
                              cv2.destroyAllWindows()
                              cv2.imshow("Original", self.image) 
                              # Values below 127 goes to 0 (black, everything above goes to 255 (white)
                              ReturnValues,thresh1 = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY)
                              cv2.imshow('Threshold Binary', thresh1)

                              # It's good practice to blur images as it removes noise
                              self.image = cv2.GaussianBlur(self.image, (3, 3), 0)
                           
                              # Using adaptiveThreshold
                              Adaptive_thresh = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 3) 
                              cv2.imshow("Adaptive Mean Thresholding", Adaptive_thresh) 

                              ReturnValues,thresh2 = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                              cv2.imshow("Otsu's Thresholding", thresh2) 

                              # Otsu's thresholding after Gaussian filtering
                              self.image = cv2.GaussianBlur(self.image, (5,5), 0)
                              ReturnValues, thresh3 = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                              cv2.imshow("Guassian Otsu's Thresholding", thresh3)  

            self.WaitKeyCloseWindows()                                        
        
        else:
            QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

    # Dilation, Erosion, Edge Detection            
    def DilationErosionEdgeDetection(self,operation):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
            match operation:
                  case "Dilation, Erosion, Opening, Closing":
                        cv2.destroyAllWindows()
                        cv2.imshow("Original", self.image)              
                        # Define a kernel Matrix (Default is 3*3)
                        kernel = np.ones((5,5), np.uint8)
                        '''                      
                        cv2.erode() is a function within the OpenCV used for performing morphological erosion on an image. 
                        Useful for tasks like noise removal, thinning object boundaries, and disconnecting connected components.
                        How it works:
                        Erosion operates by "eroding away" the boundaries of foreground objects in a binary image 
                        (where foreground is typically represented by white pixels and background by black). 
                        The process involves:
                        
                           Kernel/Structuring Element:
                           A small matrix, known as a kernel or structuring element, slides across the image.
                           
                           Pixel Evaluation:
                           For each pixel in the image, the kernel's origin is placed on that pixel. 
                           The pixel in the output image (eroded image) will be a foreground pixel (white) only 
                           if all the pixels under the kernel in the original image are also foreground pixels. 
                           Otherwise, the output pixel will be a background pixel (black).
                           
                           Boundary Shrinkage:
                           This process effectively shrinks the white regions or foreground objects in the image, 
                           as any foreground pixels that are not entirely covered by the kernel (i.e., they are on the boundary) will be turned into background pixels. 

                        Key Parameters:

                           src: The input image.
                           kernel: The structuring element used for erosion. This can be created using cv2.getStructuringElement() or numpy.ones(). 
                                   If None, a default 3x3 rectangular kernel is used.
                           iterations: The number of times the erosion operation is applied. More iterations lead to greater erosion.
                           anchor: The position of the anchor within the kernel. By default, it's at the center.
                           borderType: and borderValue: Used to handle borders during the operation.

                        Applications:

                           Noise Removal: Removing small, isolated foreground "blobs" or noise.
                           Thinning Object Boundaries: Making the outlines of objects thinner.
                           Disconnecting Connected Objects: Separating objects that are slightly connected.
                           Boundary Detection: Subtracting the eroded image from the original can highlight object boundaries.
                        '''
                        # Erode
                        erosion = cv2.erode(self.image, kernel, iterations = 1)
                        cv2.imshow('Erosion', erosion)
                        '''
                        cv2.dilate is a function within the OpenCV that performs morphological dilation on an image. 
                        Dilation is a fundamental morphological operation used to expand the white (or foreground) regions in a binary image. 
                        Functionality:

                           Expansion of Foreground:
                           It effectively "grows" or thickens the boundaries of foreground objects (typically represented by white pixels) in an image.

                        Filling Holes and Connecting Components:
                                Dilation can be used to fill small holes within objects and to connect disjointed components that are close to each other.
                        Effect of Kernel:
                                The extent of dilation is determined by a "structuring element" or "kernel." 
                                This kernel defines the shape and size of the neighborhood over which the dilation operation is applied. 
                                If at least one pixel under the kernel is a foreground pixel (e.g., 1 or 255), the central pixel under the kernel is set to a foreground value. 

                        Syntax IN Python:

                                        cv2.dilate(src, kernel, dst=None, anchor=(-1,-1), iterations=1, borderType=BORDER_REFLECT_101, borderValue=None)

                        Parameters:

                           src: The input image, which should typically be a binary image or an image where foreground objects are represented by higher intensity values.
                           kernel: The structuring element used for dilation. This can be created using np.ones() or cv2.getStructuringElement().
                           iterations: (Optional) The number of times the dilation operation is applied.
                           Other optional parameters control aspects like the anchor point of the kernel, border handling, etc.

                        Typical Use Cases:

                           Noise Removal: Often used in conjunction with cv2.erode (erosion) in operations like "opening" - 
                           (erosion followed by dilation) to remove small noise while preserving object shape.
                           Connecting Broken Objects: Useful for joining parts of an object that have been separated due to noise or other image processing steps.
                           Thickening Object Boundaries: Can be used to make foreground objects appear larger or more prominent.
                        '''
                        # Dilate 
                        dilation = cv2.dilate(self.image, kernel, iterations = 1)
                        cv2.imshow('Dilation', dilation)
                        '''                        
                        The cv2.morphologyEx() function in OpenCV is used to perform advanced morphological transformations on images. 
                        These operations are based on fundamental morphological operations like erosion and dilation, 
                        but combine them in specific sequences to achieve more complex effects.
                        The syntax for cv2.morphologyEx() IN Python is:
                                             cv2.morphologyEx(src, op, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]])
                        Key Arguments:
                           src: The input image.
                           op: The type of morphological operation to be performed. This can be one of the following:
                              cv2.MORPH_OPEN: Opening (erosion followed by dilation). Useful for removing small objects or noise.
                              cv2.MORPH_CLOSE: Closing (dilation followed by erosion). Useful for filling small holes or gaps in objects.
                              cv2.MORPH_GRADIENT: Morphological gradient (dilation minus erosion). Highlights object boundaries.
                              cv2.MORPH_TOPHAT: Top Hat (original image minus opening). Reveals bright objects on a dark background.
                              cv2.MORPH_BLACKHAT: Black Hat (closing minus original image). Reveals dark objects on a bright background. 
                           kernel: The structuring element (kernel) used for the morphological operation. This can be created using cv2.getStructuringElement().
                           dst: Optional output image.
                           anchor: Optional anchor position within the kernel.
                           iterations: Optional number of times the morphological operation is applied.
                           borderType: Optional border type.
                           borderValue: Optional border value.

                        Common Uses:
                           Noise removal: Opening can effectively remove small noise particles.
                           Hole filling: Closing can fill small holes within objects.
                           Object boundary detection: Morphological gradient highlights edges.
                           Feature extraction: Top Hat and Black Hat can be used to extract specific features based on their brightness relative to the background.
                        '''
                        # Opening - Good for removing noise
                        opening = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
                        cv2.imshow('Opening', opening)

                        # Closing - Good for removing noise
                        closing = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)
                        cv2.imshow('Closing', closing) 
                        
                  case "Edge Detection by Canny (Normal, Wide, Narrow)":
                        cv2.destroyAllWindows()
                        cv2.imshow("Original", self.image) 
                        '''                        
                        cv2.Canny is a function in the OpenCV library used to perform Canny edge detection on an image. 
                        The Canny edge detection algorithm is a multi-stage process designed to detect:
                        a wide range of edges in images while suppressing noise and providing good localization.
                        
                        The cv2.Canny function typically takes the following main parameters:

                           image: The input image on which edge detection is to be performed. This image is usually grayscale.
                           threshold1: The first (lower) threshold for the hysteresis thresholding procedure.
                           threshold2: The second (upper) threshold for the hysteresis thresholding procedure. 

                        How Canny Edge Detection Works (in stages):

                           Noise Reduction:
                           The image is first smoothed using a Gaussian filter to remove noise that could lead to false edges.
                           Gradient Calculation:
                           The intensity gradients of the smoothed image are then calculated to find potential edge magnitudes and directions.
                           Non-Maximum Suppression:
                           This stage thins the edges by suppressing pixels that are not at the local maximum of the gradient magnitude in the direction of the gradient. 
                           This ensures that only single-pixel-wide edges remain.
                           Hysteresis Thresholding:
                           This is a crucial step that uses two thresholds (threshold1 and threshold2).
                              Pixels with gradient magnitudes above threshold2 are considered "strong" edges.
                              Pixels with gradient magnitudes between threshold1 and threshold2 are considered "weak" edges.
                              Weak edges are only included in the final edge map if they are connected to strong edges. 
                              This helps to connect broken edge segments and eliminate isolated noise.
                        '''
                        # Canny Edge Detection uses gradient values as thresholds
                        canny = cv2.Canny(self.image, 50, 120)
                        cv2.imshow('Canny 1', canny)

                        canny = cv2.Canny(self.image, 70, 110)
                        cv2.imshow('Canny 2', canny) 

                        canny = cv2.Canny(self.image, 10, 170)
                        cv2.imshow('Canny 3', canny)

                        canny = cv2.Canny(self.image, 80, 100)
                        cv2.imshow('Canny 4', canny)

                        canny = cv2.Canny(self.image, 60, 110)
                        cv2.imshow('Canny 4', canny)

                        canny = cv2.Canny(self.image, 10, 200)
                        cv2.imshow('Canny Wide', canny)

                        canny = cv2.Canny(self.image, 200, 240)
                        cv2.imshow('Canny Narrow', canny)

                  case "Edge Detection Comparison (Canny, Sobel, Laplacian)":
                        cv2.destroyAllWindows()
                        cv2.imshow("Original", self.image) 
                        '''                     
                        cv2.Sobel is a function in the OpenCV library used to compute image derivatives, specifically focusing on edge detection. 
                        It approximates the gradient of the image intensity function, highlighting areas of significant change in pixel values.
                        Function Signature in Python:
                                                    dst = cv2.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]])
                        Parameters:
                           src: The input image. It should be an 8-bit, 16-bit, or 32-bit floating-point image.
                           ddepth: The desired depth of the output image. Common choices include:
                                   cv2.CV_8U for 8-bit unsigned integers, cv2.CV_16S for 16-bit signed integers, and cv2.CV_64F for 64-bit floating-point numbers. 
                                   Using floating-point depths like cv2.CV_64F is often recommended to avoid data loss due to truncation, 
                                   especially when dealing with negative gradient values.
                           dx: Order of the derivative in the x direction. It can be 0 or 1.
                           dy: Order of the derivative in the y direction. It can be 0 or 1.
                           dst: (optional): Output image of the same size and number of channels as src.
                           ksize: (optional): Size of the extended Sobel kernel; it must be 1, 3, 5, or 7. A larger ksize results in a smoother derivative but can also blur fine details.
                           scale: (optional): Optional scale factor for the computed derivative values.
                           delta: (optional): Optional delta value added to the results before storing them in dst.
                           borderType: (optional): Pixel extrapolation method.

                        How it works:
                        The Sobel operator works by convolving the input image with two kernels: 
                            one for horizontal gradients (detecting vertical edges) and one for vertical gradients (detecting horizontal edges). 
                        These kernels are designed to approximate the first derivative of the image intensity. 
                        The combination of these gradients can then be used to calculate the overall gradient magnitude and direction, which are crucial for edge detection algorithms.
                        '''
                        height, width , depth = 0 , 0 , 0
                        if len (self.image.shape) > 2: height, width, depth = self.image.shape
                        else: height, width = self.image.shape
                        # Extract Sobel Edges
                        sobel_x = cv2.Sobel(self.image, cv2.CV_64F, 0, 1, ksize=5)
                        sobel_y = cv2.Sobel(self.image, cv2.CV_64F, 1, 0, ksize=5)
                        sobel_OR = cv2.bitwise_or(sobel_x, sobel_y)
                        cv2.imshow('Sobel X', sobel_x)
                        cv2.imshow('Sobel Y', sobel_y)
                        cv2.imshow('sobel_OR', sobel_OR)
                        '''
                        cv2.Laplacian is a function in the OpenCV library used to compute the Laplacian of an image. 
                        The Laplacian operator is a second-order derivative operator that highlights regions of rapid intensity change, making it useful for edge detection. 
                        Function Signature:
                        Python

                        cv2.Laplacian(src, ddepth[, dst[, ksize[, scale[, delta[, borderType]]]]])

                        Parameters:

                           src: The input image (source image).
                           ddepth: The desired depth of the destination image. This is crucial as the Laplacian can produce negative values, 
                                   which are lost if the output is an 8-bit unsigned integer type (CV_8U or np.uint8). 
                                   Common choices to preserve negative values include CV_16S, CV_32F, or CV_64F.
                           dst: Optional output image. If provided, it will store the result.
                           ksize: Optional size of the extended Laplacian kernel. It must be positive and odd. Default is 1.
                           scale: Optional scaling factor for the computed Laplacian values. Default is 1.
                           delta: Optional value added to the result. Default is 0.
                           borderType: Optional border extrapolation method. Default is BORDER_DEFAULT.

                        Usage:
                        The cv2.Laplacian function calculates the second derivative in both the x and y directions, summing them to produce the Laplacian value for each pixel. 
                        Edges are typically found at zero-crossings in the Laplacian output, where the pixel intensity changes rapidly. 
                        Due to its sensitivity to noise, it is often recommended to apply a smoothing filter (like a Gaussian blur) to the image before applying the Laplacian operator.
                        '''
                        laplacian = cv2.Laplacian(self.image, cv2.CV_64F)
                        cv2.imshow('Laplacian', laplacian)
                        
                        # Provide two values: threshold1 and threshold2. 
                        # Any gradient value larger than threshold2 is considered to be an edge. 
                        # Any value below threshold1 is considered not to be an edge. 
                        # Values between threshold1 and threshold2 are either classiﬁed as edges or non-edges based on how their intensities are “connected”. 
                        # In this case, any gradient values below 60 are considered non-edges whereas any values above 120 are considered edges.

                        # Canny Edge Detection uses gradient values as thresholds
                        canny = cv2.Canny(self.image, 50, 120)
                        cv2.imshow('Canny', canny)  

            self.WaitKeyCloseWindows()                                        

        else:
            QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")

    # Function to Display Contour Area
    def get_contour_areas(self,contours):
         """returns the areas of all contours as list"""
         all_areas = []
         for contour in contours:
            area = cv2.contourArea(contour)
            all_areas.append(area)
         return all_areas
      
    # Functions for Sorting by Position
    def x_cord_contour(self,contours):
         """Returns the X cordinate for the contour"""
         Moment = cv2.moments(contours)  
         '''
         The cv2.moments() function in OpenCV is used to calculate all the moments (up to the third order) of a binary image or a contour. 
         These moments provide valuable information about the shape, size, and orientation of an object within an image. 
         Function Signature IN Python:
                                       M = cv2.moments(array, binaryImage=False)
         Parameters:
            array:
            This can be either a single-channel image (e.g., a grayscale image) or a NumPy array representing the contour points of an object. 
            If it is an image, it should be of type np.uint8, np.int32, or np.float32.
            binaryImage:
            This is an optional boolean parameter, used only if the input array is an image. 
            If set to True, all non-zero pixels in the image are treated as 1s, effectively binarizing the image for moment calculation. 
            If False (default), pixel intensities are used as weights.

         Return Value:
            The function returns a dictionary (M) containing various moment values. Some of the key moments include:
            m00:
                  This represents the area of the object (or the sum of pixel intensities if binaryImage is False).
            m10, m01:
                     These are used to calculate the centroid (center of mass) of the object.
                        Centroid X-coordinate: cX = M['m10'] / M['m00']
                        Centroid Y-coordinate: cY = M['m01'] / M['m00'] 
            mu20, mu02, mu11:
                              These are central moments, which are translation-invariant and provide information about the object's orientation and shape.
            nu20, nu02, nu11:
                              These are central normalized moments (Hu moments), which are both translation and scale-invariant, 
                              making them useful for shape description and recognition. 

         Applications:
                     cv2.moments() is widely used in computer vision for tasks such as:
                     Calculating the area of a detected object.
                     Finding the centroid (center of mass) of an object.
                     Analyzing the shape and orientation of objects.
                     Object recognition and classification based on shape features.
         '''
         # To avoid divided by zero error
         if Moment['m00'] != 0:
            return (int(Moment['m10']/Moment['m00']))
         else:
             return int(Moment['m10'])
          
    def label_contour_center(self,image, contour):
      """Places a red circle on the center of contours"""
      Moment = cv2.moments(contour)
      # To avoid divided by zero error
      cx = int(Moment['m10'])
      cy = int(Moment['m01']) 
      if Moment['m00'] != 0:
         cx = int(Moment['m10'] / Moment['m00'])
         cy = int(Moment['m01'] / Moment['m00'])
      # Draw the contour number on the image
      cv2.circle(image,(cx,cy), 10, (0,0,255), -1)
      return image
    
    # Find contours in Binary Image
    def SegmentationAndContours(self,text):
        if self.image is not None and self.imageName is not None and isinstance(self.image, np.ndarray):
            cv2.destroyAllWindows()
            cv2.imshow("Original", self.image) 
            blank_image = None
            gray = self.image
            if len(self.image.shape) > 2:
               # Create a black image with same dimensions as loaded Image
               blank_image = np.zeros((self.image.shape[0], self.image.shape[1], 3))
               # Grayscale
               gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            else:
               blank_image = np.zeros((self.image.shape[0], self.image.shape[1]))
            '''             
               The cv2.findContours() function in OpenCV is used to find contours in a binary image. 
               Contours are essentially the curves joining all continuous points (along the boundary), having the same color or intensity. 
               They represent the boundaries of objects within an image.
               Function Signature in Python:
                                          contours, hierarchy = cv2.findContours(Image, Retrieval Mode, Approximation Method[, contours[, hierarchy[, offset]]])
               Parameters:
                  image:
                  This is the source 8-bit single-channel image. 
                  It should be a binary image (black background, white foreground) where non-zero pixels are treated as 1 and zero pixels are treated as 0. 
                  You can typically obtain this by applying thresholding or Canny edge detection to a grayscale image.

               mode:
               This specifies the contour retrieval mode. Common modes include:
                  cv2.RETR_EXTERNAL: Retrieves only external or the extreme outer contours.
                  cv2.RETR_LIST: Retrieves all contours without establishing any hierarchical relationships. 
                  cv2.RETR_TREE: Retrieves all contours and reconstructs a full hierarchy of nested contours.
                  cv2.RETR_COMP: Retrieves all in a 2-level hierarchy 

               method:
                     This specifies the contour approximation method. Common methods include:
                        cv2.CHAIN_APPROX_NONE: Stores all contour points. 
                                                But we don't necessarily need all bounding points. 
                                                If the points form a straight line, we only need the start and ending points of that line.
                        cv2.CHAIN_APPROX_SIMPLE: Compresses horizontal, vertical, and diagonal segments and leaves only their end points, saving memory.

               Return Values:
                  contours:
                           A Python list of all the detected contours. 
                           Each individual contour is a NumPy array of (x,y) coordinates of the boundary points of the object.
                  hierarchy:
                           This is an optional output array containing information about the hierarchy of the contours 
                           (e.g., parent-child relationships for nested contours), depending on the chosen mode. 
         
               drawContours()
                        cv2.drawContours(image, contours, specific contour, color, thickness)
                        The contours parameter is the output from findContours
                        Specific contour relates to which contour to draw e.g. Contour[0], Contour[1]. To draw all contours, use -1
                        color - BGR 
                        thickness as it relates to line thickness 

               Note
                  If using OpenCV 3.X, findContours returns a 3rd argument which is ret (or a boolean indicating if the function was successfully run). 
                  If you're using OpenCV 3.X replace line _ with:
                  _, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                  The variable 'contours' are stored as a numpy array of (x,y) points that form the contour
                  While, 'hierarchy' describes the child-parent relationships between contours (i.e. contours within contours)           

               Typical Usage:
                  Load and Preprocess Image: Load an image and convert it to grayscale.
                  Binarization: Convert the grayscale image into a binary image using thresholding or Canny edge detection, 
                                 ensuring a black background and white foreground for optimal contour detection.
                  Find Contours: Call cv2.findContours() with the binary image and desired mode and method.
                  Process/Draw Contours: Iterate through the contours list to perform operations like calculating area, perimeter, 
                                          or drawing them on the original image using cv2.drawContours().
            '''
            match text:
                  case "Find Contours":                                       
                     # Find Canny Edges
                     edged = cv2.Canny(gray, 30, 200)
                     cv2.imshow('Canny Edges', edged)
                     
                     # Use a copy of image, since findContours alters the Image
                     copy = edged.copy()
                     # Finding Contours
                     contours, hierarchy = cv2.findContours(copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                     cv2.imshow('Canny Edges After Contouring', copy)

                     #Draw all contours over blank image
                     cv2.drawContours(blank_image, contours, -1, (0,255,0), 3)
                     cv2.imshow('All Contours over Blank Image', blank_image)

                     # Draw all contours over Original Image
                     # Use '-1' as the 3rd parameter to select all Indexes to draw all Contours
                     cv2.drawContours(self.image, contours, -1, (0,255,0), 3)
                     cv2.imshow('All Contours over Original Image', self.image) 
                     # Number of Contours Found 
                     QMessageBox.information(None, "Number of Contours", "Number of Contours found = " + str(len(contours)))                                
                     
                  case "Sort Contours by Area":
                     # Find Canny edges
                     edged = cv2.Canny(gray, 50, 200)
                     cv2.imshow('Canny Edges', edged)

                     # Find contours 
                     contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                     
                     # Sort contours large to small
                     sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
                     # If there are a lot of contours you can control the number of contours to show as below:
                     # sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]                   

                     # Iterate over Contours and Draw one at a time
                     for index , contour in enumerate(sorted_contours):
                        # Control number of Display to Avoid StackOverFlow by showing only first 10 Contours:
                        if index < 11:
                           try:
                              cv2.drawContours(self.image, [contour], -1, (0,255,0), 4)
                              # print(str(sorted_contours[index]) )
                              imageName = 'Contours area of ordered index: ' + str(index) + " added."
                              cv2.imshow(imageName, self.image)
                              if index < len(contours)-1:
                                 cv2.waitKey(0)
                           except:
                              print("error: " + str(index))
                     
                     message =  ""
                     if len(contours) > 10: message += "Only 10 of contours presented to Avoid Time Consuming Process!\n"
                     message += "Contor Areas before sorting =\n" + str(self.get_contour_areas(contours)) + "\nContor Areas after sorting =\n" + str(self.get_contour_areas(sorted_contours))                 
                     # Number of Contours + Areas of the Contours before and After Sorting
                     QMessageBox.information(None, "Number of Contours found = " + str(len(contours)), message)

                  case "Sort Contours Left to Right":                         
                     # Find Canny edges
                     edged = cv2.Canny(gray, 50, 200)
                     cv2.imshow('Canny Edges', edged)

                     # Find contours 
                     contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                     
                     orginal_image = self.image.copy()
                     # Places a red circle on the center of contours
                     for index, contour in enumerate(contours):
                         red = self.label_contour_center(self.image, contour)
                     
                     # Showing the Contour centers
                     cv2.imshow("Red circle on the center of contours", self.image)
                     
                     # Sort by left to right using x_cord_contour function located above
                     contours_left_to_right = sorted(contours, key = self.x_cord_contour, reverse = False)                      

                     # Labeling Contours left to right
                     for (index,contour)  in enumerate(contours_left_to_right):
                        # Control number of Display to Avoid StackOverFlow by showing only first 10 Contours:
                        if index < 11:
                           cv2.drawContours(orginal_image, [contour], -1, (0,0,255), 3)  
                           Moment = cv2.moments(contour)
                           # To avoid divided by zero error
                           cx = int(Moment['m10'])
                           cy = int(Moment['m01']) 
                           if Moment['m00'] != 0:
                              cx = int(Moment['m10'] / Moment['m00'])
                              cy = int(Moment['m01'] / Moment['m00'])                        
                           cv2.putText(orginal_image, str(index + 1), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                           cv2.imshow('Sorting Left to Right, order: ' + str(index + 1), orginal_image)
                           if index < len(contours)-1:
                                 cv2.waitKey(0)
                           #***Crop each contour and save these images***
                           #(x, y, w, h) = cv2.boundingRect(c)                          
                           #cropped_contour = orginal_image[y:y + h, x:x + w]
                           #image_name = "output_shape_number_" + str(i+1) + ".jpg"
                           #print(image_name)
                           #cv2.imwrite(image_name, cropped_contour)
                     
                     message =  ""
                     if len(contours) > 10: message += "Only 10 of contours presented to Avoid Time Consuming Process!\n"
                     else: message +=  "Number of Contours found = "+ str(len(contours))
                     # Number of Contours Found 
                     QMessageBox.information(None, "Number of Contours found = "+ str(len(contours)), message) 

                  case "Approximate Contours by ApproxPolyDP":
                     ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

                     # Find contours 
                     contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
                     copy = self.image.copy()

                     # Iterate through each contour 
                     for contour in contours:
                        cv2.drawContours(self.image, [contour], 0, (0, 255, 0), 2)
                        cv2.imshow('Contours over Image', self.image)

                     # Iterate through each contour and compute the approx contour
                     for contour in contours:
                        # Calculate accuracy as a percent of the contour perimeter
                        accuracy = 0.03 * cv2.arcLength(contour, True)
                        '''                        
                        cv2.approxPolyDP is an OpenCV function used to approximate a polygonal curve or contour with a simpler shape that has fewer vertices. 
                        It implements the Douglas-Peucker algorithm.
                        Purpose:
                        The primary purpose of cv2.approxPolyDP is to reduce the number of points in a contour while 
                        maintaining its general shape within a specified precision. This is useful for:

                           Simplifying complex contours: Reducing noise and irrelevant details in a contour.
                           Shape analysis: Making it easier to identify basic geometric shapes (e.g., rectangles, triangles) from more complex outlines.
                           Computational efficiency: Reducing the number of points to process in subsequent operations. 

                        Syntax in Python:
                                         approx_contour = cv2.approxPolyDP(curve, epsilon, closed)

                        Parameters:
                           curve: The input contour or polygonal curve. This is typically a NumPy array of points.
                           epsilon: A crucial parameter that specifies the approximation accuracy. 
                                    It represents the maximum distance between the original curve and its approximated version. 
                                    A smaller epsilon results in a more precise approximation with more points, 
                                    while a larger epsilon leads to a coarser approximation with fewer points. 
                                    This value is often calculated as a percentage of the contour's perimeter using cv2.arcLength().
                           closed: A boolean value indicating whether the input curve is closed (e.g., a contour) or open (e.g., a line segment). 
                                   Set to True for closed contours and False for open curves.

                        Return Value:
                           approx_contour: A NumPy array representing the approximated contour with fewer vertices. These are the (x, y) coordinates of the simplified shape.
                        '''
                        approx = cv2.approxPolyDP(contour, accuracy, True)
                        cv2.drawContours(copy, [approx], 0, (0, 255, 0), 2)
                        cv2.imshow('Approx Poly DP', copy)

                  case "Approximate Contours by ConvexHull":
                     # Threshold the image
                     ret, thresh = cv2.threshold(gray, 176, 255, 0)

                     # Find contours 
                     contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
                        
                     # Sort Contors by area and then remove the largest frame contour
                     n = len(contours) - 1
                     contours = sorted(contours, key=cv2.contourArea, reverse=False)[:n]

                     # Iterate through contours and draw the convex hull
                     for contour in contours:
                        '''                        
                        The cv2.convexHull() function in OpenCV is used to find the convex hull of a point set or a contour. 
                        The convex hull of a set of points is the smallest convex polygon that contains all the points. 
                        Imagine stretching a rubber band around a group of scattered nails; the shape formed by the tightened rubber band represents the convex hull.
                        Syntax in Python:
                                        hull = cv2.convexHull(points, hull=None, clockwise=None, returnPoints=None)

                        Parameters:
                           points:
                                 This is the input array of 2D points or a contour (a NumPy array of points).
                           hull:
                               (Optional) This is the output hull array. 
                               If returnPoints=False, it will contain the indices of the hull points from the original points array. 
                               If returnPoints=True, it will contain the coordinates of the hull points.
                           clockwise:
                                   (Optional) A boolean flag. If True, the output convex hull points are ordered in a clockwise direction. 
                                   Otherwise, they are ordered counter-clockwise. The default is False (counter-clockwise).
                           returnPoints:
                                       (Optional) A boolean flag. If True (default), the function returns the coordinates of the convex hull points. 
                                       If False, it returns the indices of the convex hull points within the input points array.

                        Return Value:
                                   The function returns the hull array, which contains either the coordinates of the convex hull points or 
                                   their indices, depending on the returnPoints parameter.
                        '''
                        hull = cv2.convexHull(contour)
                        cv2.drawContours(self.image, [hull], 0, (0, 255, 0), 2)
                        cv2.imshow('Convex Hull', self.image)
        
            self.WaitKeyCloseWindows() 

        else:
            QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
        
    #
    def ObjectDetection(self,text):
         print(text)
         match text:
               case "Line Detection using HoughLines":
                  print("")
               case "Line Detection using Probablistic HoughLines":
                  print("")
               case "Circle Detection using HoughCircles":
                  print("")
               case "Blob Detection":
                  print("")
               case "Face and Eye Detection with HAAR Cascade Classifiers":
                  print("")
               case "Live Face and Eye Detection with HAAR Cascade Classifiers":
                  print("")
               case "Live People Detection with HAAR Cascade Classifiers":
                  print("")
               case "Live Car Detection with HAAR Cascade Classifiers":
                  print("")

    #
    def OpticalCharacterRecognition(self,text):
         print(text)
         match text:
               case "OCR by Tesseract":
                  print("")