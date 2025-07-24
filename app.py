#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# -*- Encoding: utf-8 -*- #
"""
@Author | Developer: Mehrdad Ahady
"""
import os
from os import path
import sys
import cv2
import PyQt6
import PyQt6.QtCore
from functools import partial
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMenu, QMainWindow, QApplication, QWidget
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEngineProfile
from utils.CustomPDFView import CustomPdfView

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
        self.page_AboutTool = QtWidgets.QWidget()
        self.page_AboutTool.setObjectName("page_AboutTool")
        self.text_AboutTool = QtWidgets.QTextBrowser(parent=self.page_AboutTool)
        self.text_AboutTool.setGeometry(QtCore.QRect(5, 1, 991, 711))
        self.text_AboutTool.setObjectName("text_AboutTool")
        self.pages.addWidget(self.page_AboutTool)
        self.page_AboutAuthorDeveloper = QtWidgets.QWidget()
        self.page_AboutAuthorDeveloper.setObjectName("page_AboutAuthorDeveloper")
        self.text_AboutAuthorDeveloper = QtWidgets.QTextBrowser(parent=self.page_AboutAuthorDeveloper)
        self.text_AboutAuthorDeveloper.setGeometry(QtCore.QRect(5, 1, 991, 711))
        self.text_AboutAuthorDeveloper.setObjectName("text_AboutAuthorDeveloper")
        self.pages.addWidget(self.page_AboutAuthorDeveloper)
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
        self.menu_PreRequisites = QMenu(parent=MainWindow)  #**********************************
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(".\\icons/n1.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_PreRequisites.setIcon(icon7)
        self.menu_PreRequisites.setObjectName("menu_PreRequisites")
        self.menu_FundamentalOfComputerVision = QMenu(parent=MainWindow)  #**********************************
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(".\\icons/n3.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_FundamentalOfComputerVision.setIcon(icon8)
        self.menu_FundamentalOfComputerVision.setObjectName("menu_FundamentalOfComputerVision")
        self.menu_Machine_Learning_Model_Fundamentals = QMenu(parent=MainWindow)  #**********************************
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(".\\icons/n2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_Machine_Learning_Model_Fundamentals.setIcon(icon9)
        self.menu_Machine_Learning_Model_Fundamentals.setObjectName("menu_Machine_Learning_Model_Fundamentals")
        self.menu_Deep_Learning_Foundations = QMenu(parent=MainWindow)  #**********************************
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(".\\icons/n4.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_Deep_Learning_Foundations.setIcon(icon10)
        self.menu_Deep_Learning_Foundations.setObjectName("menu_Deep_Learning_Foundations")
        self.menu_Core_CV_Computer_Vision_Tasks = QMenu(parent=MainWindow)  #**********************************
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(".\\icons/n5.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_Core_CV_Computer_Vision_Tasks.setIcon(icon11)
        self.menu_Core_CV_Computer_Vision_Tasks.setObjectName("menu_Core_CV_Computer_Vision_Tasks")
        self.menu_Advanced_Generative_Models_Architectures = QMenu(parent=MainWindow)  #**********************************
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(".\\icons/n6.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_Advanced_Generative_Models_Architectures.setIcon(icon12)
        self.menu_Advanced_Generative_Models_Architectures.setObjectName("menu_Advanced_Generative_Models_Architectures")
        self.menu_Applications_Deployment_Optimization = QMenu(parent=MainWindow)  #**********************************
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(".\\icons/n7.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_Applications_Deployment_Optimization.setIcon(icon13)
        self.menu_Applications_Deployment_Optimization.setObjectName("menu_Applications_Deployment_Optimization")
        self.menu_Ethics_Explainability_and_Portfolios = QMenu(parent=MainWindow)  #**********************************
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(".\\icons/n8.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_Ethics_Explainability_and_Portfolios.setIcon(icon14)
        self.menu_Ethics_Explainability_and_Portfolios.setObjectName("menu_Ethics_Explainability_and_Portfolios")
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
        #
        self.menuLab.addMenu(self.menu_PreRequisites)  #*************************************
        self.menuLab.addSeparator()
        self.menuLab.addMenu(self.menu_Machine_Learning_Model_Fundamentals)#*************************************
        self.menuLab.addSeparator()
        self.menuLab.addMenu(self.menu_FundamentalOfComputerVision) #*************************************
        self.menuLab.addSeparator()
        self.menuLab.addMenu(self.menu_Deep_Learning_Foundations) #*************************************
        self.menuLab.addSeparator()
        self.menuLab.addMenu(self.menu_Core_CV_Computer_Vision_Tasks) #*************************************
        self.menuLab.addSeparator()
        self.menuLab.addMenu(self.menu_Advanced_Generative_Models_Architectures) #*************************************
        self.menuLab.addSeparator()
        self.menuLab.addMenu(self.menu_Applications_Deployment_Optimization) #*************************************
        self.menuLab.addSeparator()
        self.menuLab.addSeparator()
        self.menuLab.addMenu(self.menu_Ethics_Explainability_and_Portfolios) #*************************************
        #
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
        self.menu_FundamentalOfComputerVision.setTitle(_translate("MainWindow", "Fundamental of Computer Vision"))  #****************************
        self.menu_Machine_Learning_Model_Fundamentals.setTitle(_translate("MainWindow", "Machine Learning Model Fundamentals"))  #*******************************
        self.menu_Deep_Learning_Foundations.setTitle(_translate("MainWindow", "Deep Learning Foundations"))  #*******************************
        self.menu_Core_CV_Computer_Vision_Tasks.setTitle(_translate("MainWindow", "Core CV (Computer Vision) Tasks"))  #*******************************
        self.menu_Advanced_Generative_Models_Architectures.setTitle(_translate("MainWindow", "Advanced & Generative Models & Architectures"))  #*******************************
        self.menu_Applications_Deployment_Optimization.setTitle(_translate("MainWindow", "Applications Deployment & Optimization"))  #*******************************
        self.menu_Ethics_Explainability_and_Portfolios.setTitle(_translate("MainWindow", "Ethics, Explainability, and Portfolios"))  #*******************************
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.menu_Mathematics.setTitle(_translate("MainWindow", "🧮 Mathematics"))
        self.action_LinearAlgebraAndCalculus.setText(_translate("MainWindow", "📊 Linear Algebra and Calculus"))
        self.action_ProbabilityAndStatistics.setText(_translate("MainWindow", "📉 Probability and Statistics"))
        self.action_PythonProgramming.setText(_translate("MainWindow", "🐍 Base of Python Programming"))
        self.action_CoreMachineLearningPrinciples.setTitle(_translate("MainWindow", "🧠 Core Machine Learning Principles"))
        self.action_CategorizingByLearningParadigm.setText(_translate("MainWindow", "🗂️ Categorizing by Learning Paradigm"))
        self.action_FromFundamentalsToAdvanced.setText(_translate("MainWindow", "🔍 From Fundamentals to Advanced"))
        self.action_MLModelOverview.setText(_translate("MainWindow", "🌌 ML Model Overview"))
        self.action_CoreMLModelFormatSpecification.setText(_translate("MainWindow", "📚 Core ML Model Format Specification"))
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<     
#############################################################################
    def html_in_window(self,path):
      #  path = os.path.abspath(path)
        self.webView.setUrl(QUrl(path))
        #self.webView.load(QUrl.fromLocalFile(path))
        self.webView.show()

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
                  self.pdf_path = os.path.relpath("pages/CategorizingByLearningParadigm.pdf")
             case 7:
                  self.pdf_path = os.path.relpath("pages/FromFundamentalsToAdvanced.pdf")
                  
        self.pdf_document.load(self.pdf_path)
        self.pdf_view.pdf_path = self.pdf_path
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.pdf_document = self.pdf_document 
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def pdf_in_browser(self,pdf_path,local):
        if local == True:
           pdf_path = os.path.relpath(pdf_path)
           QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(pdf_path))
        else:
            QDesktopServices.openUrl(QUrl(pdf_path))

    def connectActions(self):
        self.action_BigPicture.triggered.connect(partial(self.changePDFPage,0))
        self.action_UniversityCurriculum.triggered.connect(partial(self.changePDFPage,1))
        self.action_RoadMap.triggered.connect(partial(self.changePDFPage,2))
        self.action_StudyPlan.triggered.connect(partial(self.changePDFPage,3))
        self.action_HeadingResearch.triggered.connect(partial(self.changePDFPage,4))
        self.action_UserGuide.triggered.connect(partial(self.changePDFPage,5))
        self.action_CategorizingByLearningParadigm.triggered.connect(partial(self.changePDFPage,6))
        self.action_FromFundamentalsToAdvanced.triggered.connect(partial(self.changePDFPage,7))

        self.action_AboutTool.triggered.connect(self.changePage)
        self.action_AboutAuthorDeveloper.triggered.connect(self.changePage)
        self.action_CloseOtherWindows.triggered.connect(self.closeWindow)
        self.action_CloseMainWindow.triggered.connect(self.closeWindow)
        self.action_CloseAllWindows.triggered.connect(self.closeWindow)
        self.action_PythonProgramming.triggered.connect(self.changePage)
        self.action_LinearAlgebraAndCalculus.triggered.connect(self.changePage)
        self.action_ProbabilityAndStatistics.triggered.connect(self.changePage)
        
        #self.action_PythonProgramming.triggered.connect(partial(self.html_in_window,"https://www.w3schools.com/python/default.asp"))
        #self.action_LinearAlgebraAndCalculus.triggered.connect(partial(self.html_in_window,"https://github.com/Ryota-Kawamura/Mathematics-for-Machine-Learning-and-Data-Science-Specialization"))
        #self.action_ProbabilityAndStatistics.triggered.connect(partial(self.pdf_in_browser,"./pages/Mathematics_for_Machine_Learning_mml_book.pdf",True))
        self.action_ProbabilityAndStatistics.triggered.connect(partial(self.pdf_in_browser,"https://mml-book.github.io/book/mml-book.pdf",False))
        self.action_PythonProgramming.triggered.connect(partial(self.pdf_in_browser,"https://www.w3schools.com/python/default.asp",False))
        self.action_LinearAlgebraAndCalculus.triggered.connect(partial(self.pdf_in_browser,"https://github.com/Ryota-Kawamura/Mathematics-for-Machine-Learning-and-Data-Science-Specialization",False))
        self.action_MLModelOverview.triggered.connect(partial(self.pdf_in_browser,"https://apple.github.io/coremltools/docs-guides/source/mlmodel.html",False))
        self.action_CoreMLModelFormatSpecification.triggered.connect(partial(self.pdf_in_browser,"https://apple.github.io/coremltools/mlmodel/index.html",False))

    def changePage(self):
        #print(self.sender().objectName())
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
    
    def load_html_file(self,file_path):
        with open(file_path, 'r') as f: #, encoding='utf-8'
            return f.read()

    def on_cert_error(self,e):
            # print(f"cert error: {e.description()}")
            # print(f"type: {e.type()}")
            # print(f"overridable: {e.isOverridable()}")
            # print(f"url: {e.url()}")
            # for c in e.certificateChain():
            #     print(c.toText())
            e.acceptCertificate()
            e.ignoreCertificateError()
            return True

    def manualSetup(self):
        self.action_PythonProgramming = QtGui.QAction(parent=MainWindow)  
        self.action_PythonProgramming.setObjectName("action_PythonProgramming")
        self.menu_PreRequisites.addAction(self.action_PythonProgramming)
        self.menu_Mathematics = QMenu(parent=MainWindow)  
        self.menu_Mathematics.setObjectName("menu_Mathematics")
        self.menu_PreRequisites.addMenu(self.menu_Mathematics)
        self.action_LinearAlgebraAndCalculus = QtGui.QAction(parent=MainWindow)
        self.action_LinearAlgebraAndCalculus.setObjectName("action_LinearAlgebraAndCalculus")    
        self.menu_Mathematics.addAction(self.action_LinearAlgebraAndCalculus)
        self.action_ProbabilityAndStatistics = QtGui.QAction(parent=MainWindow)
        self.action_ProbabilityAndStatistics.setObjectName("action_ProbabilityAndStatistics")    
        self.menu_Mathematics.addAction(self.action_ProbabilityAndStatistics)
        
        self.action_CoreMachineLearningPrinciples = QMenu(parent=MainWindow)  
        self.action_CoreMachineLearningPrinciples.setObjectName("action_CoreMachineLearningPrinciples")
        self.menu_PreRequisites.addMenu(self.action_CoreMachineLearningPrinciples)
        self.action_CategorizingByLearningParadigm = QtGui.QAction(parent=MainWindow)
        self.action_CategorizingByLearningParadigm.setObjectName("action_CategorizingByLearningParadigm")    
        self.action_CoreMachineLearningPrinciples.addAction(self.action_CategorizingByLearningParadigm)
        self.action_FromFundamentalsToAdvanced = QtGui.QAction(parent=MainWindow)
        self.action_FromFundamentalsToAdvanced.setObjectName("action_FromFundamentalsToAdvanced")    
        self.action_CoreMachineLearningPrinciples.addAction(self.action_FromFundamentalsToAdvanced)

        self.action_MLModelOverview = QtGui.QAction(parent=MainWindow)  
        self.action_MLModelOverview.setObjectName("action_MLModelOverview")
        self.menu_Machine_Learning_Model_Fundamentals.addAction(self.action_MLModelOverview)
        self.action_CoreMLModelFormatSpecification = QtGui.QAction(parent=MainWindow)  
        self.action_CoreMLModelFormatSpecification.setObjectName("action_CoreMLModelFormatSpecification")
        self.menu_Machine_Learning_Model_Fundamentals.addAction(self.action_CoreMLModelFormatSpecification)

        self.pdf_view = CustomPdfView(self.pages)
        self.pdf_document = QPdfDocument(self.pdf_view)
        self.pages.addWidget(self.pdf_view)
      
        AboutAuthorDeveloper = self.load_html_file(os.path.relpath("pages/Text_AboutAuthorDeveloper.html"))
        self.text_AboutAuthorDeveloper.setHtml(AboutAuthorDeveloper)
        self.text_AboutAuthorDeveloper.setStyleSheet("padding:10px")
        AboutTool = self.load_html_file(os.path.relpath("pages/Text_AboutTool.html"))
        self.text_AboutTool.setHtml(AboutTool)
        self.text_AboutTool.setStyleSheet("padding:10px")
        self.pages.setCurrentWidget(self.page_AboutTool)

        self.webView = QWebEngineView(parent=None)
        self.webView.setObjectName("Python Programming")
        self.webView.setWindowTitle("Python Programming")
        self.webView.resize(1024, 768)
        self.webView.setMinimumSize(QtCore.QSize(1024, 768))
        self.webView.setBaseSize(QtCore.QSize(1024, 768))
        self.webView.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        profile = QWebEngineProfile.defaultProfile() 
        webpage = QWebEnginePage(profile, self.webView)
        self.webView.setPage(webpage)
        settings = self.webView.page().settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, True)
        self.webView.setContextMenuPolicy(PyQt6.QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.webView.page().certificateError.connect(self.on_cert_error)

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
