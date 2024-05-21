import sys
from PyQt5.uic import loadUi
#from PySide6.QtCore import QPoint
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QAction, QMenu, QDesktopWidget
from PyQt5.QtGui import *
import numpy as np
from mainWindowInterface import *
import testCaptureUI
from AddDataToDatabase import FaceRecognitionFirebaseDB



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.db = FaceRecognitionFirebaseDB()   #-----> db here
        self.ui.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        self.show()

        # self.createNewWidgets(0, 0)
        # FOR loop
        # 10 rows
        for x in range(0,10):
            # columns
            for y in range(0,3):
                self.createStudentWidget(x, y)
                self.createCourseWidget(x, y)
        
        self.ui.takeAttendanceButton.clicked.connect(self.launchCapture)

        #Menu switching buttons
        # self.ui.attendanceMenuIconButton.clicked.connect(self.switchToAttendancePage)
        # self.ui.attendanceMenuLabelButton.clicked.connect(self.switchToAttendancePage)

        # self.ui.manageClassesMenuIconButton.clicked.connect(self.switchToManageCoursesPage)
        # self.ui.manageClassesMenuLabelButton.clicked.connect(self.switchToManageCoursesPage)

        # self.ui.manageStudentsMenuIconButton.clicked.connect(self.switchToManageStudentsPage)
        # self.ui.manageStudentsMenuLabelButton.clicked.connect(self.switchToManageStudentsPage)

        # Connect buttons to respective context menus
        self.ui.userDropMenuButton.clicked.connect(self.user_context_menu)

        #set default screen
        self.switchToManageCoursesPage()


    #Methods to show context menus
    def user_context_menu(self):

        self.show_custom_context_menu(self.ui.userDropMenuButton, ["Profile", "My Classes", "My Students", "Reports", "Sign Out", "Temp-Take Attendance"])


    def show_custom_context_menu(self, button, menu_items):
        menu = QMenu(self)

        #Set style sheet
        menu.setStyleSheet("""
                           
                           QMenu{
                           background-color: black;
                           color: white;
                           }
                           

                           QMenu:selected{
                           back-ground-color:white;
                           color: #12B298;
                           }
                           """)

        #Add actions to the menu
        for item_text in menu_items:
            action = QAction(item_text, self)
            action.triggered.connect(self.handle_menu_tem_click)
            menu.addAction(action)

        # Show the menu
        menu.move(button.mapToGlobal(button.rect().bottomLeft()))
        menu.exec()
    
    def handle_menu_tem_click(self):
        text = self.sender().text()
        match text:
            case "My Classes":
                self.switchToManageCoursesPage()
            case "Profile":
                self.switchToProfilePage()
            case "Reports":
                self.switchToReportsPage()
            case "Sign Out":
                sys.exit(0)
            case "My Students":
                self.switchToManageStudentsPage()
            case "Temp-Take Attendance":
                self.switchToAttendancePage()
            case _:
                pass


    def switchToAttendancePage(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        
    def switchToManageStudentsPage(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        # Must populate student tiles here
        # set flag so you don't need to repopulate everytime

    def switchToManageCoursesPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        # Must populate course tiles here
        # set flag so you don't need to repopulate everytime

    def switchToReportsPage(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def switchToProfilePage(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def launchCapture(self):
        testCaptureUI.launch()


    def createCourseWidget(self, rowNumber, columnNumber):
        
        # CREATE NEW UNIQUE NAMES FOR THE WIDGETS ---> dev check. REMOVE BEFORE DEPLOY
        newName = "frame" + str(rowNumber) + "_" + str(columnNumber)

        print(newName)

        # Course Card starts here
        self.courseCardWidget = QtWidgets.QWidget(self.ui.scrollAreaWidgetContents_2)
        self.courseCardWidget.setMaximumSize(QtCore.QSize(150, 150))
        self.courseCardWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.courseCardWidget.setObjectName("courseCardWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.courseCardWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_14 = QtWidgets.QWidget(self.courseCardWidget)
        self.widget_14.setMaximumSize(QtCore.QSize(150, 40))
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.widget_14)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.courseNameCardLabel = QtWidgets.QLabel(self.widget_14)
        self.courseNameCardLabel.setObjectName("courseNameCardLabel")
        self.horizontalLayout_13.addWidget(self.courseNameCardLabel)
        spacerItem9 = QtWidgets.QSpacerItem(59, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem9)
        self.verticalLayout_5.addWidget(self.widget_14)
        self.widget_4 = QtWidgets.QWidget(self.courseCardWidget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.courseCardSectionLabel = QtWidgets.QLabel(self.widget_4)
        self.courseCardSectionLabel.setObjectName("courseCardSectionLabel")
        self.horizontalLayout_17.addWidget(self.courseCardSectionLabel)
        spacerItem10 = QtWidgets.QSpacerItem(58, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem10)
        self.verticalLayout_5.addWidget(self.widget_4)
        self.widget_12 = QtWidgets.QWidget(self.courseCardWidget)
        self.widget_12.setMaximumSize(QtCore.QSize(150, 60))
        self.widget_12.setObjectName("widget_12")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_12)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.widget_13 = QtWidgets.QWidget(self.widget_12)
        self.widget_13.setObjectName("widget_13")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.widget_13)
        self.horizontalLayout_12.setContentsMargins(0, -1, 1, 0)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem11 = QtWidgets.QSpacerItem(98, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem11)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_13)
        self.pushButton_3.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/blackIcons/BlackIcons/edit-3.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/whiteIcons/whiteIcons/edit-3.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_3.setAutoExclusive(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_12.addWidget(self.pushButton_3)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_13)
        self.pushButton_5.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/blackIcons/BlackIcons/trash-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/whiteIcons/whiteIcons/trash-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_5.setIcon(icon2)
        self.pushButton_5.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_5.setAutoExclusive(True)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_12.addWidget(self.pushButton_5)
        self.horizontalLayout_9.addWidget(self.widget_13)
        self.verticalLayout_5.addWidget(self.widget_12)


        #retranslate functions
        _translate = QtCore.QCoreApplication.translate
        self.courseNameCardLabel.setText(_translate("MainWindow", "Course Name"))
        self.courseCardSectionLabel.setText(_translate("MainWindow", "Section Name"))
        
        
        # Create new attribute to Ui_Mainwindow
        # Syntax : setattr(obj, var, val)
        # Parameters :
        # obj : Object whose which attribute is to be assigned.
        # var : object attribute which has to be assigned.
        # val : value with which variable is to be assigned.
        setattr(self.ui, newName, self.courseCardWidget)
        
        self.ui.coursesGridLayout.addWidget(self.courseCardWidget, rowNumber, columnNumber, 1, 1)
        pass

    def createStudentWidget(self, rowNumber, columnNumber):

        # CREATE NEW UNIQUE NAMES FOR THE WIDGETS ---> dev check. REMOVE BEFORE DEPLOY
        newName = "frame" + str(rowNumber) + "_" + str(columnNumber)

        # print(newName)


        # Student ID frame starts here
        self.student1 = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        self.student1.setMinimumSize(QtCore.QSize(300, 100))
        self.student1.setMaximumSize(QtCore.QSize(500, 200))
        self.student1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
        "border-color: rgb(68, 8, 98);")
        self.student1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.student1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.student1.setObjectName("student1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.student1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.student1)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.student1)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 61, 16))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.frame_4)

        #Style Student ID Frame
        self.student1.setFrameShape(QFrame.StyledPanel)
        self.student1.setFrameShadow(QFrame.Raised)

        #retranslate functions
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "Name"))
        self.label_2.setText(_translate("MainWindow", "Student ID"))

        # Create new attribute to Ui_Mainwindow
        # Syntax : setattr(obj, var, val)
        # Parameters :
        # obj : Object whose which attribute is to be assigned.
        # var : object attribute which has to be assigned.
        # val : value with which variable is to be assigned.
        setattr(self.ui, newName, self.student1)


        # 
        # void QGridLayout::addLayout(QLayout *layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())
        # 
        self.ui.gridLayout.addWidget(self.student1, rowNumber, columnNumber, 1, 1)
  
        





if __name__ == "__main__":

    testDB = DB("testDB")
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())