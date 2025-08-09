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
        self.tempImageName = None

    # Consider|Attention: 
    # Here all parameters Assigned have relation to Image Dimensions for Visibility of Changes > image.shape = (height,width,depth)

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
                  name = "BackScaled" + str(coefficient) + "Times"
                  ScaledImageName = name + "_" + self.imageName
                  self.tempImage = ScaledImage
                  self.tempImageName = ScaledImageName
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
                  self.tempImage = RotatedImage
                  self.tempImageName = RotatedImageName
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
            TranslatedImageName = name + "Translation_" + self.imageName
            self.ImageSizeChanged.emit(name)
            self.tempImage = TranslatedImage
            self.tempImageName = TranslatedImageName
            cv2.imshow(self.imageName,self.image)
            cv2.imshow(TranslatedImageName,TranslatedImage)
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
            cv2.imshow(self.imageName, self.image)
            cv2.imshow(croppedImageName, croppedImage) 
            self.WaitKeyCloseWindows()

    # Add Text to Image
    def AddText(self,text):
        # Check if Image does not Exist then Create a Colored Image
        if self.image is None or self.imageName is None or not isinstance(self.image, np.ndarray): 
           self.image = np.zeros((800,600,3), np.uint8) 
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
       
    # Draw Some Shapes
    def DrawShape(self,shape): 
        # Check if Image does not Exist then Create a Colored Image
        if self.image is None or self.imageName is None or not isinstance(self.image, np.ndarray): 
           self.image = np.zeros((800,600,3), np.uint8) 

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
              
            
        
        
        