import sys
from PyQt5.uic import loadUi
#from PySide6.QtCore import QPoint
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtGui import *
from mainWindowInterface import *
import testCaptureUI

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.menuLabels.setHidden(True)

        self.show()

        # self.createNewWidgets(0, 0)
        # FOR loop
        # 10 rows
        for x in range(0,10):
            # columns
            for y in range(0,3):
                self.createStudentWidget(x, y)
        
        self.ui.takeAttendanceButton.clicked.connect(self.launchCapture)

        #Menu switching buttons
        self.ui.attendanceMenuIconButton.clicked.connect(self.switchToAttendancePage)
        self.ui.attendanceMenuLabelButton.clicked.connect(self.switchToAttendancePage)

        self.ui.manageClassesMenuIconButton.clicked.connect(self.switchToManageCoursesPage)
        self.ui.manageClassesMenuLabelButton.clicked.connect(self.switchToManageCoursesPage)

        self.ui.manageStudentsMenuIconButton.clicked.connect(self.switchToManageStudentsPage)
        self.ui.manageStudentsMenuLabelButton.clicked.connect(self.switchToManageStudentsPage)



    def switchToAttendancePage(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        

    def switchToManageStudentsPage(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def switchToManageCoursesPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def launchCapture(self):
        testCaptureUI.launch()


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

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())