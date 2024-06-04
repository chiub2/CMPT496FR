# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QTextEdit, QVBoxLayout, QWidget)
import backgoundImages_rc
import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 791)
        MainWindow.setMinimumSize(QSize(1200, 500))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.headerWidget = QWidget(self.widget)
        self.headerWidget.setObjectName(u"headerWidget")
        self.headerWidget.setMinimumSize(QSize(0, 80))
        self.headerWidget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(123, 3, 35);\n"
"\n"
"}\n"
"QPushButton{\n"
"	color:white;\n"
"	height:30px;\n"
"	text-align:center;\n"
"	border:none;\n"
"}\n"
"\n"
"\n"
"QLabel{\n"
"	color:white;\n"
"	text-align:center;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: #34111a;\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(self.headerWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(344, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label_7 = QLabel(self.headerWidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_2.addWidget(self.label_7)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_9 = QLabel(self.headerWidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_2.addWidget(self.label_9)

        self.label_8 = QLabel(self.headerWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(30, 30))
        self.label_8.setStyleSheet(u"text-align:centre;")
        self.label_8.setPixmap(QPixmap(u":/whiteIcons/whiteIcons/user.svg"))
        self.label_8.setScaledContents(False)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_8)

        self.userDropMenuButton = QPushButton(self.headerWidget)
        self.userDropMenuButton.setObjectName(u"userDropMenuButton")
        self.userDropMenuButton.setMinimumSize(QSize(35, 35))
        self.userDropMenuButton.setMaximumSize(QSize(35, 35))
        icon = QIcon()
        icon.addFile(u":/whiteIcons/whiteIcons/chevron-down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.userDropMenuButton.setIcon(icon)
        self.userDropMenuButton.setIconSize(QSize(20, 20))
        self.userDropMenuButton.setCheckable(True)
        self.userDropMenuButton.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.userDropMenuButton)


        self.verticalLayout.addWidget(self.headerWidget)

        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"")
        self.stackedWidget.setFrameShape(QFrame.NoFrame)
        self.stackedWidget.setLineWidth(0)
        self.attendancePage = QWidget()
        self.attendancePage.setObjectName(u"attendancePage")
        self.verticalLayout_2 = QVBoxLayout(self.attendancePage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.attendancePage)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"background-color:  rgb(255, 255, 255); ")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1180, 691))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QSize(0, 200))
        self.frame_2.setMaximumSize(QSize(16777215, 200))
        self.frame_2.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"	background-color: rgb(59,59,59);\n"
