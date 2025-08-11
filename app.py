#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Start Block 1
# -*- Encoding: utf-8 -*- #
"""
@Author | Developer: Mehrdad Ahady
"""
import os
from os import path, listdir
from os.path import isfile, join
import sys
import time
import cv2
import shutil
import inspect
from functools import partial
import emoji
import numpy as np
import regex
import PyQt6
import PyQt6.QtCore
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMenu, QMainWindow, QApplication, QWidget, QMessageBox, QFileDialog
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtGui import QDesktopServices, QCloseEvent
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineCore import QWebEngineProfile
from utils.CustomPDFView import CustomPdfView
from utils.ImagesAndColorsManipulationsAndOprations import ImagesAndColorsManipulationsAndOprations

class Ui_MainWindow(QMainWindow,object):
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<End Block 1
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
        self.container.setMinimumSize(QtCore.QSize(1024, 734))
        self.container.setMaximumSize(QtCore.QSize(1024, 734))
        self.container.setBaseSize(QtCore.QSize(1024, 734))
        self.container.setObjectName("container")
        self.pages = QtWidgets.QStackedWidget(parent=self.container)
        self.pages.setGeometry(QtCore.QRect(10, 0, 1011, 721))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pages.sizePolicy().hasHeightForWidth())
        self.pages.setSizePolicy(sizePolicy)
        self.pages.setMinimumSize(QtCore.QSize(1011, 721))
        self.pages.setMaximumSize(QtCore.QSize(1011, 721))
        self.pages.setBaseSize(QtCore.QSize(1011, 721))
        self.pages.setObjectName("pages")
        self.page_ImagesAndColorsManipulationsAndOprations = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_ImagesAndColorsManipulationsAndOprations.sizePolicy().hasHeightForWidth())
        self.page_ImagesAndColorsManipulationsAndOprations.setSizePolicy(sizePolicy)
        self.page_ImagesAndColorsManipulationsAndOprations.setObjectName("page_ImagesAndColorsManipulationsAndOprations")
        self.groupBox_FlipImage = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_FlipImage.setGeometry(QtCore.QRect(10, 290, 481, 71))
        self.groupBox_FlipImage.setObjectName("groupBox_FlipImage")
        self.gridLayoutWidget_6 = QtWidgets.QWidget(parent=self.groupBox_FlipImage)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(30, 10, 441, 61))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.gridLayout_FlipImage = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_FlipImage.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_FlipImage.setObjectName("gridLayout_FlipImage")
        self.checkBox_FlipVertical = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_6)
        self.checkBox_FlipVertical.setObjectName("checkBox_FlipVertical")
        self.gridLayout_FlipImage.addWidget(self.checkBox_FlipVertical, 0, 1, 1, 1)
        self.checkBox_FlipHorizantal = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_6)
        self.checkBox_FlipHorizantal.setObjectName("checkBox_FlipHorizantal")
        self.gridLayout_FlipImage.addWidget(self.checkBox_FlipHorizantal, 0, 0, 1, 1)
        self.checkBox_SwapTranspose = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_6)
        self.checkBox_SwapTranspose.setObjectName("checkBox_SwapTranspose")
        self.gridLayout_FlipImage.addWidget(self.checkBox_SwapTranspose, 0, 2, 1, 1)
        self.groupBox_BGRColorSpace = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_BGRColorSpace.setGeometry(QtCore.QRect(500, 70, 241, 51))
        self.groupBox_BGRColorSpace.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.groupBox_BGRColorSpace.setObjectName("groupBox_BGRColorSpace")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(parent=self.groupBox_BGRColorSpace)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(60, 10, 181, 41))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_BGRChannel = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_BGRChannel.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_BGRChannel.setObjectName("gridLayout_BGRChannel")
        self.checkBox_GreenChannel = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_2)
        self.checkBox_GreenChannel.setObjectName("checkBox_GreenChannel")
        self.gridLayout_BGRChannel.addWidget(self.checkBox_GreenChannel, 0, 2, 1, 1)
        self.checkBox_RedChannel = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_2)
        self.checkBox_RedChannel.setObjectName("checkBox_RedChannel")
        self.gridLayout_BGRChannel.addWidget(self.checkBox_RedChannel, 0, 3, 1, 1)
        self.checkBox_BlueChannel = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_2)
        self.checkBox_BlueChannel.setObjectName("checkBox_BlueChannel")
        self.gridLayout_BGRChannel.addWidget(self.checkBox_BlueChannel, 0, 0, 1, 1)
        self.groupBox_HSVColorSpace = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_HSVColorSpace.setGeometry(QtCore.QRect(750, 70, 241, 51))
        self.groupBox_HSVColorSpace.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.groupBox_HSVColorSpace.setObjectName("groupBox_HSVColorSpace")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(parent=self.groupBox_HSVColorSpace)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(30, 10, 211, 41))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_HSVChannel = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_HSVChannel.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_HSVChannel.setObjectName("gridLayout_HSVChannel")
        self.checkBox_HSVHueChannel = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_3)
        self.checkBox_HSVHueChannel.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.checkBox_HSVHueChannel.setObjectName("checkBox_HSVHueChannel")
        self.gridLayout_HSVChannel.addWidget(self.checkBox_HSVHueChannel, 0, 0, 1, 1)
        self.checkBox_HSVSaturation = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_3)
        self.checkBox_HSVSaturation.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.checkBox_HSVSaturation.setObjectName("checkBox_HSVSaturation")
        self.gridLayout_HSVChannel.addWidget(self.checkBox_HSVSaturation, 0, 1, 1, 1)
        self.checkBox_HSVValue = QtWidgets.QCheckBox(parent=self.gridLayoutWidget_3)
        self.checkBox_HSVValue.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.checkBox_HSVValue.setObjectName("checkBox_HSVValue")
        self.gridLayout_HSVChannel.addWidget(self.checkBox_HSVValue, 0, 2, 1, 1)
        self.groupBox_ResizeScaleImageByDimention = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_ResizeScaleImageByDimention.setGeometry(QtCore.QRect(10, 120, 481, 61))
        self.groupBox_ResizeScaleImageByDimention.setObjectName("groupBox_ResizeScaleImageByDimention")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(parent=self.groupBox_ResizeScaleImageByDimention)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(80, 20, 391, 31))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_ResizeImage = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_ResizeImage.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_ResizeImage.setObjectName("gridLayout_ResizeImage")
        self.horizontalSlider_ResizeWidth = QtWidgets.QSlider(parent=self.gridLayoutWidget_4)
        self.horizontalSlider_ResizeWidth.setMinimum(50)
        self.horizontalSlider_ResizeWidth.setMaximum(2000)
        self.horizontalSlider_ResizeWidth.setSingleStep(10)
        self.horizontalSlider_ResizeWidth.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_ResizeWidth.setObjectName("horizontalSlider_ResizeWidth")
        self.gridLayout_ResizeImage.addWidget(self.horizontalSlider_ResizeWidth, 1, 1, 1, 1)
        self.horizontalSlider_ResizeHeight = QtWidgets.QSlider(parent=self.gridLayoutWidget_4)
        self.horizontalSlider_ResizeHeight.setMinimum(50)
        self.horizontalSlider_ResizeHeight.setMaximum(2000)
        self.horizontalSlider_ResizeHeight.setSingleStep(10)
        self.horizontalSlider_ResizeHeight.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_ResizeHeight.setObjectName("horizontalSlider_ResizeHeight")
        self.gridLayout_ResizeImage.addWidget(self.horizontalSlider_ResizeHeight, 1, 0, 1, 1)
        self.label_ResizeHeight = QtWidgets.QLabel(parent=self.gridLayoutWidget_4)
        self.label_ResizeHeight.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_ResizeHeight.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_ResizeHeight.setObjectName("label_ResizeHeight")
        self.gridLayout_ResizeImage.addWidget(self.label_ResizeHeight, 2, 0, 1, 1)
        self.label_ResizeWidth = QtWidgets.QLabel(parent=self.gridLayoutWidget_4)
        self.label_ResizeWidth.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_ResizeWidth.setObjectName("label_ResizeWidth")
        self.gridLayout_ResizeImage.addWidget(self.label_ResizeWidth, 2, 1, 1, 1)
        self.pushButton_LargerPyrUp = QtWidgets.QPushButton(parent=self.groupBox_ResizeScaleImageByDimention)
        self.pushButton_LargerPyrUp.setGeometry(QtCore.QRect(10, 20, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.pushButton_LargerPyrUp.setFont(font)
        self.pushButton_LargerPyrUp.setObjectName("pushButton_LargerPyrUp")
        self.pushButton_SmallerPyrDown = QtWidgets.QPushButton(parent=self.groupBox_ResizeScaleImageByDimention)
        self.pushButton_SmallerPyrDown.setGeometry(QtCore.QRect(40, 20, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_SmallerPyrDown.setFont(font)
        self.pushButton_SmallerPyrDown.setObjectName("pushButton_SmallerPyrDown")
        self.groupBox_RotationScale = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_RotationScale.setGeometry(QtCore.QRect(500, 180, 491, 111))
        self.groupBox_RotationScale.setObjectName("groupBox_RotationScale")
        self.gridLayoutWidget_5 = QtWidgets.QWidget(parent=self.groupBox_RotationScale)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(40, 10, 451, 91))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_RotationScale = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_RotationScale.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_RotationScale.setObjectName("gridLayout_RotationScale")
        self.dial_RotationDegree = QtWidgets.QDial(parent=self.gridLayoutWidget_5)
        self.dial_RotationDegree.setMinimum(0)
        self.dial_RotationDegree.setMaximum(360)
        self.dial_RotationDegree.setSingleStep(10)
        self.dial_RotationDegree.setObjectName("dial_RotationDegree")
        self.gridLayout_RotationScale.addWidget(self.dial_RotationDegree, 1, 0, 1, 1)
        self.dial_RotationScale = QtWidgets.QDial(parent=self.gridLayoutWidget_5)
        self.dial_RotationScale.setMinimum(0)
        self.dial_RotationScale.setMaximum(10)
        self.dial_RotationScale.setProperty("value", 0)
        self.dial_RotationScale.setObjectName("dial_RotationScale")
        self.gridLayout_RotationScale.addWidget(self.dial_RotationScale, 1, 1, 1, 1)
        self.gridLayout_RotationDegree = QtWidgets.QGridLayout()
        self.gridLayout_RotationDegree.setObjectName("gridLayout_RotationDegree")
        self.label_RotationDegree = QtWidgets.QLabel(parent=self.gridLayoutWidget_5)
        self.label_RotationDegree.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_RotationDegree.setObjectName("label_RotationDegree")
        self.gridLayout_RotationDegree.addWidget(self.label_RotationDegree, 0, 0, 1, 1)
        self.label_RotationDegreeValue = QtWidgets.QLabel(parent=self.gridLayoutWidget_5)
        self.label_RotationDegreeValue.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_RotationDegreeValue.setObjectName("label_RotationDegreeValue")
        self.gridLayout_RotationDegree.addWidget(self.label_RotationDegreeValue, 0, 1, 1, 1)
        self.gridLayout_RotationScale.addLayout(self.gridLayout_RotationDegree, 2, 0, 1, 1)
        self.gridLayout_RorationScale = QtWidgets.QGridLayout()
        self.gridLayout_RorationScale.setObjectName("gridLayout_RorationScale")
        self.label_RorationScale = QtWidgets.QLabel(parent=self.gridLayoutWidget_5)
        self.label_RorationScale.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_RorationScale.setObjectName("label_RorationScale")
        self.gridLayout_RorationScale.addWidget(self.label_RorationScale, 0, 0, 1, 1)
        self.label_RorationScaleValue = QtWidgets.QLabel(parent=self.gridLayoutWidget_5)
        self.label_RorationScaleValue.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_RorationScaleValue.setObjectName("label_RorationScaleValue")
        self.gridLayout_RorationScale.addWidget(self.label_RorationScaleValue, 0, 1, 1, 1)
        self.gridLayout_RotationScale.addLayout(self.gridLayout_RorationScale, 2, 1, 1, 1)
        self.groupBox_DrawingShape = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_DrawingShape.setGeometry(QtCore.QRect(500, 360, 491, 61))
        self.groupBox_DrawingShape.setObjectName("groupBox_DrawingShape")
        self.comboBox_DrawShape = QtWidgets.QComboBox(parent=self.groupBox_DrawingShape)
        self.comboBox_DrawShape.setGeometry(QtCore.QRect(80, 20, 391, 31))
        self.comboBox_DrawShape.setObjectName("comboBox_DrawShape")
        self.comboBox_DrawShape.addItem("")
        self.comboBox_DrawShape.setItemText(0, "")
        self.comboBox_DrawShape.addItem("")
        self.comboBox_DrawShape.addItem("")
        self.comboBox_DrawShape.addItem("")
        self.comboBox_DrawShape.addItem("")
        self.comboBox_DrawShape.addItem("")
        self.groupBox_Translation = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_Translation.setGeometry(QtCore.QRect(10, 180, 481, 111))
        self.groupBox_Translation.setObjectName("groupBox_Translation")
        self.gridLayoutWidget_7 = QtWidgets.QWidget(parent=self.groupBox_Translation)
        self.gridLayoutWidget_7.setGeometry(QtCore.QRect(0, 20, 481, 81))
        self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_7")
        self.gridLayout_Translation = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_Translation.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Translation.setObjectName("gridLayout_Translation")
        self.dial_Y1 = QtWidgets.QDial(parent=self.gridLayoutWidget_7)
        self.dial_Y1.setMaximum(255)
        self.dial_Y1.setSingleStep(5)
        self.dial_Y1.setProperty("value", 200)
        self.dial_Y1.setObjectName("dial_Y1")
        self.gridLayout_Translation.addWidget(self.dial_Y1, 0, 2, 1, 1)
        self.dial_Y2 = QtWidgets.QDial(parent=self.gridLayoutWidget_7)
        self.dial_Y2.setMaximum(255)
        self.dial_Y2.setSingleStep(5)
        self.dial_Y2.setProperty("value", 50)
        self.dial_Y2.setObjectName("dial_Y2")
        self.gridLayout_Translation.addWidget(self.dial_Y2, 0, 3, 1, 1)
        self.dial_X1 = QtWidgets.QDial(parent=self.gridLayoutWidget_7)
        self.dial_X1.setMaximum(255)
        self.dial_X1.setSingleStep(5)
        self.dial_X1.setProperty("value", 10)
        self.dial_X1.setObjectName("dial_X1")
        self.gridLayout_Translation.addWidget(self.dial_X1, 0, 0, 1, 1)
        self.dial_Z1 = QtWidgets.QDial(parent=self.gridLayoutWidget_7)
        self.dial_Z1.setMaximum(255)
        self.dial_Z1.setSingleStep(5)
        self.dial_Z1.setProperty("value", 100)
        self.dial_Z1.setObjectName("dial_Z1")
        self.gridLayout_Translation.addWidget(self.dial_Z1, 0, 4, 1, 1)
        self.dial_Z2 = QtWidgets.QDial(parent=self.gridLayoutWidget_7)
        self.dial_Z2.setMaximum(255)
        self.dial_Z2.setSingleStep(5)
        self.dial_Z2.setProperty("value", 250)
        self.dial_Z2.setObjectName("dial_Z2")
        self.gridLayout_Translation.addWidget(self.dial_Z2, 0, 5, 1, 1)
        self.dial_X2 = QtWidgets.QDial(parent=self.gridLayoutWidget_7)
        self.dial_X2.setMaximum(255)
        self.dial_X2.setSingleStep(5)
        self.dial_X2.setProperty("value", 100)
        self.dial_X2.setObjectName("dial_X2")
        self.gridLayout_Translation.addWidget(self.dial_X2, 0, 1, 1, 1)
        self.gridLayout_X1 = QtWidgets.QGridLayout()
        self.gridLayout_X1.setObjectName("gridLayout_X1")
        self.label_X1 = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_X1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_X1.setObjectName("label_X1")
        self.gridLayout_X1.addWidget(self.label_X1, 0, 0, 1, 1)
        self.label_X1_Value = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_X1_Value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_X1_Value.setObjectName("label_X1_Value")
        self.gridLayout_X1.addWidget(self.label_X1_Value, 0, 1, 1, 1)
        self.gridLayout_Translation.addLayout(self.gridLayout_X1, 1, 0, 1, 1)
        self.gridLayout_X2 = QtWidgets.QGridLayout()
        self.gridLayout_X2.setObjectName("gridLayout_X2")
        self.label_X2 = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_X2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_X2.setObjectName("label_X2")
        self.gridLayout_X2.addWidget(self.label_X2, 0, 0, 1, 1)
        self.label_X2_Value = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_X2_Value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_X2_Value.setObjectName("label_X2_Value")
        self.gridLayout_X2.addWidget(self.label_X2_Value, 0, 1, 1, 1)
        self.gridLayout_Translation.addLayout(self.gridLayout_X2, 1, 1, 1, 1)
        self.gridLayout_Y1 = QtWidgets.QGridLayout()
        self.gridLayout_Y1.setObjectName("gridLayout_Y1")
        self.label_Y1 = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_Y1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Y1.setObjectName("label_Y1")
        self.gridLayout_Y1.addWidget(self.label_Y1, 0, 0, 1, 1)
        self.label_Y1_Value = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_Y1_Value.setObjectName("label_Y1_Value")
        self.gridLayout_Y1.addWidget(self.label_Y1_Value, 0, 1, 1, 1)
        self.gridLayout_Translation.addLayout(self.gridLayout_Y1, 1, 2, 1, 1)
        self.gridLayout_Y2 = QtWidgets.QGridLayout()
        self.gridLayout_Y2.setObjectName("gridLayout_Y2")
        self.label_Y2 = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_Y2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Y2.setObjectName("label_Y2")
        self.gridLayout_Y2.addWidget(self.label_Y2, 0, 0, 1, 1)
        self.label_Y2_Value = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_Y2_Value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Y2_Value.setObjectName("label_Y2_Value")
        self.gridLayout_Y2.addWidget(self.label_Y2_Value, 0, 1, 1, 1)
        self.gridLayout_Translation.addLayout(self.gridLayout_Y2, 1, 3, 1, 1)
        self.gridLayout_Z1 = QtWidgets.QGridLayout()
        self.gridLayout_Z1.setObjectName("gridLayout_Z1")
        self.label_Z1 = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_Z1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Z1.setObjectName("label_Z1")
        self.gridLayout_Z1.addWidget(self.label_Z1, 0, 0, 1, 1)
        self.label_Z1_Value = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_Z1_Value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Z1_Value.setObjectName("label_Z1_Value")
        self.gridLayout_Z1.addWidget(self.label_Z1_Value, 0, 1, 1, 1)
        self.gridLayout_Translation.addLayout(self.gridLayout_Z1, 1, 4, 1, 1)
        self.gridLayout_Z2 = QtWidgets.QGridLayout()
        self.gridLayout_Z2.setObjectName("gridLayout_Z2")
        self.label_Z2 = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_Z2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Z2.setObjectName("label_Z2")
        self.gridLayout_Z2.addWidget(self.label_Z2, 0, 0, 1, 1)
        self.label_Z2_Value = QtWidgets.QLabel(parent=self.gridLayoutWidget_7)
        self.label_Z2_Value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Z2_Value.setObjectName("label_Z2_Value")
        self.gridLayout_Z2.addWidget(self.label_Z2_Value, 0, 1, 1, 1)
        self.gridLayout_Translation.addLayout(self.gridLayout_Z2, 1, 5, 1, 1)
        self.groupBox_AddText = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_AddText.setGeometry(QtCore.QRect(10, 360, 481, 61))
        self.groupBox_AddText.setObjectName("groupBox_AddText")
        self.textEdit_AddText = QtWidgets.QTextEdit(parent=self.groupBox_AddText)
        self.textEdit_AddText.setGeometry(QtCore.QRect(10, 20, 391, 31))
        self.textEdit_AddText.setObjectName("textEdit_AddText")
        self.pushButton_AddText = QtWidgets.QPushButton(parent=self.groupBox_AddText)
        self.pushButton_AddText.setGeometry(QtCore.QRect(410, 20, 61, 31))
        self.pushButton_AddText.setObjectName("pushButton_AddText")
        self.groupBox_Skew = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_Skew.setGeometry(QtCore.QRect(500, 120, 491, 61))
        self.groupBox_Skew.setObjectName("groupBox_Skew")
        self.gridLayoutWidget_8 = QtWidgets.QWidget(parent=self.groupBox_Skew)
        self.gridLayoutWidget_8.setGeometry(QtCore.QRect(40, 20, 441, 31))
        self.gridLayoutWidget_8.setObjectName("gridLayoutWidget_8")
        self.gridLayout_Skew = QtWidgets.QGridLayout(self.gridLayoutWidget_8)
        self.gridLayout_Skew.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Skew.setObjectName("gridLayout_Skew")
        self.horizontalSlider_SkewWidth = QtWidgets.QSlider(parent=self.gridLayoutWidget_8)
        self.horizontalSlider_SkewWidth.setMinimum(50)
        self.horizontalSlider_SkewWidth.setMaximum(2000)
        self.horizontalSlider_SkewWidth.setSingleStep(50)
        self.horizontalSlider_SkewWidth.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_SkewWidth.setObjectName("horizontalSlider_SkewWidth")
        self.gridLayout_Skew.addWidget(self.horizontalSlider_SkewWidth, 1, 1, 1, 1)
        self.horizontalSlider_SkewHeight = QtWidgets.QSlider(parent=self.gridLayoutWidget_8)
        self.horizontalSlider_SkewHeight.setMinimum(50)
        self.horizontalSlider_SkewHeight.setMaximum(2000)
        self.horizontalSlider_SkewHeight.setSingleStep(50)
        self.horizontalSlider_SkewHeight.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_SkewHeight.setObjectName("horizontalSlider_SkewHeight")
        self.gridLayout_Skew.addWidget(self.horizontalSlider_SkewHeight, 1, 0, 1, 1)
        self.label_SkewHeight = QtWidgets.QLabel(parent=self.gridLayoutWidget_8)
        self.label_SkewHeight.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_SkewHeight.setObjectName("label_SkewHeight")
        self.gridLayout_Skew.addWidget(self.label_SkewHeight, 2, 0, 1, 1)
        self.label_SkewWidth = QtWidgets.QLabel(parent=self.gridLayoutWidget_8)
        self.label_SkewWidth.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_SkewWidth.setObjectName("label_SkewWidth")
        self.gridLayout_Skew.addWidget(self.label_SkewWidth, 2, 1, 1, 1)
        self.groupBox_Crop = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_Crop.setGeometry(QtCore.QRect(500, 290, 491, 71))
        self.groupBox_Crop.setObjectName("groupBox_Crop")
        self.gridLayoutWidget_9 = QtWidgets.QWidget(parent=self.groupBox_Crop)
        self.gridLayoutWidget_9.setGeometry(QtCore.QRect(39, 20, 441, 44))
        self.gridLayoutWidget_9.setObjectName("gridLayoutWidget_9")
        self.gridLayout_Crop = QtWidgets.QGridLayout(self.gridLayoutWidget_9)
        self.gridLayout_Crop.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Crop.setObjectName("gridLayout_Crop")
        self.horizontalSlider_CropTopLefCoefficient = QtWidgets.QSlider(parent=self.gridLayoutWidget_9)
        self.horizontalSlider_CropTopLefCoefficient.setMinimum(1)
        self.horizontalSlider_CropTopLefCoefficient.setMaximum(100)
        self.horizontalSlider_CropTopLefCoefficient.setSingleStep(5)
        self.horizontalSlider_CropTopLefCoefficient.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_CropTopLefCoefficient.setObjectName("horizontalSlider_CropTopLefCoefficient")
        self.gridLayout_Crop.addWidget(self.horizontalSlider_CropTopLefCoefficient, 0, 0, 1, 1)
        self.horizontalSlider_CropBottomRightCoefficient = QtWidgets.QSlider(parent=self.gridLayoutWidget_9)
        self.horizontalSlider_CropBottomRightCoefficient.setMinimum(1)
        self.horizontalSlider_CropBottomRightCoefficient.setMaximum(100)
        self.horizontalSlider_CropBottomRightCoefficient.setSingleStep(5)
        self.horizontalSlider_CropBottomRightCoefficient.setProperty("value", 100)
        self.horizontalSlider_CropBottomRightCoefficient.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_CropBottomRightCoefficient.setObjectName("horizontalSlider_CropBottomRightCoefficient")
        self.gridLayout_Crop.addWidget(self.horizontalSlider_CropBottomRightCoefficient, 0, 1, 1, 1)
        self.gridLayout__CropTopLefCoefficient = QtWidgets.QGridLayout()
        self.gridLayout__CropTopLefCoefficient.setObjectName("gridLayout__CropTopLefCoefficient")
        self.label_CropTopLefCoefficient = QtWidgets.QLabel(parent=self.gridLayoutWidget_9)
        self.label_CropTopLefCoefficient.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_CropTopLefCoefficient.setObjectName("label_CropTopLefCoefficient")
        self.gridLayout__CropTopLefCoefficient.addWidget(self.label_CropTopLefCoefficient, 0, 0, 1, 1)
        self.label_CropTopLefCoefficientValue = QtWidgets.QLabel(parent=self.gridLayoutWidget_9)
        self.label_CropTopLefCoefficientValue.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_CropTopLefCoefficientValue.setObjectName("label_CropTopLefCoefficientValue")
        self.gridLayout__CropTopLefCoefficient.addWidget(self.label_CropTopLefCoefficientValue, 0, 1, 1, 1)
        self.gridLayout_Crop.addLayout(self.gridLayout__CropTopLefCoefficient, 1, 0, 1, 1)
        self.gridLayout_CropBottomRightCoefficient = QtWidgets.QGridLayout()
        self.gridLayout_CropBottomRightCoefficient.setObjectName("gridLayout_CropBottomRightCoefficient")
        self.label_CropBottomRightCoefficient = QtWidgets.QLabel(parent=self.gridLayoutWidget_9)
        self.label_CropBottomRightCoefficient.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_CropBottomRightCoefficient.setObjectName("label_CropBottomRightCoefficient")
        self.gridLayout_CropBottomRightCoefficient.addWidget(self.label_CropBottomRightCoefficient, 0, 0, 1, 1)
        self.label_CropBottomRightCoefficientValue = QtWidgets.QLabel(parent=self.gridLayoutWidget_9)
        self.label_CropBottomRightCoefficientValue.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_CropBottomRightCoefficientValue.setObjectName("label_CropBottomRightCoefficientValue")
        self.gridLayout_CropBottomRightCoefficient.addWidget(self.label_CropBottomRightCoefficientValue, 0, 1, 1, 1)
        self.gridLayout_Crop.addLayout(self.gridLayout_CropBottomRightCoefficient, 1, 1, 1, 1)
        self.groupBox_ColorSpaceConversion = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_ColorSpaceConversion.setGeometry(QtCore.QRect(10, 70, 481, 51))
        self.groupBox_ColorSpaceConversion.setObjectName("groupBox_ColorSpaceConversion")
        self.comboBox_ColorSpaceConversion = QtWidgets.QComboBox(parent=self.groupBox_ColorSpaceConversion)
        self.comboBox_ColorSpaceConversion.setGeometry(QtCore.QRect(150, 14, 321, 31))
        self.comboBox_ColorSpaceConversion.setObjectName("comboBox_ColorSpaceConversion")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.comboBox_ColorSpaceConversion.setItemText(0, "")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.comboBox_ColorSpaceConversion.addItem("")
        self.groupBox_ImageInfo = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_ImageInfo.setGeometry(QtCore.QRect(10, 30, 481, 41))
        self.groupBox_ImageInfo.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.groupBox_ImageInfo.setObjectName("groupBox_ImageInfo")
        self.gridLayoutWidget_21 = QtWidgets.QWidget(parent=self.groupBox_ImageInfo)
        self.gridLayoutWidget_21.setGeometry(QtCore.QRect(120, 10, 351, 31))
        self.gridLayoutWidget_21.setObjectName("gridLayoutWidget_21")
        self.gridLayout_ImageInfo = QtWidgets.QGridLayout(self.gridLayoutWidget_21)
        self.gridLayout_ImageInfo.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_ImageInfo.setObjectName("gridLayout_ImageInfo")
        self.label_ImageDepthValue = QtWidgets.QLabel(parent=self.gridLayoutWidget_21)
        self.label_ImageDepthValue.setText("")
        self.label_ImageDepthValue.setObjectName("label_ImageDepthValue")
        self.gridLayout_ImageInfo.addWidget(self.label_ImageDepthValue, 0, 7, 1, 1)
        self.label_ImageWidth = QtWidgets.QLabel(parent=self.gridLayoutWidget_21)
        self.label_ImageWidth.setObjectName("label_ImageWidth")
        self.gridLayout_ImageInfo.addWidget(self.label_ImageWidth, 0, 4, 1, 1)
        self.label_ImageHeightValue = QtWidgets.QLabel(parent=self.gridLayoutWidget_21)
        self.label_ImageHeightValue.setText("")
        self.label_ImageHeightValue.setObjectName("label_ImageHeightValue")
        self.gridLayout_ImageInfo.addWidget(self.label_ImageHeightValue, 0, 3, 1, 1)
        self.label_ImageShapeValue = QtWidgets.QLabel(parent=self.gridLayoutWidget_21)
        self.label_ImageShapeValue.setText("")
        self.label_ImageShapeValue.setObjectName("label_ImageShapeValue")
        self.gridLayout_ImageInfo.addWidget(self.label_ImageShapeValue, 0, 1, 1, 1)
        self.label_ImageWidthValue = QtWidgets.QLabel(parent=self.gridLayoutWidget_21)
        self.label_ImageWidthValue.setText("")
        self.label_ImageWidthValue.setObjectName("label_ImageWidthValue")
        self.gridLayout_ImageInfo.addWidget(self.label_ImageWidthValue, 0, 5, 1, 1)
        self.label_ImageHeight = QtWidgets.QLabel(parent=self.gridLayoutWidget_21)
        self.label_ImageHeight.setObjectName("label_ImageHeight")
        self.gridLayout_ImageInfo.addWidget(self.label_ImageHeight, 0, 2, 1, 1)
        self.label_ImageDepth = QtWidgets.QLabel(parent=self.gridLayoutWidget_21)
        self.label_ImageDepth.setObjectName("label_ImageDepth")
        self.gridLayout_ImageInfo.addWidget(self.label_ImageDepth, 0, 6, 1, 1)
        self.label_ImageShape = QtWidgets.QLabel(parent=self.gridLayoutWidget_21)
        self.label_ImageShape.setObjectName("label_ImageShape")
        self.gridLayout_ImageInfo.addWidget(self.label_ImageShape, 0, 0, 1, 1)
        self.pushButton_UploadVideos = QtWidgets.QPushButton(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.pushButton_UploadVideos.setGeometry(QtCore.QRect(500, 0, 121, 31))
        self.pushButton_UploadVideos.setObjectName("pushButton_UploadVideos")
        self.label_SelectImage = QtWidgets.QLabel(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.label_SelectImage.setGeometry(QtCore.QRect(170, 0, 71, 31))
        self.label_SelectImage.setObjectName("label_SelectImage")
        self.comboBox_SelectVideo = QtWidgets.QComboBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.comboBox_SelectVideo.setGeometry(QtCore.QRect(750, 0, 241, 31))
        self.comboBox_SelectVideo.setObjectName("comboBox_SelectVideo")
        self.comboBox_SelectVideo.addItem("")
        self.comboBox_SelectVideo.setItemText(0, "")
        self.groupBox_VideoInfo = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_VideoInfo.setGeometry(QtCore.QRect(500, 30, 491, 41))
        self.groupBox_VideoInfo.setObjectName("groupBox_VideoInfo")
        self.label_SelectVideo = QtWidgets.QLabel(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.label_SelectVideo.setGeometry(QtCore.QRect(670, 5, 71, 21))
        self.label_SelectVideo.setObjectName("label_SelectVideo")
        self.pushButton_UploadImages = QtWidgets.QPushButton(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.pushButton_UploadImages.setGeometry(QtCore.QRect(9, 0, 121, 31))
        self.pushButton_UploadImages.setObjectName("pushButton_UploadImages")
        self.comboBox_SelectImage = QtWidgets.QComboBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.comboBox_SelectImage.setGeometry(QtCore.QRect(250, 0, 241, 31))
        self.comboBox_SelectImage.setObjectName("comboBox_SelectImage")
        self.comboBox_SelectImage.addItem("")
        self.comboBox_SelectImage.setItemText(0, "")
        self.pushButton_SaveImage = QtWidgets.QPushButton(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.pushButton_SaveImage.setGeometry(QtCore.QRect(10, 680, 100, 40))
        self.pushButton_SaveImage.setObjectName("pushButton_SaveImage")
        self.pushButton_SaveCode = QtWidgets.QPushButton(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.pushButton_SaveCode.setGeometry(QtCore.QRect(890, 680, 100, 40))
        self.pushButton_SaveCode.setObjectName("pushButton_SaveCode")
        self.textBrowser_ImageAndColors = QtWidgets.QTextBrowser(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.textBrowser_ImageAndColors.setGeometry(QtCore.QRect(10, 550, 981, 131))
        self.textBrowser_ImageAndColors.setObjectName("textBrowser_ImageAndColors")
        self.groupBox_DilationErosionEdgeDetection = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_DilationErosionEdgeDetection.setGeometry(QtCore.QRect(670, 420, 321, 61))
        self.groupBox_DilationErosionEdgeDetection.setObjectName("groupBox_DilationErosionEdgeDetection")
        self.comboBox_DilationErosionEdgeDetection = QtWidgets.QComboBox(parent=self.groupBox_DilationErosionEdgeDetection)
        self.comboBox_DilationErosionEdgeDetection.setGeometry(QtCore.QRect(10, 20, 301, 31))
        self.comboBox_DilationErosionEdgeDetection.setObjectName("comboBox_DilationErosionEdgeDetection")
        self.comboBox_DilationErosionEdgeDetection.addItem("")
        self.comboBox_DilationErosionEdgeDetection.setItemText(0, "")
        self.comboBox_DilationErosionEdgeDetection.addItem("")
        self.comboBox_DilationErosionEdgeDetection.addItem("")
        self.comboBox_DilationErosionEdgeDetection.addItem("")
        self.groupBox_ObjectDetection = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_ObjectDetection.setGeometry(QtCore.QRect(340, 480, 321, 61))
        self.groupBox_ObjectDetection.setObjectName("groupBox_ObjectDetection")
        self.comboBox_ObjectDetection = QtWidgets.QComboBox(parent=self.groupBox_ObjectDetection)
        self.comboBox_ObjectDetection.setGeometry(QtCore.QRect(10, 20, 301, 31))
        self.comboBox_ObjectDetection.setObjectName("comboBox_ObjectDetection")
        self.comboBox_ObjectDetection.addItem("")
        self.comboBox_ObjectDetection.setItemText(0, "")
        self.comboBox_ObjectDetection.addItem("")
        self.comboBox_ObjectDetection.addItem("")
        self.comboBox_ObjectDetection.addItem("")
        self.comboBox_ObjectDetection.addItem("")
        self.comboBox_ObjectDetection.addItem("")
        self.comboBox_ObjectDetection.addItem("")
        self.comboBox_ObjectDetection.addItem("")
        self.comboBox_ObjectDetection.addItem("")
        self.groupBox_Filters = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_Filters.setGeometry(QtCore.QRect(340, 420, 321, 61))
        self.groupBox_Filters.setObjectName("groupBox_Filters")
        self.comboBox_Filters = QtWidgets.QComboBox(parent=self.groupBox_Filters)
        self.comboBox_Filters.setGeometry(QtCore.QRect(10, 20, 301, 31))
        self.comboBox_Filters.setObjectName("comboBox_Filters")
        self.comboBox_Filters.addItem("")
        self.comboBox_Filters.setItemText(0, "")
        self.comboBox_Filters.addItem("")
        self.comboBox_Filters.addItem("")
        self.comboBox_Filters.addItem("")
        self.comboBox_Filters.addItem("")
        self.comboBox_Filters.addItem("")
        self.groupBox_ArithmeticAndBitwiseOperations = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_ArithmeticAndBitwiseOperations.setGeometry(QtCore.QRect(10, 420, 321, 61))
        self.groupBox_ArithmeticAndBitwiseOperations.setObjectName("groupBox_ArithmeticAndBitwiseOperations")
        self.comboBox_ArithmeticAndBitwiseOperations = QtWidgets.QComboBox(parent=self.groupBox_ArithmeticAndBitwiseOperations)
        self.comboBox_ArithmeticAndBitwiseOperations.setGeometry(QtCore.QRect(10, 20, 301, 31))
        self.comboBox_ArithmeticAndBitwiseOperations.setObjectName("comboBox_ArithmeticAndBitwiseOperations")
        self.comboBox_ArithmeticAndBitwiseOperations.addItem("")
        self.comboBox_ArithmeticAndBitwiseOperations.setItemText(0, "")
        self.comboBox_ArithmeticAndBitwiseOperations.addItem("")
        self.comboBox_ArithmeticAndBitwiseOperations.addItem("")
        self.groupBox_OCR = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_OCR.setGeometry(QtCore.QRect(670, 480, 321, 61))
        self.groupBox_OCR.setObjectName("groupBox_OCR")
        self.comboBox_OCR = QtWidgets.QComboBox(parent=self.groupBox_OCR)
        self.comboBox_OCR.setGeometry(QtCore.QRect(10, 20, 301, 31))
        self.comboBox_OCR.setObjectName("comboBox_OCR")
        self.comboBox_OCR.addItem("")
        self.comboBox_OCR.setItemText(0, "")
        self.comboBox_OCR.addItem("")
        self.groupBox_SegmentationAndContours = QtWidgets.QGroupBox(parent=self.page_ImagesAndColorsManipulationsAndOprations)
        self.groupBox_SegmentationAndContours.setGeometry(QtCore.QRect(10, 480, 321, 61))
        self.groupBox_SegmentationAndContours.setObjectName("groupBox_SegmentationAndContours")
        self.comboBox_SegmentationAndContours = QtWidgets.QComboBox(parent=self.groupBox_SegmentationAndContours)
        self.comboBox_SegmentationAndContours.setGeometry(QtCore.QRect(10, 20, 301, 31))
        self.comboBox_SegmentationAndContours.setObjectName("comboBox_SegmentationAndContours")
        self.comboBox_SegmentationAndContours.addItem("")
        self.comboBox_SegmentationAndContours.setItemText(0, "")
        self.comboBox_SegmentationAndContours.addItem("")
        self.comboBox_SegmentationAndContours.addItem("")
        self.comboBox_SegmentationAndContours.addItem("")
        self.comboBox_SegmentationAndContours.addItem("")
        self.comboBox_SegmentationAndContours.addItem("")
        self.comboBox_SegmentationAndContours.addItem("")
        self.pages.addWidget(self.page_ImagesAndColorsManipulationsAndOprations)
        self.page_AboutAuthorDeveloper = QtWidgets.QWidget()
        self.page_AboutAuthorDeveloper.setObjectName("page_AboutAuthorDeveloper")
        self.textBrowser_AboutAuthorDeveloper = QtWidgets.QTextBrowser(parent=self.page_AboutAuthorDeveloper)
        self.textBrowser_AboutAuthorDeveloper.setGeometry(QtCore.QRect(5, 0, 991, 711))
        self.textBrowser_AboutAuthorDeveloper.setObjectName("textBrowser_AboutAuthorDeveloper")
        self.pages.addWidget(self.page_AboutAuthorDeveloper)
        self.page_AboutTool = QtWidgets.QWidget()
        self.page_AboutTool.setObjectName("page_AboutTool")
        self.textBrowser_AboutTool = QtWidgets.QTextBrowser(parent=self.page_AboutTool)
        self.textBrowser_AboutTool.setGeometry(QtCore.QRect(5, 0, 991, 711))
        self.textBrowser_AboutTool.setObjectName("textBrowser_AboutTool")
        self.pages.addWidget(self.page_AboutTool)
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
        #
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
        #
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(".\\icons/n8.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_Ethics_Explainability_and_Portfolios.setIcon(icon14)
        self.menu_Ethics_Explainability_and_Portfolios.setObjectName("menu_Ethics_Explainability_and_Portfolios")
        self.action_CreateDefaultFolders = QtGui.QAction(parent=MainWindow)
        self.action_CreateDefaultFolders.setObjectName("action_CreateDefaultFolders")
        self.action_UploadImages = QtGui.QAction(parent=MainWindow)
        self.action_UploadImages.setObjectName("action_UploadImages")
        self.action_UlpoadModels = QtGui.QAction(parent=MainWindow)
        self.action_UlpoadModels.setObjectName("action_UlpoadModels")
        self.action_UploadStyles = QtGui.QAction(parent=MainWindow)
        self.action_UploadStyles.setObjectName("action_UploadStyles")
        self.action_UploadVideos = QtGui.QAction(parent=MainWindow)
        self.action_UploadVideos.setObjectName("action_UploadVideos")
        self.action_UploadClassifiers = QtGui.QAction(parent=MainWindow)
        self.action_UploadClassifiers.setObjectName("action_UploadClassifiers")
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
        self.menuSettings.addAction(self.action_CreateDefaultFolders)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.action_UploadVideos)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.action_UploadClassifiers)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.action_UlpoadModels)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.action_UploadImages)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.action_UploadStyles)
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

        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Start Block 2
        self.manualSetup()     
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<End Block 2
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Computer Vision with Machine Learning and Deep Learning"))
        self.groupBox_FlipImage.setTitle(_translate("MainWindow", "Flip"))
        self.checkBox_FlipVertical.setText(_translate("MainWindow", "Vertical"))
        self.checkBox_FlipHorizantal.setText(_translate("MainWindow", "Horizantal"))
        self.checkBox_SwapTranspose.setText(_translate("MainWindow", "Swap Rows and Columns ( Transpose )"))
        self.groupBox_BGRColorSpace.setTitle(_translate("MainWindow", "BGR-RGB"))
        self.checkBox_GreenChannel.setText(_translate("MainWindow", "Green"))
        self.checkBox_RedChannel.setText(_translate("MainWindow", "Red"))
        self.checkBox_BlueChannel.setText(_translate("MainWindow", "Blue"))
        self.groupBox_HSVColorSpace.setTitle(_translate("MainWindow", "HSV"))
        self.checkBox_HSVHueChannel.setText(_translate("MainWindow", "Hue"))
        self.checkBox_HSVSaturation.setText(_translate("MainWindow", "Saturation"))
        self.checkBox_HSVValue.setText(_translate("MainWindow", "Value"))
        self.groupBox_ResizeScaleImageByDimention.setTitle(_translate("MainWindow", "Resize "))
        self.label_ResizeHeight.setText(_translate("MainWindow", "Height"))
        self.label_ResizeWidth.setText(_translate("MainWindow", "Width"))
        self.pushButton_LargerPyrUp.setText(_translate("MainWindow", "✚"))
        self.pushButton_SmallerPyrDown.setText(_translate("MainWindow", "━"))
        self.groupBox_RotationScale.setTitle(_translate("MainWindow", "Rotation | Scale"))
        self.label_RotationDegree.setText(_translate("MainWindow", "Set Rotation Degree"))
        self.label_RotationDegreeValue.setText(_translate("MainWindow", "0 degree"))
        self.label_RorationScale.setText(_translate("MainWindow", "Set Scale Coefficient"))
        self.label_RorationScaleValue.setText(_translate("MainWindow", "0 times"))
        self.groupBox_DrawingShape.setTitle(_translate("MainWindow", "Draw Shape"))
        self.comboBox_DrawShape.setItemText(1, _translate("MainWindow", "Line"))
        self.comboBox_DrawShape.setItemText(2, _translate("MainWindow", "Rectangle"))
        self.comboBox_DrawShape.setItemText(3, _translate("MainWindow", "Circle"))
        self.comboBox_DrawShape.setItemText(4, _translate("MainWindow", "Ellipse"))
        self.comboBox_DrawShape.setItemText(5, _translate("MainWindow", "PolyLines"))
        self.groupBox_Translation.setTitle(_translate("MainWindow", "Translation"))
        self.label_X1.setText(_translate("MainWindow", "X1"))
        self.label_X1_Value.setText(_translate("MainWindow", "10"))
        self.label_X2.setText(_translate("MainWindow", "X2"))
        self.label_X2_Value.setText(_translate("MainWindow", "100"))
        self.label_Y1.setText(_translate("MainWindow", "Y1"))
        self.label_Y1_Value.setText(_translate("MainWindow", "200"))
        self.label_Y2.setText(_translate("MainWindow", "Y2"))
        self.label_Y2_Value.setText(_translate("MainWindow", "50"))
        self.label_Z1.setText(_translate("MainWindow", "Z1"))
        self.label_Z1_Value.setText(_translate("MainWindow", "100"))
        self.label_Z2.setText(_translate("MainWindow", "Z2"))
        self.label_Z2_Value.setText(_translate("MainWindow", "250"))
        self.groupBox_AddText.setTitle(_translate("MainWindow", "Add Text"))
        self.pushButton_AddText.setText(_translate("MainWindow", "Add"))
        self.groupBox_Skew.setTitle(_translate("MainWindow", "Skew"))
        self.label_SkewHeight.setText(_translate("MainWindow", "Height"))
        self.label_SkewWidth.setText(_translate("MainWindow", "Width"))
        self.groupBox_Crop.setTitle(_translate("MainWindow", "Crop"))
        self.label_CropTopLefCoefficient.setText(_translate("MainWindow", "Top Left Coefficient"))
        self.label_CropTopLefCoefficientValue.setText(_translate("MainWindow", "0 %"))
        self.label_CropBottomRightCoefficient.setText(_translate("MainWindow", "Bottom Right Coefficient"))
        self.label_CropBottomRightCoefficientValue.setText(_translate("MainWindow", "100 %"))
        self.groupBox_ColorSpaceConversion.setTitle(_translate("MainWindow", "Color Space Conversion: "))
        self.comboBox_ColorSpaceConversion.setItemText(1, _translate("MainWindow", "BGR to Gray Scale"))
        self.comboBox_ColorSpaceConversion.setItemText(2, _translate("MainWindow", "BGR to RGB"))
        self.comboBox_ColorSpaceConversion.setItemText(3, _translate("MainWindow", "BGR to HSV"))
        self.comboBox_ColorSpaceConversion.setItemText(4, _translate("MainWindow", "RGB to Gray Scale"))
        self.comboBox_ColorSpaceConversion.setItemText(5, _translate("MainWindow", "RGB to BGR"))
        self.comboBox_ColorSpaceConversion.setItemText(6, _translate("MainWindow", "RGB to HSV"))
        self.comboBox_ColorSpaceConversion.setItemText(7, _translate("MainWindow", "HSV to RGB"))
        self.comboBox_ColorSpaceConversion.setItemText(8, _translate("MainWindow", "HSV to BGR"))
        self.groupBox_ImageInfo.setTitle(_translate("MainWindow", "Image Information:"))
        self.label_ImageWidth.setText(_translate("MainWindow", "Width:"))
        self.label_ImageHeight.setText(_translate("MainWindow", "Height:"))
        self.label_ImageDepth.setText(_translate("MainWindow", "Depth:"))
        self.label_ImageShape.setText(_translate("MainWindow", "Shape:"))
        self.pushButton_UploadVideos.setText(_translate("MainWindow", "Upload Videos"))
        self.label_SelectImage.setText(_translate("MainWindow", "Select Image:"))
        self.groupBox_VideoInfo.setTitle(_translate("MainWindow", "Video Information: "))
        self.label_SelectVideo.setText(_translate("MainWindow", "Select Video:"))
        self.pushButton_UploadImages.setText(_translate("MainWindow", "Upload Images"))
        self.pushButton_SaveImage.setText(_translate("MainWindow", "Save Image"))
        self.pushButton_SaveCode.setText(_translate("MainWindow", "Save Code"))
        self.groupBox_DilationErosionEdgeDetection.setTitle(_translate("MainWindow", "Dilation, Erosion, Opening, Closing, Edge Detection "))
        self.comboBox_DilationErosionEdgeDetection.setItemText(1, _translate("MainWindow", "Dilation, Erosion, Opening, Closing"))
        self.comboBox_DilationErosionEdgeDetection.setItemText(2, _translate("MainWindow", "Edge Detection by Canny (Normal, Wide, Narrow)"))
        self.comboBox_DilationErosionEdgeDetection.setItemText(3, _translate("MainWindow", "Edge Detection Comparison (Canny, Sobel, Laplacian)"))
        self.groupBox_ObjectDetection.setTitle(_translate("MainWindow", "Object Detection "))
        self.comboBox_ObjectDetection.setItemText(1, _translate("MainWindow", "Line Detection using HoughLines"))
        self.comboBox_ObjectDetection.setItemText(2, _translate("MainWindow", "Line Detection using Probablistic HoughLines"))
        self.comboBox_ObjectDetection.setItemText(3, _translate("MainWindow", "Circle Detection using HoughCircles"))
        self.comboBox_ObjectDetection.setItemText(4, _translate("MainWindow", "Blob Detection"))
        self.comboBox_ObjectDetection.setItemText(5, _translate("MainWindow", "Face and Eye Detection with HAAR Cascade Classifiers"))
        self.comboBox_ObjectDetection.setItemText(6, _translate("MainWindow", "Live Face and Eye Detection with HAAR Cascade Classifiers"))
        self.comboBox_ObjectDetection.setItemText(7, _translate("MainWindow", "Live People Detection with HAAR Cascade Classifiers"))
        self.comboBox_ObjectDetection.setItemText(8, _translate("MainWindow", "Live Car Detection with HAAR Cascade Classifiers"))
        self.groupBox_Filters.setTitle(_translate("MainWindow", "Filters (Bluring, Sharppening, De-Noising)"))
        self.comboBox_Filters.setItemText(1, _translate("MainWindow", "Bluring and Sharprning by Kernel"))
        self.comboBox_Filters.setItemText(2, _translate("MainWindow", "De-Noising by Filter"))
        self.comboBox_Filters.setItemText(3, _translate("MainWindow", "Bluring by Filter"))
        self.comboBox_Filters.setItemText(4, _translate("MainWindow", "Segmenting by Threshold - Binarization"))
        self.comboBox_Filters.setItemText(5, _translate("MainWindow", "Segmenting by Adaptive Threshold - Binarization"))
        self.groupBox_ArithmeticAndBitwiseOperations.setTitle(_translate("MainWindow", "Arithmetic and Bitwise Operations"))
        self.comboBox_ArithmeticAndBitwiseOperations.setItemText(1, _translate("MainWindow", "Arithmetic Operations"))
        self.comboBox_ArithmeticAndBitwiseOperations.setItemText(2, _translate("MainWindow", "Bitwise Operations"))
        self.groupBox_OCR.setTitle(_translate("MainWindow", "Optical Character Recognition (OCR) "))
        self.comboBox_OCR.setItemText(1, _translate("MainWindow", "OCR by Tesseract"))
        self.groupBox_SegmentationAndContours.setTitle(_translate("MainWindow", " Segmentation and Contours "))
        self.comboBox_SegmentationAndContours.setItemText(1, _translate("MainWindow", "Find Contours"))
        self.comboBox_SegmentationAndContours.setItemText(2, _translate("MainWindow", "Sort Contours"))
        self.comboBox_SegmentationAndContours.setItemText(3, _translate("MainWindow", "Sort Contours by Area"))
        self.comboBox_SegmentationAndContours.setItemText(4, _translate("MainWindow", "Sort Contours Left to Right"))
        self.comboBox_SegmentationAndContours.setItemText(5, _translate("MainWindow", "Approximate Contours by ApproxPolyDP"))
        self.comboBox_SegmentationAndContours.setItemText(6, _translate("MainWindow", "Approximate Contours by ConvexHull"))
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
        #
        self.menu_PreRequisites.setTitle(_translate("MainWindow", "Pre Requisites"))  #*******************************
        self.menu_FundamentalOfComputerVision.setTitle(_translate("MainWindow", "Fundamental of Computer Vision"))  #****************************
        self.menu_Machine_Learning_Model_Fundamentals.setTitle(_translate("MainWindow", "Machine Learning Model Fundamentals"))  #*******************************
        self.menu_Deep_Learning_Foundations.setTitle(_translate("MainWindow", "Deep Learning Foundations"))  #*******************************
        self.menu_Core_CV_Computer_Vision_Tasks.setTitle(_translate("MainWindow", "Core CV (Computer Vision) Tasks"))  #*******************************
        self.menu_Advanced_Generative_Models_Architectures.setTitle(_translate("MainWindow", "Advanced & Generative Models & Architectures"))  #*******************************
        self.menu_Applications_Deployment_Optimization.setTitle(_translate("MainWindow", "Applications Deployment & Optimization"))  #*******************************
        self.menu_Ethics_Explainability_and_Portfolios.setTitle(_translate("MainWindow", "Ethics, Explainability, and Portfolios"))  #*******************************
        #
        self.action_CreateDefaultFolders.setText(_translate("MainWindow", "📁 Create Default Folders"))
        self.action_UploadImages.setText(_translate("MainWindow", "⤴️ Upload Images"))
        self.action_UlpoadModels.setText(_translate("MainWindow", "🔼 Ulpoad Models"))
        self.action_UploadStyles.setText(_translate("MainWindow", "⏫ Upload Styles"))
        self.action_UploadVideos.setText(_translate("MainWindow", "📤Upload Videos"))
        self.action_UploadClassifiers.setText(_translate("MainWindow", "⏏️Upload Classifiers"))
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Start Block 3
        self.menu_Mathematics.setTitle(_translate("MainWindow", "🧮 Mathematics"))
        self.action_LinearAlgebraAndCalculus.setText(_translate("MainWindow", "📉 Linear Algebra and Calculus"))
        self.action_ProbabilityAndStatistics.setText(_translate("MainWindow", "🎲 Probability and Statistics"))
        self.menu_PythonProgramming.setTitle(_translate("MainWindow", "🐍 Python Programming"))
        self.action_PythonProgramming.setText(_translate("MainWindow", "🐍 Base of Python Programming"))
        self.action_Numpy.setText(_translate("MainWindow", "🔢 Numpy Library Sheet"))
        self.action_Pandas.setText(_translate("MainWindow", "🥨 Pandas Library Sheet"))
        self.action_MatPlotLib.setText(_translate("MainWindow", "📊 MatPlotLib Library Sheet"))
        self.action_SeaBorn.setText(_translate("MainWindow", "📊 SeaBorn Library Sheet"))
        self.action_CoreMachineLearningPrinciples.setTitle(_translate("MainWindow", "🧠 Core Machine Learning Principles"))
        self.action_MLBigPicture.setText(_translate("MainWindow", "🖼️ ML Big Picture"))
        self.action_CategorizingByLearningParadigm.setText(_translate("MainWindow", "🗂️ Categorizing by Learning Paradigm"))
        self.action_FromFundamentalsToAdvanced.setText(_translate("MainWindow", "🔥 From Fundamentals to Advanced"))
        self.action_MLModelOverview.setText(_translate("MainWindow", "🌌 ML Model Overview"))
        self.action_CoreMLModelFormatSpecification.setText(_translate("MainWindow", "📚 Core ML Model Format Specification"))
        self.action_SupervisedMLProcess.setText(_translate("MainWindow", "🎵 Supervised ML Process"))
        self.action_CodeSamplesByLearningParadigm.setText(_translate("MainWindow", "📜 Code Samples by Learning Paradigm"))
        self.action_DeeperCodeSamplesWithDefinitions.setText(_translate("MainWindow", "🔍 Deeper Code Samples with Definitions"))
        self.action_TheoreticalFoundationsOfComputerVision.setText(_translate("MainWindow", "👀 Theoretical"))
        self.action_PracticalFoundationsOfComputerVision.setTitle(_translate("MainWindow", "🛠 Practical"))
        self.action_ImagesAndColorsManipulationsAndOprations.setText(_translate("MainWindow", "🎨 Images and Colors Manipulations And Oprations"))
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<End Block 3

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Start Block 4
    
    def connectActions(self):
        self.action_BigPicture.triggered.connect(partial(self.changePDFPage,0))
        self.action_UniversityCurriculum.triggered.connect(partial(self.changePDFPage,1))
        self.action_RoadMap.triggered.connect(partial(self.changePDFPage,2))
        self.action_StudyPlan.triggered.connect(partial(self.changePDFPage,3))
        self.action_HeadingResearch.triggered.connect(partial(self.changePDFPage,4))
        self.action_UserGuide.triggered.connect(partial(self.changePDFPage,5))
        self.action_MLBigPicture.triggered.connect(partial(self.changePDFPage,6))
        self.action_CategorizingByLearningParadigm.triggered.connect(partial(self.changePDFPage,7))
        self.action_FromFundamentalsToAdvanced.triggered.connect(partial(self.changePDFPage,8))
        self.action_CodeSamplesByLearningParadigm.triggered.connect(partial(self.changePDFPage,9))
        self.action_DeeperCodeSamplesWithDefinitions.triggered.connect(partial(self.changePDFPage,10))
        self.action_TheoreticalFoundationsOfComputerVision.triggered.connect(partial(self.changePDFPage,11))
        self.action_Numpy.triggered.connect(partial(self.changePDFPage,12))
        self.action_Pandas.triggered.connect(partial(self.changePDFPage,13))
        self.action_MatPlotLib.triggered.connect(partial(self.changePDFPage,14))
        self.action_SeaBorn.triggered.connect(partial(self.changePDFPage,15))
        self.action_SupervisedMLProcess.triggered.connect(partial(self.changePDFPage,16))

        self.action_AboutTool.triggered.connect(self.changePage)
        self.action_AboutAuthorDeveloper.triggered.connect(self.changePage)
        self.action_CloseOtherWindows.triggered.connect(self.closeWindow)
        self.action_CloseMainWindow.triggered.connect(self.closeWindow)
        self.action_CloseAllWindows.triggered.connect(self.closeWindow)
        self.action_PythonProgramming.triggered.connect(self.changePage)
        self.action_LinearAlgebraAndCalculus.triggered.connect(self.changePage)
        self.action_ProbabilityAndStatistics.triggered.connect(self.changePage)
        self.action_ImagesAndColorsManipulationsAndOprations.triggered.connect(self.changePage)
        self.action_CreateDefaultFolders.triggered.connect(self.CheckCreateDefaultFolders)

        self.action_ProbabilityAndStatistics.triggered.connect(partial(self.pdf_in_browser,"https://mml-book.github.io/book/mml-book.pdf",False))
        self.action_PythonProgramming.triggered.connect(partial(self.pdf_in_browser,"https://www.w3schools.com/python/default.asp",False))
        self.action_LinearAlgebraAndCalculus.triggered.connect(partial(self.pdf_in_browser,"https://github.com/Ryota-Kawamura/Mathematics-for-Machine-Learning-and-Data-Science-Specialization",False))
        self.action_MLModelOverview.triggered.connect(partial(self.pdf_in_browser,"https://apple.github.io/coremltools/docs-guides/source/mlmodel.html",False))
        self.action_CoreMLModelFormatSpecification.triggered.connect(partial(self.pdf_in_browser,"https://apple.github.io/coremltools/mlmodel/index.html",False))

        self.action_UploadImages.triggered.connect(self.upload_files)
        self.action_UploadVideos.triggered.connect(self.upload_files)
        self.pushButton_UploadImages.clicked.connect(self.upload_files)
        self.pushButton_UploadVideos.clicked.connect(self.upload_files)
        self.comboBox_SelectImage.currentTextChanged.connect(self.PrepareSelectImageComboBox)
        self.comboBox_ColorSpaceConversion.currentTextChanged.connect(self.PrepareConvertColorSpace)
        self.ImagesAndColorsHandler.valueChanged.connect(self.SetImageInfo)
        self.pushButton_SaveCode.clicked.connect(self.SaveImagesAndColorsCode)    
        self.pushButton_SaveImage.clicked.connect(self.ImagesAndColorsHandler.SaveImage)
        self.ImagesAndColorsHandler.ImageSizeChanged.connect(self.ImageSizeChanged)
        
        for channel in self.ColorChannelChangeCheckBoxes:
            channel.clicked.connect(partial(self.PrepareColorChannelRemove,channel.objectName()))#stateChanged

        for translation in self.TranslationDials:
             translation.valueChanged.connect(self.PrepareTranslateImage)
        
        self.horizontalSlider_SkewHeight.valueChanged.connect(self.PrepareSkewImage)
        self.horizontalSlider_SkewWidth.valueChanged.connect(self.PrepareSkewImage)
        self.horizontalSlider_ResizeHeight.valueChanged.connect(self.PrepareResizeImage)
        self.horizontalSlider_ResizeWidth.valueChanged.connect(self.PrepareResizeImage)
        self.pushButton_LargerPyrUp.clicked.connect(self.PreparePyrUpDown)
        self.pushButton_SmallerPyrDown.clicked.connect(self.PreparePyrUpDown)
        self.ImagesAndColorsHandler.ResetParams.connect(self.ResetParams)
        self.dial_RotationScale.valueChanged.connect(self.PrepareScaleByCoefficient)
        self.dial_RotationDegree.valueChanged.connect(self.PrepareRotationByAngle)
        self.checkBox_FlipHorizantal.checkStateChanged.connect(self.PrepareFlip)
        self.checkBox_FlipVertical.checkStateChanged.connect(self.PrepareFlip)
        self.checkBox_SwapTranspose.checkStateChanged.connect(self.PrepareTranspose)
        self.horizontalSlider_CropTopLefCoefficient.valueChanged.connect(self.PrepareCrop)
        self.horizontalSlider_CropBottomRightCoefficient.valueChanged.connect(self.PrepareCrop)
        self.pushButton_AddText.clicked.connect(self.PrepareAddText)
        self.comboBox_DrawShape.currentTextChanged.connect(self.PrepareDrawShape)
        self.comboBox_ArithmeticAndBitwiseOperations.currentTextChanged.connect(self.PrepareOperations)
        self.comboBox_Filters.currentTextChanged.connect(self.PrepareFilters)
        self.comboBox_DilationErosionEdgeDetection.currentTextChanged.connect(self.PrepareDilationErosionEdgeDetection)

    def PrepareOperations(self,operation):
        if str(operation).strip() != "":
           self.ImagesAndColorsHandler.Operations(operation.strip())

    def PrepareFilters(self,filter):
        if str(filter).strip() != "":
           self.ImagesAndColorsHandler.Filters(filter.strip()) 

    def PrepareDilationErosionEdgeDetection(self,operation):
        if str(operation).strip() != "":
           self.ImagesAndColorsHandler.DilationErosionEdgeDetection(operation.strip())     

    def PrepareDrawShape(self,shape):
        if str(shape).strip() != "":
           self.ImagesAndColorsHandler.DrawShape(shape)
        # else:
        #      QMessageBox.warning(None, "No Shape Selected", "First, Select a Shape!")

    def PrepareAddText(self):
        text = self.textEdit_AddText.toPlainText().strip()
        if text != "":
             self.ImagesAndColorsHandler.AddText(text)     
        else:
             QMessageBox.warning(None, "Empty Text", "First, Write a Text!")
                
    def PrepareCrop(self):
        # print(value,self.sender().objectName())
        if self.label_ImageShapeValue.text().strip() != ""  and self.ImagesAndColorsHandler.image is not None: 
            name = self.sender().objectName().split("_")[1]
            if name == "CropTopLefCoefficient":
                 self.label_CropTopLefCoefficientValue.setText(str(self.horizontalSlider_CropTopLefCoefficient.value()) +" %")
                 QMessageBox.warning(None, "Top Lef Coefficient is Set", "Set Bottom Right Coefficient to Continue!") 
            else:
                TopLeft= self.horizontalSlider_CropTopLefCoefficient.value()
                BottomRight = self.horizontalSlider_CropBottomRightCoefficient.value()
                if TopLeft == 0 or TopLeft == 100 or BottomRight == 0 or BottomRight == 100:
                   QMessageBox.critical(None, "Coefficient Error", "Coefficient Can't be 0 % or 100 %!")  
                else:
                    self.lower()
                    cv2.destroyAllWindows()
                    self.label_CropBottomRightCoefficientValue.setText(str(BottomRight) + " %")
                    self.ImagesAndColorsHandler.Crop(TopLeft/100,BottomRight/100) 
         
    def PrepareTranspose(self):
        if self.label_ImageShapeValue.text().strip() != "" and self.ImagesAndColorsHandler.image is not None: 
            self.lower()
            cv2.destroyAllWindows()
            self.ImagesAndColorsHandler.Transpose()

    def PrepareFlip(self,check):
        if self.label_ImageShapeValue.text().strip() != "" and self.ImagesAndColorsHandler.image is not None: 
            self.lower()
            cv2.destroyAllWindows()
            name = self.sender().objectName().split("_")[1]
            self.ImagesAndColorsHandler.Flip(name)

    def PrepareRotationByAngle(self,angle):
          if self.label_ImageShapeValue.text().strip() != "" and self.ImagesAndColorsHandler.image is not None: 
             if angle == 0:
                QMessageBox.critical(None, "Value Error", "Angle Must be Greater than 0!") 
             else:
                self.lower()
                cv2.destroyAllWindows()
                self.label_RotationDegreeValue.setText(str(angle) + " degree")
                self.ImagesAndColorsHandler.RotationByAngle(angle)

    def PrepareScaleByCoefficient(self,coefficient):
          if self.label_ImageShapeValue.text().strip() != "" and self.ImagesAndColorsHandler.image is not None: 
             if coefficient == 0:
                QMessageBox.critical(None, "Value Error", "Coefficient Must be Greater than 0!") 
             else:
                self.lower()
                cv2.destroyAllWindows()
                self.label_RorationScaleValue.setText(str(coefficient) + " times")
                self.ImagesAndColorsHandler.ScaleByCoefficient(coefficient)       

    def PrepareTranslateImage(self,value):
        if  self.ImagesAndColorsHandler.image is not None: 
            self.lower()
            cv2.destroyAllWindows()
            name = self.sender().objectName().split("_")[1]
            Diff_Array = [
                 [self.dial_X1.value(),self.dial_X2.value()],
                 [self.dial_Y1.value(),self.dial_Y2.value()],
                 [self.dial_Z1.value(),self.dial_Z2.value()]
            ]
            for TranslationLabelValue in self.TranslationLabelValues:
                 dialName = "dial_" + TranslationLabelValue.objectName().split("_")[1]
                 dial =  [dial for dial in self.TranslationDials if dial.objectName() == dialName]
                 TranslationLabelValue.setText(str(dial[0].value()))
            self.ImagesAndColorsHandler.TranslateImage(name,value,np.float32(Diff_Array))

    def PrepareSkewImage(self,value):
        #print(value,type(value))
        if self.label_ImageShapeValue.text().strip() != "" and self.ImagesAndColorsHandler.image is not None: 
            self.lower()
            cv2.destroyAllWindows()
            name = self.sender().objectName().split("_")[1]
            #value = self.sender().value()
            #time.sleep(0.1)
            self.ImagesAndColorsHandler.SkewImage(name,value)

    def PrepareResizeImage(self,value):
        if self.label_ImageShapeValue.text().strip() != "" and self.ImagesAndColorsHandler.image is not None: 
            self.lower()
            cv2.destroyAllWindows()
            name = self.sender().objectName().split("_")[1]
            self.ImagesAndColorsHandler.ResizeImage(name,value)

    def PreparePyrUpDown(self):
        if self.label_ImageShapeValue.text().strip() != "" and self.ImagesAndColorsHandler.image is not None: 
            self.lower()
            cv2.destroyAllWindows()
            name = self.sender().objectName().split("_")[1]
            self.ImagesAndColorsHandler.PyrUpDown(name)    

    def ResetParams(self):
        self.lower()
        cv2.destroyAllWindows()
        self.comboBox_SelectImage.blockSignals(True)
        self.comboBox_SelectImage.setCurrentIndex(0)
        self.comboBox_SelectImage.blockSignals(False)
        self.textEdit_AddText.clear()
        self.comboBox_ColorSpaceConversion.setCurrentIndex(0)      
        self.comboBox_ArithmeticAndBitwiseOperations.setCurrentIndex(0)
        self.comboBox_Filters.setCurrentIndex(0)
        self.comboBox_DilationErosionEdgeDetection.setCurrentIndex(0)
        self.comboBox_DrawShape.setCurrentIndex(0)
        
        self.comboBox_SegmentationAndContours.setCurrentIndex(0)
        self.comboBox_ObjectDetection.setCurrentIndex(0)
        self.comboBox_OCR.setCurrentIndex(0)

        self.label_ImageShapeValue.clear()
        self.label_ImageHeightValue.clear() 
        self.label_ImageWidthValue.clear()
        self.label_ImageDepthValue.clear() 

        for counter, option in enumerate(self.ColorChannelChangeCheckBoxes):
                option.setChecked(False)
                option.setDisabled(True)
                option.setEnabled(False)
        
        self.ImagesAndColorsHandler.image = None
        self.ImagesAndColorsHandler.imageName = None
        self.ImagesAndColorsHandler.imageConversion = None
        self.ImagesAndColorsHandler.tempImage = None
        self.ImagesAndColorsHandler.tempImageName = None

        self.label_X1_Value.setText("10")
        self.label_X2_Value.setText("100")
        self.label_Y1_Value.setText("200")
        self.label_Y2_Value.setText("50")
        self.label_Z1_Value.setText("100")
        self.label_Z2_Value.setText("250")
        self.dial_X1.setValue(10)
        self.dial_X2.setValue(100)
        self.dial_Y1.setValue(200)
        self.dial_Y2.setValue(50)
        self.dial_Z1.setValue(100)
        self.dial_Z2.setValue(250)       

        self.label_CropBottomRightCoefficientValue.setText("100 %")
        self.label_CropTopLefCoefficientValue.setText("0 %")
        self.horizontalSlider_CropBottomRightCoefficient.setValue(100)
        self.horizontalSlider_CropTopLefCoefficient.setValue(0)

        self.label_RotationDegreeValue.setText("0 degree")
        self.label_RorationScaleValue.setText("0 times")
        self.dial_RotationDegree.setValue(0)
        self.dial_RotationScale.setValue(0)

        self.comboBox_DrawShape.blockSignals(True)
        self.comboBox_DrawShape.setCurrentIndex(0)
        self.comboBox_DrawShape.blockSignals(False)

        self.horizontalSlider_ResizeHeight.blockSignals(True)
        self.horizontalSlider_ResizeWidth.blockSignals(True)
        self.horizontalSlider_SkewHeight.blockSignals(True)
        self.horizontalSlider_SkewWidth.blockSignals(True)
        self.horizontalSlider_ResizeHeight.setValue(50)   
        self.horizontalSlider_ResizeWidth.setValue(50)   
        self.horizontalSlider_SkewHeight.setValue(50)                          
        self.horizontalSlider_SkewWidth.setValue(50) 
        self.horizontalSlider_ResizeHeight.blockSignals(False)
        self.horizontalSlider_ResizeWidth.blockSignals(False)
        self.horizontalSlider_SkewHeight.blockSignals(False)
        self.horizontalSlider_SkewWidth.blockSignals(False)  

        self.dial_X1.blockSignals(True)
        self.dial_X2.blockSignals(True)
        self.dial_Y1.blockSignals(True)
        self.dial_Y2.blockSignals(True)
        self.dial_Z1.blockSignals(True)
        self.dial_Z2.blockSignals(True)    
        self.dial_X1.setValue(10)
        self.dial_X2.setValue(100)
        self.dial_Y1.setValue(200)
        self.dial_Y2.setValue(50)
        self.dial_Z1.setValue(100)
        self.dial_Z2.setValue(250) 
        self.dial_X1.blockSignals(False)
        self.dial_X2.blockSignals(False)
        self.dial_Y1.blockSignals(False)
        self.dial_Y2.blockSignals(False)
        self.dial_Z1.blockSignals(False)
        self.dial_Z2.blockSignals(False)                     

    def PrepareColorChannelRemove(self,text,check):
        if self.ImagesAndColorsHandler.image is not None and self.ImagesAndColorsHandler.imageName is not None:
             channels = {}
             for channel in self.ColorChannelChangeCheckBoxes:
                 channels[channel.objectName().split("_")[1]] = channel.isChecked()
                 if channel.isChecked():pass
                 else:
                      channel.setDisabled(True)
                      channel.setEnabled(False)
             
             self.ImagesAndColorsHandler.ColorChannelRemove(channels)

        else:
             QMessageBox.warning(None, "No Image Selected", "First, Select an Image!")
   
    def PrepareSelectImageComboBox(self,text):
        self.lower()
        cv2.destroyAllWindows()
        self.comboBox_ColorSpaceConversion.setCurrentIndex(0)
        self.comboBox_ArithmeticAndBitwiseOperations.setCurrentIndex(0)
        self.comboBox_Filters.setCurrentIndex(0)
        self.comboBox_DilationErosionEdgeDetection.setCurrentIndex(0)
        self.comboBox_DrawShape.setCurrentIndex(0)
        self.comboBox_SegmentationAndContours.setCurrentIndex(0)
        self.comboBox_ObjectDetection.setCurrentIndex(0)
        self.comboBox_OCR.setCurrentIndex(0)
        self.textEdit_AddText.clear()

        self.label_ImageShapeValue.clear()
        self.label_ImageHeightValue.clear() 
        self.label_ImageWidthValue.clear()
        self.label_ImageDepthValue.clear() 

        self.comboBox_DrawShape.blockSignals(True)
        self.comboBox_DrawShape.setCurrentIndex(0)
        self.comboBox_DrawShape.blockSignals(False)

        self.horizontalSlider_ResizeHeight.setValue(50)   
        self.horizontalSlider_ResizeWidth.setValue(50)   
        self.horizontalSlider_SkewHeight.setValue(50)                          
        self.horizontalSlider_SkewWidth.setValue(50) 
       
        for counter, option in enumerate(self.ColorChannelChangeCheckBoxes):
                option.setChecked(False)
                option.setDisabled(True)
                option.setEnabled(False)

        self.ImagesAndColorsHandler.tempImage = None
        self.ImagesAndColorsHandler.tempImageName = None
        if self.is_valid_extension(text.strip(),"image"):
           self.ImagesAndColorsHandler.ReadShowImage(text)
        else:
             self.comboBox_SelectImage.blockSignals(True)
             self.comboBox_SelectImage.setCurrentIndex(0)
             self.ImagesAndColorsHandler.image = None
             self.ImagesAndColorsHandler.imageName = None
             self.ImagesAndColorsHandler.imageConversion = None
             self.ResetParams()
             self.comboBox_SelectImage.blockSignals(False)            
             QMessageBox.critical(None, "Image Extension Error", "Valid Extensions: " + " jpg , jpeg , png , gif , bmp , psd ")

    def PrepareConvertColorSpace(self,text):
        if text.strip() != "":
            self.comboBox_ArithmeticAndBitwiseOperations.setCurrentIndex(0)
            self.comboBox_Filters.setCurrentIndex(0)
            self.comboBox_DilationErosionEdgeDetection.setCurrentIndex(0)
            self.comboBox_SegmentationAndContours.setCurrentIndex(0)
            self.comboBox_ObjectDetection.setCurrentIndex(0)
            self.comboBox_OCR.setCurrentIndex(0)
            self.comboBox_DrawShape.setCurrentIndex(0)
            self.textEdit_AddText.clear()

            self.ImagesAndColorsHandler.ConvertColorSpace(text)       

    def ImageSizeChanged(self, text):
           
            shape = self.ImagesAndColorsHandler.image.shape
            height = self.ImagesAndColorsHandler.image.shape[0]
            width = self.ImagesAndColorsHandler.image.shape[1]

            self.horizontalSlider_ResizeHeight.blockSignals(True)
            self.horizontalSlider_ResizeWidth.blockSignals(True)
            self.horizontalSlider_SkewHeight.blockSignals(True)
            self.horizontalSlider_SkewWidth.blockSignals(True)
            self.horizontalSlider_ResizeHeight.setValue(height)   
            self.horizontalSlider_ResizeWidth.setValue(width)   
            self.horizontalSlider_SkewHeight.setValue(height)                          
            self.horizontalSlider_SkewWidth.setValue(width) 
            self.horizontalSlider_ResizeHeight.blockSignals(False)
            self.horizontalSlider_ResizeWidth.blockSignals(False)
            self.horizontalSlider_SkewHeight.blockSignals(False)
            self.horizontalSlider_SkewWidth.blockSignals(False) 

            self.label_ImageShapeValue.setText(str(shape))
            self.label_ImageHeightValue.setText(str(height))  
            self.label_ImageWidthValue.setText(str(width))
            if self.ImagesAndColorsHandler.imageConversion not in ["BGR2GRAY","RGB2GRAY"]:
                depth = self.ImagesAndColorsHandler.image.shape[2]       
                self.label_ImageDepthValue.setText(str(depth))
              
    def SetImageInfo(self,text):
        if  self.ImagesAndColorsHandler.image is not None: #self.comboBox_SelectImage.currentText().strip() != "" and
            shape = self.ImagesAndColorsHandler.image.shape
            height = self.ImagesAndColorsHandler.image.shape[0]
            width = self.ImagesAndColorsHandler.image.shape[1]

            self.horizontalSlider_ResizeHeight.setValue(height)   
            self.horizontalSlider_ResizeWidth.setValue(width)   
            self.horizontalSlider_SkewHeight.setValue(height)                          
            self.horizontalSlider_SkewWidth.setValue(width)  

            self.label_ImageShapeValue.setText(str(shape))
            self.label_ImageHeightValue.setText(str(height))  
            self.label_ImageWidthValue.setText(str(width))
            if self.ImagesAndColorsHandler.imageConversion not in ["BGR2GRAY","RGB2GRAY"]:
                depth = self.ImagesAndColorsHandler.image.shape[2]       
                self.label_ImageDepthValue.setText(str(depth))
            
            if self.ImagesAndColorsHandler.imageConversion is not None:
               match self.ImagesAndColorsHandler.imageConversion:
                    case "BGR2GRAY"|"RGB2GRAY":
                        for counter, option in enumerate(self.ColorChannelChangeCheckBoxes):
                                option.setDisabled(True)
                                option.setEnabled(False)
                                option.setChecked(False)

                    case "BGR2RGB"|"RGB2BGR"|"HSV2BGR"|"HSV2RGB":
                        for counter, option in enumerate(self.ColorChannelChangeCheckBoxes):
                                if counter in [0,1,2]:
                                    option.setDisabled(False)
                                    option.setEnabled(True)
                                    option.setChecked(True)
                                else:
                                    option.setDisabled(True)
                                    option.setEnabled(False)
                                    option.setChecked(False)
                                                                        
                    case "BGR2HSV"|"RGB2HSV":
                        for counter, option in enumerate(self.ColorChannelChangeCheckBoxes):
                                if counter in [3,4,5]:
                                    option.setDisabled(False)
                                    option.setEnabled(True)
                                    option.setChecked(True)
                                else:
                                    option.setDisabled(True)
                                    option.setEnabled(False)
                                    option.setChecked(False)
                  
            else:
                for counter, option in enumerate(self.ColorChannelChangeCheckBoxes):
                                    if counter in [0,1,2]:
                                        option.setDisabled(False)
                                        option.setEnabled(True)
                                        option.setChecked(True)
                                    else:
                                        option.setDisabled(True)
                                        option.setEnabled(False)
                                        option.setChecked(False)

        else:
            self.lower()
            cv2.destroyAllWindows()
            self.comboBox_ColorSpaceConversion.setCurrentIndex(0)
            self.label_ImageShapeValue.clear()
            self.label_ImageHeightValue.clear() 
            self.label_ImageWidthValue.clear()
            self.label_ImageDepthValue.clear()
            self.horizontalSlider_ResizeHeight.setValue(50)   
            self.horizontalSlider_ResizeWidth.setValue(50)   
            self.horizontalSlider_SkewHeight.setValue(50)                          
            self.horizontalSlider_SkewWidth.setValue(50)  
            for counter, option in enumerate(self.ColorChannelChangeCheckBoxes):
                    option.setChecked(False)
                    option.setDisabled(True)
                    option.setEnabled(False)
                  
    def messageBox(self,type,title,contents):
          match type:
              case "red":
                  QMessageBox.critical(self, title, contents)
              case "blue":
                  QMessageBox.information(self, title, contents)
              case "yellow":
                  QMessageBox.warning(self, title, contents)
              
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

    def CheckCreateDefaultFolders(self):
            base = os.path.normpath("resources")
            if os.path.isdir(base):
                pass
            else:
                os.makedirs(base, exist_ok=True)
            images = os.path.normpath(join("resources","images")) 
            models = os.path.normpath(join("resources","models")) 
            styles = os.path.normpath(join("resources","styles"))
            videos = os.path.normpath(join("resources","videos"))  
            if os.path.isdir(images):
                pass
            else:
                os.makedirs(images, exist_ok=True)
            if os.path.isdir(models):
                pass
            else:
                os.makedirs(models, exist_ok=True)
            if os.path.isdir(styles):
                pass
            else:
                os.makedirs(styles, exist_ok=True)
            if os.path.isdir(videos):
                pass
            else:
                os.makedirs(videos, exist_ok=True)

    def split_emojis(self,text):
        return regex.sub(r'\p{Emoji}', '', text)

    def upload_files(self,type):
          self.CheckCreateDefaultFolders()
          destination_folder = os.path.normpath("resources")
          senderObject = self.sender()
          sender = (self.split_emojis(senderObject.text())).strip()
          #print(sender)
          file_paths, _ = QFileDialog.getOpenFileNames(self, "Select File", "", "All Files (*);;Text Files (*.txt)")
          if file_paths:
               # Copy each file
               for path in file_paths:
                    file_name = os.path.basename(path)

                    if sender.__contains__("Upload Models"):
                        destination_folder = os.path.normpath(join("resources","models")) 
                    if sender.__contains__("Upload Images"):
                        if self.is_valid_extension(file_name.strip(),"image"):
                           destination_folder = os.path.normpath(join("resources","images")) 
                        else:
                            QMessageBox.critical(None, "Image Extension Error: " + file_name, "Valid Extensions: " + " jpg , jpeg , png , gif , bmp , psd ")
                        
                    if sender.__contains__("Upload Styles"):
                        destination_folder = os.path.normpath(join("resources","styles")) 

                    if sender.__contains__("Upload Videos"):
                        if self.is_valid_extension(file_name.strip(),"video"):
                           destination_folder = os.path.normpath(join("resources","Videos"))  
                        else:
                            QMessageBox.critical(None, "Video Extension Error: " + file_name, "Valid Extensions: " + " avi , mp4 , mpg , mpeg , mov , wmv , mkv , flv ")                   
                        
                    dest_path = os.path.join(destination_folder, file_name)
                    if destination_folder != os.path.normpath("resources"):
                       shutil.copy2(path, dest_path)                         

               self.LoadResources()
               #print(f"Selected file: {file_paths}")
     
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
                  self.pdf_path = os.path.relpath("pages/ML_BigPicture.pdf")
             case 7:
                  self.pdf_path = os.path.relpath("pages/CategorizingByLearningParadigm.pdf")
             case 8:
                  self.pdf_path = os.path.relpath("pages/FromFundamentalsToAdvanced.pdf")
             case 9:
                  self.pdf_path = os.path.relpath("pages/CodeSamplesByLearningParadigm.pdf")
             case 10:
                  self.pdf_path = os.path.relpath("pages/DeeperCodeSamplesWithDefinitions.pdf")
             case 11:
                  self.pdf_path = os.path.relpath("pages/TheoreticalFoundationsOfComputerVision.pdf")
             case 12:
                  self.pdf_path = os.path.relpath("pages/Numpy_Sheet.pdf")
             case 13:
                  self.pdf_path = os.path.relpath("pages/Pandas_Sheet.pdf")
             case 14:
                  self.pdf_path = os.path.relpath("pages/MatPlotLib_Sheet.pdf")
             case 15:
                  self.pdf_path = os.path.relpath("pages/SeaBorn_Sheet.pdf")
             case 16:
                  self.pdf_path = os.path.relpath("pages/SupervisedML_Process.pdf")
                  
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

    def LoadResources(self):
        Base_Image_Path = os.path.normpath(join("resources","videos"))
        for f in listdir(Base_Image_Path):
            if isfile(join(Base_Image_Path, f)) and self.is_valid_extension(f.strip(),"video"):             
               if self.comboBox_SelectVideo.findText(f) == -1 :
                  self.comboBox_SelectVideo.addItem(f) 
                   
        Base_Image_Path = os.path.normpath(join("resources","images"))
        for f in listdir(Base_Image_Path):
            if isfile(join(Base_Image_Path, f)) and self.is_valid_extension(f.strip(),"image"):             
               if self.comboBox_SelectImage.findText(f) == -1 :
                  self.comboBox_SelectImage.addItem(f)   

               #    index = self.comboBox_SelectImage.findText(f)                           
               #    self.comboBox_SelectImage.setCurrentIndex(index)
     #    for index in range(self.comboBox_SelectImage.count()):
     #        if self.comboBox_SelectImage.itemText(index).strip() == "":
     #            self.comboBox_SelectImage.removeItem(index)                                         

     #    model_file_path = os.path.normpath(join("resources","models"))# "./models/"
     #    for f in listdir(model_file_path):
     #        if isfile(join(model_file_path, f)):
     #           if self.comboBox_1.findText(f) == -1 :
     #              self.comboBox_1.addItem(f)
     #              index = self.comboBox_1.findText(f)
     #              self.comboBox_1.setCurrentIndex(index)

     #    for index in range(self.comboBox_1.count()):
     #        if self.comboBox_1.itemText(index).strip() == "":
     #            self.comboBox_1.removeItem(index)  

    def closeEvent(self, event: QCloseEvent):
        #print(self.sender().objectName())
        event.accept()  

    def FillImagesAndColorsCode(self):
        function_code = inspect.getsource(ImagesAndColorsManipulationsAndOprations)
        lines = function_code.splitlines()[13:]
        commentCount = 0
        ChangedContent = ""
        for index,line in enumerate(lines):
            #print(index)
            stripedLine = line.strip()
            if lines[index].strip().startswith("'''"): commentCount += 1
            if stripedLine.startswith("#") or (commentCount % 2 != 0 or lines[index].strip().startswith("'''")):
                line = "<span style='color: green'>" + line +"</span>" #.strip()
            ChangedContent += line +"\n"
        self.textBrowser_ImageAndColors.setHtml(("<pre>" + ChangedContent ).strip())
        self.textBrowser_ImageAndColors.show()

    def SaveImagesAndColorsCode(self):
        # Choose file location
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;HTML Files (*.html);;All Files (*)")
        if file_path:
            content = ""
            # Choose between plain text or HTML
            if(file_path.endswith("html") or file_path.endswith("htm")):
                content = self.textBrowser_ImageAndColors.toHtml()                
            else:
                content = self.textBrowser_ImageAndColors.toPlainText()
            with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

    def is_valid_extension(self,file_name,file_type):
        match file_type:
             case "image":
                  valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp','.psd'}
             case "video":
                  valid_extensions = {'.avi','.mp4','.mpg','.mpeg','.mov','.WMV','.MKV','.FLV'}
        return any(file_name.lower().endswith(extension) for extension in valid_extensions)

    def manualSetup(self):
        self.ImagesAndColorsHandler = ImagesAndColorsManipulationsAndOprations()
        self.ColorChannelChangeCheckBoxes = [
            self.checkBox_BlueChannel,
            self.checkBox_GreenChannel,
            self.checkBox_RedChannel,
            self.checkBox_HSVHueChannel,
            self.checkBox_HSVSaturation,
            self.checkBox_HSVValue
        ]
        for channel in self.ColorChannelChangeCheckBoxes:
                channel.setDisabled(True)
                channel.setEnabled(False)

        self.TranslationDials = [
             self.dial_X1,
             self.dial_Y1,
             self.dial_Z1,
             self.dial_X2,
             self.dial_Y2,
             self.dial_Z2
        ]

        self.dial_X1.setValue(10)
        self.dial_X2.setValue(100)
        self.dial_Y1.setValue(200)
        self.dial_Y2.setValue(50)
        self.dial_Z1.setValue(100)
        self.dial_Z2.setValue(250)

        self.TranslationLabelValues = [
             self.label_X1_Value,
             self.label_X2_Value,
             self.label_Y1_Value,
             self.label_Y2_Value,
             self.label_Z1_Value,
             self.label_Z2_Value
        ]

        for TranslationLabelValue in self.TranslationLabelValues:
             TranslationLabelValue.setStyleSheet("color:red")
        
        self.label_CropTopLefCoefficientValue.setStyleSheet("color:red")
        self.label_CropBottomRightCoefficientValue.setStyleSheet("color:red")
        self.label_RorationScaleValue.setStyleSheet("color:red")
        self.label_RotationDegreeValue.setStyleSheet("color:red")

        self.menu_PythonProgramming = QMenu(parent=MainWindow)  
        self.menu_PythonProgramming.setObjectName("action_PythonProgramming")
        self.menu_PreRequisites.addMenu(self.menu_PythonProgramming)
        self.action_PythonProgramming = QtGui.QAction(parent=MainWindow)  
        self.action_PythonProgramming.setObjectName("action_PythonProgramming")
        self.menu_PythonProgramming.addAction(self.action_PythonProgramming)
        self.action_Numpy = QtGui.QAction(parent=MainWindow)  
        self.action_Numpy.setObjectName("action_Numpy")
        self.menu_PythonProgramming.addAction(self.action_Numpy)
        self.action_Pandas = QtGui.QAction(parent=MainWindow)  
        self.action_Pandas.setObjectName("action_Pandas")
        self.menu_PythonProgramming.addAction(self.action_Pandas)
        self.action_MatPlotLib = QtGui.QAction(parent=MainWindow)  
        self.action_MatPlotLib.setObjectName("action_MatPlotLib")
        self.menu_PythonProgramming.addAction(self.action_MatPlotLib)
        self.action_SeaBorn = QtGui.QAction(parent=MainWindow)  
        self.action_SeaBorn.setObjectName("action_SeaBorn")
        self.menu_PythonProgramming.addAction(self.action_SeaBorn)

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
        self.action_MLBigPicture = QtGui.QAction(parent=MainWindow)
        self.action_MLBigPicture.setObjectName("action_MLBigPicture")    
        self.action_CoreMachineLearningPrinciples.addAction(self.action_MLBigPicture)
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
        self.action_SupervisedMLProcess = QtGui.QAction(parent=MainWindow)  
        self.action_SupervisedMLProcess.setObjectName("action_SupervisedMLProcess")
        self.menu_Machine_Learning_Model_Fundamentals.addAction(self.action_SupervisedMLProcess)
        self.action_CodeSamplesByLearningParadigm = QtGui.QAction(parent=MainWindow)  
        self.action_CodeSamplesByLearningParadigm.setObjectName("action_CodeSamplesByLearningParadigm")
        self.menu_Machine_Learning_Model_Fundamentals.addAction(self.action_CodeSamplesByLearningParadigm)
        self.action_DeeperCodeSamplesWithDefinitions = QtGui.QAction(parent=MainWindow)  
        self.action_DeeperCodeSamplesWithDefinitions.setObjectName("action_DeeperCodeSamplesWithDefinitions")
        self.menu_Machine_Learning_Model_Fundamentals.addAction(self.action_DeeperCodeSamplesWithDefinitions)

        self.action_TheoreticalFoundationsOfComputerVision = QtGui.QAction(parent=MainWindow)  
        self.action_TheoreticalFoundationsOfComputerVision.setObjectName("action_TheoreticalFoundationsOfComputerVision")
        self.menu_FundamentalOfComputerVision.addAction(self.action_TheoreticalFoundationsOfComputerVision)
        self.action_PracticalFoundationsOfComputerVision = QMenu(parent=MainWindow)  
        self.action_PracticalFoundationsOfComputerVision.setObjectName("action_PracticalFoundationsOfComputerVision")
        self.menu_FundamentalOfComputerVision.addMenu(self.action_PracticalFoundationsOfComputerVision)
        self.action_ImagesAndColorsManipulationsAndOprations = QtGui.QAction(parent=MainWindow)  
        self.action_ImagesAndColorsManipulationsAndOprations.setObjectName("action_ImagesAndColorsManipulationsAndOprations")
        self.action_PracticalFoundationsOfComputerVision.addAction(self.action_ImagesAndColorsManipulationsAndOprations)

        self.pdf_view = CustomPdfView(self.pages)
        self.pdf_document = QPdfDocument(self.pdf_view)
        self.pages.addWidget(self.pdf_view)
      
        AboutAuthorDeveloper = self.load_html_file(os.path.relpath("pages/Text_AboutAuthorDeveloper.html"))
        self.textBrowser_AboutAuthorDeveloper.setHtml(AboutAuthorDeveloper)
        self.textBrowser_AboutAuthorDeveloper.setStyleSheet("padding:10px")
        AboutTool = self.load_html_file(os.path.relpath("pages/Text_AboutTool.html"))
        self.textBrowser_AboutTool.setHtml(AboutTool)
        self.textBrowser_AboutTool.setStyleSheet("padding:10px")
        self.textBrowser_AboutTool.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        #.setHorizontalScrollBarPolicy(Qt.scrol.ScrollBarAlwaysOff)
        self.pages.setCurrentWidget(self.page_AboutTool)
        
        self.label_ImageDepthValue.setStyleSheet("color:red")
        self.label_ImageShapeValue.setStyleSheet("color:red")
        self.label_ImageWidthValue.setStyleSheet("color:red")
        self.label_ImageHeightValue.setStyleSheet("color:red")
        #self.textBrowser_ImageAndColors.setStyleSheet("font-size:12px")
     #    self.webView = QWebEngineView(parent=None)
     #    self.webView.setObjectName("Python Programming")
     #    self.webView.setWindowTitle("Python Programming")
     #    self.webView.resize(1024, 768)
     #    self.webView.setMinimumSize(QtCore.QSize(1024, 768))
     #    self.webView.setBaseSize(QtCore.QSize(1024, 768))
     #    self.webView.setGeometry(QtCore.QRect(0, 0, 1024, 768))
     #    profile = QWebEngineProfile.defaultProfile() 
     #    webpage = QWebEnginePage(profile, self.webView)
     #    self.webView.setPage(webpage)
     #    settings = self.webView.page().settings()
     #    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
     #    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
     #    settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
     #    settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
     #    settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, True)
     #    self.webView.setContextMenuPolicy(PyQt6.QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
     #    self.webView.page().certificateError.connect(self.on_cert_error)
        self.CheckCreateDefaultFolders()
        self.connectActions()        
        self.LoadResources()
        self.FillImagesAndColorsCode()

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<End Block 4

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
