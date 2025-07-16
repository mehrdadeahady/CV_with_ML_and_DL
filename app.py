#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# -*- Encoding: utf-8 -*- #
"""
@Author | Developer: Mehrdad Ahady
"""
import sys
from functools import partial
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
import sys

import cv2

class Ui_MainWindow(QMainWindow,object):
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1025, 768)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\icons/eye.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.container = QtWidgets.QWidget(parent=MainWindow)
        self.container.setObjectName("container")
        self.pages = QtWidgets.QStackedWidget(parent=self.container)
        self.pages.setGeometry(QtCore.QRect(10, 0, 1011, 711))
        self.pages.setObjectName("pages")
        self.page_BigPicture = QtWidgets.QWidget()
        self.page_BigPicture.setObjectName("page_BigPicture")
        self.Text_BigPicture = QtWidgets.QTextEdit(parent=self.page_BigPicture)
        self.Text_BigPicture.setGeometry(QtCore.QRect(10, 0, 981, 711))
        self.Text_BigPicture.setAutoFillBackground(False)
        self.Text_BigPicture.setObjectName("Text_BigPicture")
        self.pages.addWidget(self.page_BigPicture)
        self.pageTopics_UniversityCurriculum = QtWidgets.QWidget()
        self.pageTopics_UniversityCurriculum.setObjectName("pageTopics_UniversityCurriculum")
        self.Text_UniversityCurriculum = QtWidgets.QTextEdit(parent=self.pageTopics_UniversityCurriculum)
        self.Text_UniversityCurriculum.setGeometry(QtCore.QRect(10, 0, 981, 711))
        self.Text_UniversityCurriculum.setObjectName("Text_UniversityCurriculum")
        self.pages.addWidget(self.pageTopics_UniversityCurriculum)
        self.pageTopics_RoadMap = QtWidgets.QWidget()
        self.pageTopics_RoadMap.setObjectName("pageTopics_RoadMap")
        self.Text_RoadMap = QtWidgets.QTextEdit(parent=self.pageTopics_RoadMap)
        self.Text_RoadMap.setGeometry(QtCore.QRect(10, 0, 981, 711))
        self.Text_RoadMap.setObjectName("Text_RoadMap")
        self.pages.addWidget(self.pageTopics_RoadMap)
        self.pageTopics_StudyPlan = QtWidgets.QWidget()
        self.pageTopics_StudyPlan.setObjectName("pageTopics_StudyPlan")
        self.Text_StudyPlan = QtWidgets.QTextEdit(parent=self.pageTopics_StudyPlan)
        self.Text_StudyPlan.setGeometry(QtCore.QRect(10, 0, 981, 711))
        self.Text_StudyPlan.setObjectName("Text_StudyPlan")
        self.pages.addWidget(self.pageTopics_StudyPlan)
        self.pageTopics_HeadingResearch = QtWidgets.QWidget()
        self.pageTopics_HeadingResearch.setObjectName("pageTopics_HeadingResearch")
        self.Text_HeadingResearch = QtWidgets.QTextEdit(parent=self.pageTopics_HeadingResearch)
        self.Text_HeadingResearch.setGeometry(QtCore.QRect(10, 0, 981, 711))
        self.Text_HeadingResearch.setObjectName("Text_HeadingResearch")
        self.pages.addWidget(self.pageTopics_HeadingResearch)
        self.pageHelp_AboutTool = QtWidgets.QWidget()
        self.pageHelp_AboutTool.setObjectName("pageHelp_AboutTool")
        self.Text_AboutTool = QtWidgets.QTextEdit(parent=self.pageHelp_AboutTool)
        self.Text_AboutTool.setGeometry(QtCore.QRect(10, 0, 981, 711))
        self.Text_AboutTool.setObjectName("Text_AboutTool")
        self.pages.addWidget(self.pageHelp_AboutTool)
        self.pageHelp_AboutAuthorDeveloper = QtWidgets.QWidget()
        self.pageHelp_AboutAuthorDeveloper.setObjectName("pageHelp_AboutAuthorDeveloper")
        self.Text_AboutAuthorDeveloper = QtWidgets.QTextEdit(parent=self.pageHelp_AboutAuthorDeveloper)
        self.Text_AboutAuthorDeveloper.setGeometry(QtCore.QRect(10, 0, 981, 711))
        self.Text_AboutAuthorDeveloper.setObjectName("Text_AboutAuthorDeveloper")
        self.pages.addWidget(self.pageHelp_AboutAuthorDeveloper)
        MainWindow.setCentralWidget(self.container)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1025, 33))
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
        self.menuHelp.addAction(self.action_AboutTool)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.action_AboutAuthorDeveloper)
        self.menubar.addAction(self.menuTopics.menuAction())
        self.menubar.addAction(self.menuLab.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuControls.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.readPages()
        self.connectActions()
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        self.retranslateUi(MainWindow)
        self.pages.setCurrentIndex(6)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

##############################################################################windows-1252####utf-8
    def readPages(self):
        _translate = QtCore.QCoreApplication.translate
        
        Text_BigPicture = ""
        with open('pages/Text_BigPicture.html', 'r' ) as file:  
             Text_BigPicture = file.read()
        self.Text_BigPicture.setHtml(_translate("MainWindow", Text_BigPicture))
        self.Text_BigPicture.setStyleSheet("padding:10px")

        Text_UniversityCurriculum = ""
        with open('pages/Text_UniversityCurriculum.html', 'r') as file:  
             Text_UniversityCurriculum = file.read()
        self.Text_UniversityCurriculum.setHtml(_translate("MainWindow", Text_UniversityCurriculum))
        self.Text_UniversityCurriculum.setStyleSheet("padding:10px")
        
        Text_RoadMap = ""
        with open('pages/Text_RoadMap.html', 'r') as file:  
             Text_RoadMap = file.read()
        self.Text_RoadMap.setHtml(_translate("MainWindow", Text_RoadMap))
        self.Text_RoadMap.setStyleSheet("padding:10px")

        Text_StudyPlan = ""
        with open('pages/Text_StudyPlan.html', 'r') as file:  
             Text_StudyPlan = file.read()
        self.Text_StudyPlan.setHtml(_translate("MainWindow", Text_StudyPlan))
        self.Text_StudyPlan.setStyleSheet("padding:10px")

        Text_HeadingResearch = ""
        with open('pages/Text_HeadingResearch.html', 'r') as file:  #, encoding='utf-8'
             Text_HeadingResearch = file.read()
        self.Text_HeadingResearch.setHtml(_translate("MainWindow", Text_HeadingResearch))
        self.Text_HeadingResearch.setStyleSheet("padding:10px")

        Text_AboutTool = ""
        with open('pages/Text_AboutTool.html', 'r') as file:  
             Text_AboutTool = file.read()
        self.Text_AboutTool.setHtml(_translate("MainWindow", Text_AboutTool))
        self.Text_AboutTool.setStyleSheet("padding:10px")

        Text_AboutAuthorDeveloper = ""
        with open('pages/Text_AboutAuthorDeveloper.html', 'r') as file: 
             Text_AboutAuthorDeveloper = file.read()
        self.Text_AboutAuthorDeveloper.setHtml(_translate("MainWindow", Text_AboutAuthorDeveloper))
        self.Text_AboutAuthorDeveloper.setStyleSheet("padding:10px")
    
    def changePage(self,index):
        self.pages.setCurrentIndex(index)

    def connectActions(self):
        self.action_BigPicture.triggered.connect(partial(self.changePage,0))
        self.action_UniversityCurriculum.triggered.connect(partial(self.changePage,1))
        self.action_RoadMap.triggered.connect(partial(self.changePage,2))
        self.action_StudyPlan.triggered.connect(partial(self.changePage,3))
        self.action_HeadingResearch.triggered.connect(partial(self.changePage,4))
        self.action_AboutTool.triggered.connect(partial(self.changePage,5))
        self.action_AboutAuthorDeveloper.triggered.connect(partial(self.changePage,6))
        self.action_CloseOtherWindows.triggered.connect(self.closeOtherWindows)
        self.action_CloseMainWindow.triggered.connect(self.closeMainWindow)
        self.action_CloseAllWindows.triggered.connect(self.closeAllWindow)

    def closeAllWindow(self):
          self.lower()
          cv2.destroyAllWindows()
          MainWindow.close()
          MainWindow.destroy()
          self.close()
          self.destroy()

    def closeOtherWindows(self):
        self.lower()
        cv2.destroyAllWindows()
       
    def closeMainWindow(self):
        MainWindow.close()
        MainWindow.destroy()
        self.close()
        self.destroy()
#############################################################################

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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