"	color: white;\n"
"	height:30px;\n"
"	text-align:left;\n"
"	border: none;\n"
"	padding-left:5px;\n"
"	padding-right:5px;\n"
"	border-bottom-left-radius:5px;\n"
"	border-top-left-radius:5px;\n"
"	border-bottom-right-radius:5px;\n"
"	border-top-right-radius:5px;\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color: rgb(52,17,26);\n"
"	color: white;\n"
"	font-weight:bold;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:  rgb(52,17,26);\n"
"	color: white;\n"
"	font-weight:bold;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.horizontalSpacer_3 = QSpacerItem(670, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.dateSelectorButton = QPushButton(self.frame)
        self.dateSelectorButton.setObjectName(u"dateSelectorButton")

        self.horizontalLayout_3.addWidget(self.dateSelectorButton)


        self.verticalLayout_6.addWidget(self.frame)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(478, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.takeAttendanceButton = QPushButton(self.frame_3)
        self.takeAttendanceButton.setObjectName(u"takeAttendanceButton")

        self.horizontalLayout_4.addWidget(self.takeAttendanceButton)


        self.verticalLayout_6.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.sortByButton = QPushButton(self.frame_4)
        self.sortByButton.setObjectName(u"sortByButton")

        self.horizontalLayout_5.addWidget(self.sortByButton)

        self.horizontalSpacer_5 = QSpacerItem(795, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_6.addWidget(self.frame_4)


        self.verticalLayout_3.addWidget(self.frame_2)

        self.widget_5 = QWidget(self.scrollAreaWidgetContents)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.horizontalLayout_6.addLayout(self.gridLayout)


        self.verticalLayout_3.addWidget(self.widget_5)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.attendancePage)
        self.manageStudentsPage = QWidget()
        self.manageStudentsPage.setObjectName(u"manageStudentsPage")
        self.verticalLayout_9 = QVBoxLayout(self.manageStudentsPage)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.widget_2 = QWidget(self.manageStudentsPage)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_7 = QVBoxLayout(self.widget_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_16 = QWidget(self.widget_2)
        self.widget_16.setObjectName(u"widget_16")
        self.verticalLayout_20 = QVBoxLayout(self.widget_16)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.widget_17 = QWidget(self.widget_16)
        self.widget_17.setObjectName(u"widget_17")
        self.horizontalLayout_16 = QHBoxLayout(self.widget_17)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_15 = QLabel(self.widget_17)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_16.addWidget(self.label_15)

        self.horizontalSpacer_6 = QSpacerItem(1051, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_6)

        self.addStudentButton_3 = QPushButton(self.widget_17)
        self.addStudentButton_3.setObjectName(u"addStudentButton_3")
        self.addStudentButton_3.setMaximumSize(QSize(100, 100))
        icon1 = QIcon()
        icon1.addFile(u":/blackIcons/BlackIcons/plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addStudentButton_3.setIcon(icon1)
        self.addStudentButton_3.setIconSize(QSize(70, 70))

        self.horizontalLayout_16.addWidget(self.addStudentButton_3)


        self.verticalLayout_20.addWidget(self.widget_17)

        self.widget_18 = QWidget(self.widget_16)
        self.widget_18.setObjectName(u"widget_18")
        self.widget_18.setStyleSheet(u"QLineEdit{\n"
"	padding-left:10px;\n"
"	border: 2px solid gray;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"")
        self.horizontalLayout_17 = QHBoxLayout(self.widget_18)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.lineEdit_3 = QLineEdit(self.widget_18)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_17.addWidget(self.lineEdit_3)

        self.studentSearchButton = QPushButton(self.widget_18)
        self.studentSearchButton.setObjectName(u"studentSearchButton")

        self.horizontalLayout_17.addWidget(self.studentSearchButton)

        self.horizontalSpacer_14 = QSpacerItem(818, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_14)

        self.refreshbutton = QPushButton(self.widget_18)
        self.refreshbutton.setObjectName(u"refreshbutton")

        self.horizontalLayout_17.addWidget(self.refreshbutton)


        self.verticalLayout_20.addWidget(self.widget_18)


        self.verticalLayout_7.addWidget(self.widget_16)

        self.widget_15 = QWidget(self.widget_2)
        self.widget_15.setObjectName(u"widget_15")
        self.gridLayout_2 = QGridLayout(self.widget_15)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea_4 = QScrollArea(self.widget_15)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 1144, 488))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.studentsViewGridLayout = QGridLayout()
        self.studentsViewGridLayout.setObjectName(u"studentsViewGridLayout")

        self.gridLayout_3.addLayout(self.studentsViewGridLayout, 0, 0, 1, 1)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_5)

        self.gridLayout_2.addWidget(self.scrollArea_4, 0, 0, 1, 1)


        self.verticalLayout_7.addWidget(self.widget_15)


        self.verticalLayout_9.addWidget(self.widget_2)

        self.stackedWidget.addWidget(self.manageStudentsPage)
        self.manageClassesPage = QWidget()
        self.manageClassesPage.setObjectName(u"manageClassesPage")
        self.verticalLayout_10 = QVBoxLayout(self.manageClassesPage)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.widget_3 = QWidget(self.manageClassesPage)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_8 = QVBoxLayout(self.widget_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame_6 = QFrame(self.widget_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(16777215, 120))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_6)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.widget_8 = QWidget(self.frame_6)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_7 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.widget_8)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.horizontalSpacer_8 = QSpacerItem(578, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)


        self.verticalLayout_11.addWidget(self.widget_8)

        self.widget_7 = QWidget(self.frame_6)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMaximumSize(QSize(16777215, 50))
        self.widget_7.setStyleSheet(u"QLineEdit{\n"
"	padding-left:10px;\n"
"	border: 2px solid gray;\n"
"	border-radius: 10px;\n"
"}")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.lineEdit = QLineEdit(self.widget_7)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"")

        self.horizontalLayout_10.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.widget_7)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_10.addWidget(self.pushButton)

        self.horizontalSpacer_7 = QSpacerItem(398, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_7)

        self.addCourseButton = QPushButton(self.widget_7)
        self.addCourseButton.setObjectName(u"addCourseButton")
        self.addCourseButton.setMaximumSize(QSize(16777215, 100))
        self.addCourseButton.setIcon(icon1)
        self.addCourseButton.setIconSize(QSize(30, 30))
        self.addCourseButton.setAutoExclusive(True)

        self.horizontalLayout_10.addWidget(self.addCourseButton)


        self.verticalLayout_11.addWidget(self.widget_7)


        self.verticalLayout_8.addWidget(self.frame_6)

        self.widget_51 = QWidget(self.widget_3)
        self.widget_51.setObjectName(u"widget_51")
        self.verticalLayout_4 = QVBoxLayout(self.widget_51)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_6 = QWidget(self.widget_51)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_8 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label = QLabel(self.widget_6)
        self.label.setObjectName(u"label")

        self.horizontalLayout_8.addWidget(self.label)

        self.horizontalSpacer_9 = QSpacerItem(1072, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_9)


        self.verticalLayout_4.addWidget(self.widget_6)

        self.scrollArea_2 = QScrollArea(self.widget_51)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setStyleSheet(u"\n"
"QPushButton{\n"
"	height:30px;\n"
"	text-align:center;\n"
"	border:none;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover{\n"
"	background-color: #ffffff;\n"
"}")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1144, 491))
        self.horizontalLayout_11 = QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.coursesGridLayout = QGridLayout()
        self.coursesGridLayout.setSpacing(10)
        self.coursesGridLayout.setObjectName(u"coursesGridLayout")
        self.coursesGridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.addCourseButtonWidget = QWidget(self.scrollAreaWidgetContents_2)
        self.addCourseButtonWidget.setObjectName(u"addCourseButtonWidget")
        self.addCourseButtonWidget.setMaximumSize(QSize(150, 120))
        self.verticalLayout_13 = QVBoxLayout(self.addCourseButtonWidget)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")

        self.coursesGridLayout.addWidget(self.addCourseButtonWidget, 0, 0, 1, 1)


        self.horizontalLayout_11.addLayout(self.coursesGridLayout)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_4.addWidget(self.scrollArea_2)


        self.verticalLayout_8.addWidget(self.widget_51)


        self.verticalLayout_10.addWidget(self.widget_3)

        self.stackedWidget.addWidget(self.manageClassesPage)
        self.reportsPage = QWidget()
        self.reportsPage.setObjectName(u"reportsPage")
        self.verticalLayout_16 = QVBoxLayout(self.reportsPage)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.widget_4 = QWidget(self.reportsPage)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_17 = QVBoxLayout(self.widget_4)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_17.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 653, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer)


        self.verticalLayout_16.addWidget(self.widget_4)

        self.stackedWidget.addWidget(self.reportsPage)
        self.profilePage = QWidget()
        self.profilePage.setObjectName(u"profilePage")
        self.horizontalLayout_15 = QHBoxLayout(self.profilePage)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.widget_13 = QWidget(self.profilePage)
        self.widget_13.setObjectName(u"widget_13")
        self.verticalLayout_18 = QVBoxLayout(self.widget_13)
        self.verticalLayout_18.setSpacing(10)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.label_10 = QLabel(self.widget_13)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_18.addWidget(self.label_10)

        self.label_11 = QLabel(self.widget_13)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_18.addWidget(self.label_11)

        self.label_12 = QLabel(self.widget_13)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_18.addWidget(self.label_12)

        self.label_13 = QLabel(self.widget_13)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_18.addWidget(self.label_13)

        self.label_14 = QLabel(self.widget_13)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_18.addWidget(self.label_14)

        self.verticalSpacer_2 = QSpacerItem(20, 557, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_2)


        self.horizontalLayout_15.addWidget(self.widget_13)

        self.widget_14 = QWidget(self.profilePage)
        self.widget_14.setObjectName(u"widget_14")
        self.verticalLayout_19 = QVBoxLayout(self.widget_14)
        self.verticalLayout_19.setSpacing(8)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.textEdit = QTextEdit(self.widget_14)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(100, 15))

        self.verticalLayout_19.addWidget(self.textEdit)

        self.textEdit_2 = QTextEdit(self.widget_14)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setMaximumSize(QSize(100, 15))

        self.verticalLayout_19.addWidget(self.textEdit_2)

        self.textEdit_3 = QTextEdit(self.widget_14)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setMaximumSize(QSize(100, 15))

        self.verticalLayout_19.addWidget(self.textEdit_3)

        self.textEdit_4 = QTextEdit(self.widget_14)
        self.textEdit_4.setObjectName(u"textEdit_4")
        self.textEdit_4.setMaximumSize(QSize(100, 15))

        self.verticalLayout_19.addWidget(self.textEdit_4)

        self.textEdit_5 = QTextEdit(self.widget_14)
        self.textEdit_5.setObjectName(u"textEdit_5")
        self.textEdit_5.setMaximumSize(QSize(100, 15))

        self.verticalLayout_19.addWidget(self.textEdit_5)

        self.verticalSpacer_3 = QSpacerItem(20, 557, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_3)


        self.horizontalLayout_15.addWidget(self.widget_14)

        self.stackedWidget.addWidget(self.profilePage)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"App Name", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Welcome Back, User", None))
        self.label_8.setText("")
        self.userDropMenuButton.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Attendance", None))
        self.dateSelectorButton.setText(QCoreApplication.translate("MainWindow", u"Date Selector", None))
        self.takeAttendanceButton.setText(QCoreApplication.translate("MainWindow", u"Take Attendance", None))
        self.sortByButton.setText(QCoreApplication.translate("MainWindow", u"Sort by:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Your Students", None))
        self.addStudentButton_3.setText("")
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Find Student ...", None))
        self.studentSearchButton.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.refreshbutton.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Find Course ...", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.addCourseButton.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Your Classes:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Reports", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"User Name", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"DOB", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Department Name", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Email", None))
    # retranslateUi

