#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# -*- Encoding: utf-8 -*- #
"""
@Author | Developer: Mehrdad Ahady
"""
import os
import sys
import cv2
from functools import partial
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog,QMenu,QApplication, QMainWindow, QWidget
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from utils.Custom_PDF_View import CustomPdfView

class Ui_MainWindow(QMainWindow,object):
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 768))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 768))
        MainWindow.setBaseSize(QtCore.QSize(1024, 768))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\icons/eye.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.container = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.container.sizePolicy().hasHeightForWidth())
        self.container.setSizePolicy(sizePolicy)
        self.container.setMinimumSize(QtCore.QSize(1024, 714))
        self.container.setMaximumSize(QtCore.QSize(1024, 714))
        self.container.setBaseSize(QtCore.QSize(1024, 714))
        self.container.setObjectName("container")
        self.pages = QtWidgets.QStackedWidget(parent=self.container)
        self.pages.setGeometry(QtCore.QRect(10, 0, 1011, 711))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pages.sizePolicy().hasHeightForWidth())
        self.pages.setSizePolicy(sizePolicy)
        self.pages.setMinimumSize(QtCore.QSize(1011, 711))
        self.pages.setMaximumSize(QtCore.QSize(1011, 711))
        self.pages.setBaseSize(QtCore.QSize(1011, 711))
        self.pages.setObjectName("pages")
        self.page_PythonProgramming = QtWidgets.QWidget()
        self.page_PythonProgramming.setObjectName("page_PythonProgramming")
        self.label_3 = QtWidgets.QLabel(parent=self.page_PythonProgramming)
        self.label_3.setGeometry(QtCore.QRect(290, 120, 261, 16))
        self.label_3.setObjectName("label_3")
        self.pages.addWidget(self.page_PythonProgramming)
        self.page_ProbabilityAndStatistics = QtWidgets.QWidget()
        self.page_ProbabilityAndStatistics.setObjectName("page_ProbabilityAndStatistics")
        self.label_2 = QtWidgets.QLabel(parent=self.page_ProbabilityAndStatistics)
        self.label_2.setGeometry(QtCore.QRect(250, 120, 261, 16))
        self.label_2.setObjectName("label_2")
        self.pages.addWidget(self.page_ProbabilityAndStatistics)
        self.page_LinearAlgebraAndCalculus = QtWidgets.QWidget()
        self.page_LinearAlgebraAndCalculus.setObjectName("page_LinearAlgebraAndCalculus")
        self.label = QtWidgets.QLabel(parent=self.page_LinearAlgebraAndCalculus)
        self.label.setGeometry(QtCore.QRect(160, 60, 381, 16))
        self.label.setObjectName("label")
        self.pages.addWidget(self.page_LinearAlgebraAndCalculus)
        MainWindow.setCentralWidget(self.container)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 33))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuTopics = QtWidgets.QMenu(parent=self.menubar)
        font = QtGui.QFont()
        font.setBold(False)
        self.menuTopics.setFont(font)
        self.menuTopics.setObjectName("menuTopics")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuControls = QtWidgets.QMenu(parent=self.menubar)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.menuControls.setFont(font)
        self.menuControls.setObjectName("menuControls")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuLab = QtWidgets.QMenu(parent=self.menubar)
        self.menuLab.setObjectName("menuLab")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_CloseOtherWindows = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\icons/c1.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_CloseOtherWindows.setIcon(icon1)
        self.action_CloseOtherWindows.setObjectName("action_CloseOtherWindows")
        self.action_CloseMainWindow = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(".\\icons/c2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_CloseMainWindow.setIcon(icon2)
        self.action_CloseMainWindow.setObjectName("action_CloseMainWindow")
        self.action_CloseAllWindows = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(".\\icons/c3.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_CloseAllWindows.setIcon(icon3)
        self.action_CloseAllWindows.setObjectName("action_CloseAllWindows")
        self.action_AboutTool = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(".\\icons/about.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_AboutTool.setIcon(icon4)
        self.action_AboutTool.setObjectName("action_AboutTool")
        self.action_AboutAuthorDeveloper = QtGui.QAction(parent=MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(".\\icons/dev.jpg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_AboutAuthorDeveloper.setIcon(icon5)
        self.action_AboutAuthorDeveloper.setObjectName("action_AboutAuthorDeveloper")
        self.action_UniversityCurriculum = QtGui.QAction(parent=MainWindow)
        self.action_UniversityCurriculum.setObjectName("action_UniversityCurriculum")
        self.action_BigPicture = QtGui.QAction(parent=MainWindow)
        self.action_BigPicture.setObjectName("action_BigPicture")
        self.action_RoadMap = QtGui.QAction(parent=MainWindow)
        self.action_RoadMap.setObjectName("action_RoadMap")
        self.action_StudyPlan = QtGui.QAction(parent=MainWindow)
        self.action_StudyPlan.setObjectName("action_StudyPlan")
        self.action_HeadingResearch = QtGui.QAction(parent=MainWindow)
        self.action_HeadingResearch.setObjectName("action_HeadingResearch")
        self.action_UserGuide = QtGui.QAction(parent=MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(".\\icons/help.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_UserGuide.setIcon(icon6)
        self.action_UserGuide.setObjectName("action_UserGuide")
        self.menu_PreRequisites = QMenu(parent=MainWindow)     #**********************************
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(".\\icons/n1.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_PreRequisites.setIcon(icon7)
        self.menu_PreRequisites.setObjectName("menu_PreRequisites")
        self.menu_FundamentalOfComputerVision = QMenu(parent=MainWindow)  #********************************
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(".\\icons/n2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_FundamentalOfComputerVision.setIcon(icon8)
        self.menu_FundamentalOfComputerVision.setObjectName("menu_FundamentalOfComputerVision")
        self.menuTopics.addSeparator()
        self.menuTopics.addSeparator()
        self.menuTopics.addAction(self.action_BigPicture)
        self.menuTopics.addSeparator()
        self.menuTopics.addAction(self.action_UniversityCurriculum)
        self.menuTopics.addSeparator()
        self.menuTopics.addAction(self.action_RoadMap)
        self.menuTopics.addSeparator()
        self.menuTopics.addAction(self.action_StudyPlan)
        self.menuTopics.addSeparator()
        self.menuTopics.addAction(self.action_HeadingResearch)
        self.menuSettings.addSeparator()
        self.menuSettings.addSeparator()
        self.menuControls.addAction(self.action_CloseOtherWindows)
        self.menuControls.addSeparator()
        self.menuControls.addAction(self.action_CloseMainWindow)
        self.menuControls.addSeparator()
        self.menuControls.addAction(self.action_CloseAllWindows)
        self.menuHelp.addAction(self.action_UserGuide)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.action_AboutTool)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.action_AboutAuthorDeveloper)
        self.menuHelp.addSeparator()
        self.menuLab.addMenu(self.menu_PreRequisites)  #*************************************
        self.menuLab.addSeparator()
        self.menuLab.addMenu(self.menu_FundamentalOfComputerVision) #*************************************
        self.menubar.addAction(self.menuTopics.menuAction())
        self.menubar.addAction(self.menuLab.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuControls.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>          
        self.manualSetup()
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Computer Vision with Machine Learning and Deep Learning"))
        self.label_3.setText(_translate("MainWindow", "PythonProgramming"))
        self.label_2.setText(_translate("MainWindow", "ProbabilityAndStatistics"))
        self.label.setText(_translate("MainWindow", "LinearAlgebraAndCalculus"))
        self.menuTopics.setTitle(_translate("MainWindow", "Topics"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuControls.setTitle(_translate("MainWindow", "Controls"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuLab.setTitle(_translate("MainWindow", "Lab"))
        self.action_CloseOtherWindows.setText(_translate("MainWindow", "Close Other Windows"))
        self.action_CloseMainWindow.setText(_translate("MainWindow", "Close Main Window"))
        self.action_CloseAllWindows.setText(_translate("MainWindow", "Close All Windows"))
        self.action_AboutTool.setText(_translate("MainWindow", "About Tool"))
        self.action_AboutAuthorDeveloper.setText(_translate("MainWindow", "About Author | Developer"))
        self.action_UniversityCurriculum.setText(_translate("MainWindow", "📗 University Curriculum"))
        self.action_BigPicture.setText(_translate("MainWindow", "📘 Big Picture"))
        self.action_RoadMap.setText(_translate("MainWindow", "📕 Road Map"))
        self.action_StudyPlan.setText(_translate("MainWindow", "📙 Study Plan"))
        self.action_StudyPlan.setToolTip(_translate("MainWindow", "Study Plan"))
        self.action_HeadingResearch.setText(_translate("MainWindow", "📒 Heading Research"))
        self.action_HeadingResearch.setToolTip(_translate("MainWindow", "Heading Research"))
        self.action_UserGuide.setText(_translate("MainWindow", "User Guide"))
        self.action_UserGuide.setToolTip(_translate("MainWindow", "Help"))
        self.menu_PreRequisites.setTitle(_translate("MainWindow", "Pre Requisites"))  #*******************************
        self.menu_FundamentalOfComputerVision.setTitle(_translate("MainWindow", "Fundamental of Computer Vision"))  #**************************
         #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.menu_Mathematics.setTitle(_translate("MainWindow", "🧮 Mathematics"))
        self.action_LinearAlgebraAndCalculus.setText(_translate("MainWindow", "📊 Linear Algebra and Calculus"))
        self.action_ProbabilityAndStatistics.setText(_translate("MainWindow", "📉 Probability and Statistics"))
        self.action_PythonProgramming.setText(_translate("MainWindow", "🐍 Python Programming"))
        self.action_CoreMachineLearningPrinciples.setText(_translate("MainWindow", "🧠 Core Machine Learning Principles"))
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#############################################################################
    def changePDFPage(self,index):
        self.pages.setCurrentWidget(self.pdf_view)
        self.pdf_path = ""
        match index: 
             case 0:
                  self.pdf_path = os.path.relpath("pages/BigPicture.pdf")
             case 1:
                  self.pdf_path = os.path.relpath("pages/UniversityCurriculum.pdf")
             case 2:
                  self.pdf_path = os.path.relpath("pages/RoadMap.pdf")
             case 3:
                  self.pdf_path = os.path.relpath("pages/StudyPlan.pdf")
             case 4:
                  self.pdf_path = os.path.relpath("pages/HeadingResearch.pdf")
             case 5:
                  self.pdf_path = os.path.relpath("pages/UserGuide.pdf")
             case 6:
                  self.pdf_path = os.path.relpath("pages/AboutTool.pdf")
             case 7:
                  self.pdf_path = os.path.relpath("pages/AboutAuthorDeveloper.pdf")
                  
        self.pdf_document.load(self.pdf_path)
        self.pdf_view.pdf_path = self.pdf_path
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.pdf_document = self.pdf_document 
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def connectActions(self):
        self.action_BigPicture.triggered.connect(partial(self.changePDFPage,0))
        self.action_UniversityCurriculum.triggered.connect(partial(self.changePDFPage,1))
        self.action_RoadMap.triggered.connect(partial(self.changePDFPage,2))
        self.action_StudyPlan.triggered.connect(partial(self.changePDFPage,3))
        self.action_HeadingResearch.triggered.connect(partial(self.changePDFPage,4))
        self.action_UserGuide.triggered.connect(partial(self.changePDFPage,5))
        self.action_AboutTool.triggered.connect(partial(self.changePDFPage,6))
        self.action_AboutAuthorDeveloper.triggered.connect(partial(self.changePDFPage,7))
        self.action_CloseOtherWindows.triggered.connect(self.closeWindow)
        self.action_CloseMainWindow.triggered.connect(self.closeWindow)
        self.action_CloseAllWindows.triggered.connect(self.closeWindow)
        self.action_PythonProgramming.triggered.connect(self.changePage)
        self.action_LinearAlgebraAndCalculus.triggered.connect(self.changePage)
        self.action_ProbabilityAndStatistics.triggered.connect(self.changePage)

    def changePage(self):
        selectedPage = self.pages.findChild(QtWidgets.QWidget,"page_" + self.sender().objectName().split("_")[1])
        if selectedPage != None:
           self.pages.setCurrentWidget(selectedPage)

    def closeWindow(self):
        match self.sender().objectName():
             case "action_CloseOtherWindows":
                  self.lower()
                  cv2.destroyAllWindows()
             case "action_CloseMainWindow":
                  MainWindow.close()
                  MainWindow.destroy()
                  self.close()
                  self.destroy()
             case "action_CloseAllWindows":
                  self.lower()
                  cv2.destroyAllWindows()
                  MainWindow.close()
                  MainWindow.destroy()
                  self.close()
                  self.destroy()                

    def manualSetup(self):
        self.menu_Mathematics = QMenu(parent=MainWindow)  
        self.menu_Mathematics.setObjectName("menu_Mathematics")
        self.menu_PreRequisites.addMenu(self.menu_Mathematics)
        self.action_LinearAlgebraAndCalculus = QtGui.QAction(parent=MainWindow)
        self.action_LinearAlgebraAndCalculus.setObjectName("action_LinearAlgebraAndCalculus")    
        self.menu_Mathematics.addAction(self.action_LinearAlgebraAndCalculus)
        self.action_ProbabilityAndStatistics = QtGui.QAction(parent=MainWindow)
        self.action_ProbabilityAndStatistics.setObjectName("action_ProbabilityAndStatistics")    
        self.menu_Mathematics.addAction(self.action_ProbabilityAndStatistics)
        self.action_PythonProgramming = QtGui.QAction(parent=MainWindow)  
        self.action_PythonProgramming.setObjectName("action_PythonProgramming")
        self.menu_PreRequisites.addAction(self.action_PythonProgramming)
        self.action_CoreMachineLearningPrinciples = QtGui.QAction(parent=MainWindow)  
        self.action_CoreMachineLearningPrinciples.setObjectName("action_CoreMachineLearningPrinciples")
        self.menu_PreRequisites.addAction(self.action_CoreMachineLearningPrinciples)

        self.pdf_view = CustomPdfView(self.pages)
        self.pdf_document = QPdfDocument(self.pdf_view)
        self.pages.addWidget(self.pdf_view)
        self.pages.setCurrentWidget(self.pdf_view)
        self.changePDFPage(6)
        self.connectActions()   
#############################################################################

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
