import logging
import sys
from tkinter import messagebox
from PyQt5.uic import loadUi
#from PySide6.QtCore import QPoint
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QAction, QMenu, QDesktopWidget, QMessageBox
from PyQt5.QtGui import *
import numpy as np
from AddStudentDialog import AddStudentDialog
from AddCourseDialog import AddCourseDialog
from mainWindowInterface import *
import testCaptureUI
from AddDataToDatabase import FaceRecognitionFirebaseDB




class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.db = FaceRecognitionFirebaseDB()   #-----> db here
        self.ui.setupUi(self)


        #Change default Font
        QFontDatabase.addApplicationFont("UI/Font/Kamerik105Cyrillic-Bold.ttf")
        custom_font = QFont("Kamerik105Cyrillic-Bold")
        # custom_font.setWeight(18)
        QApplication.setFont(custom_font, "QLabel")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Create initial student widgets
        self.refresh_student_data()

        self.show()

        # # self.createNewWidgets(0, 0)
        # # FOR loop
        # # 10 rows
        # for x in range(0,10):
        #     # columns
        #     for y in range(0,3):
        #         self.createStudentWidget(x, y)

        
        # Search for students
        self.ui.studentSearchButton.clicked.connect(self.search_student)

        # Adding students to DataBase
        self.ui.addStudentButton_3.clicked.connect(self.show_add_student_dialog)

        

        # Refreshing student data
        self.ui.refreshbutton.clicked.connect(self.refresh_student_data)
        self.refresh_student_data()

        self.ui.takeAttendanceButton.clicked.connect(self.launchCapture)

        # Adding Course to DataBase
        self.ui.addCourseButton.clicked.connect(self.show_add_course_dialog)


        self.show()

        

        
        
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


#===================================================Adding Courses to Database
    def show_add_course_dialog(self):
        dialog = AddCourseDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            course_data = dialog.get_course_data()
            self.add_course_to_db(course_data)
    
    def add_course_to_db(self, course_data):
        course_data["students"] = [0]   #-----> student 0 doesn't exist
        course_name = course_data["course_name"]
        section_id = course_data["section_id"]
        course_dict = {f"{course_name}-{section_id}": course_data}
        print(course_dict)
        self.db.addCourse(course_dict)
        QMessageBox.information(self, "Success", "Course added successfully!")
        self.refresh_course_data()

    def refresh_course_data(self):
        try:
            print(20000)
            for i in reversed(range(self.ui.coursesGridLayout.count())):
                widget = self.ui.coursesGridLayout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            courses = self.db.getAllCourses()
            print(courses)
            row = 0
            col = 0
            for course_name_sec_id, course_info in courses.items():
                self.createCourseWidget(row, col, course_info)
                col += 1
                if col == 3:
                    col = 0
                    row += 1
        except Exception as e:
            print(f"Error during refresh: {e}")



#===================================================Adding students to Database

    def search_student(self):
        try:
            search_text = self.ui.lineEdit_3.text().lower()
            all_students = self.db.getAllStudents()
            filtered_students = {sid: data for sid, data in all_students.items() if search_text in data.get("full_name", "").lower() or search_text in sid.lower()}
            self.populate_student_grid(filtered_students)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during search: {str(e)}")

    def populate_student_grid(self, students=None):
        if students is None:
            students = self.db.getAllStudents()

        for i in reversed(range(self.ui.gridLayout_3.count())):
            widget = self.ui.gridLayout_3.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        row = 0
        col = 0
        for student_id, student_info in students.items():
            self.createStudentWidget(row, col, student_info)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def show_add_student_dialog(self):
        dialog = AddStudentDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            student_data = dialog.get_student_data()
            self.add_student_to_db(student_data)



    def add_student_to_db(self, student_data):
        student_id = student_data["student_id"]
        student_dict = {student_id: student_data}
        self.db.addStudent(student_dict)
        QMessageBox.information(self, "Success", "Student added successfully!")
        self.refresh_student_data()

    def refresh_student_data(self):
        try:
            for i in reversed(range(self.ui.gridLayout_3.count())):
                widget = self.ui.gridLayout_3.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            students = self.db.getAllStudents()
            row = 0
            col = 0
            print(students)
            '''
            Some extremely weird behaviour going on here, if database is empty and user adds a student,
            students will be of instance list, but if database is not empty and user adds or edits a student,
            database will be of type dictionary


            ---> temp fix, check for instance of students and execute approprriate algorithm
            '''
            if isinstance(students, list):
                if students != None:
                    for student in students:
                        if student != None:
                            self.createStudentWidget(row, col, student)
                            col += 1
                            if col == 3:
                                col = 0
                                row += 1
            elif isinstance(students, dict):
                for student_id, student_info in students.items():
                    self.createStudentWidget(row, col, student_info)
                    col += 1
                    if col == 3:
                        col = 0
                        row += 1
        except Exception as e:
            print(f"Error during refresh: {e}")

    def edit_student(self, student_id):
        try:
            student_data = self.db.getStudent(student_id)
            oldID = student_data["student_id"]
            dialog = AddStudentDialog(student_data)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                updated_data = dialog.get_student_data()
                self.db.updateStudent(student_id, oldID, updated_data)
                self.refresh_student_data()
        except Exception as e:
            print(f"Error during edit: {e}")

    def delete_student(self, student_id):
        try:
            reply = QMessageBox.question(self, 'Delete Student', f"Are you sure you want to delete the student with ID {student_id}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                print(f"Attempting to delete student with ID: {student_id}")
                logging.debug(f"Attempting to delete student with ID: {student_id}")
                self.db.deleteStudent(student_id)
                self.refresh_student_data()
                print(f"Student with ID {student_id} deleted successfully.")
        except Exception as e:
            print(f"Error during delete: {e}")
            logging.error(f"Error during delete: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while deleting the student: {str(e)}")



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
            action.triggered.connect(self.handle_menu_item_click)
            menu.addAction(action)

        # Show the menu
        menu.move(button.mapToGlobal(button.rect().bottomLeft()))
        menu.exec()
    
    def handle_menu_item_click(self):
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


    def createCourseWidget(self, rowNumber, columnNumber, course_info = None):
        
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
        if course_info == None:
            self.courseNameCardLabel.setText(_translate("MainWindow", "Course Name"))
            self.courseCardSectionLabel.setText(_translate("MainWindow", "Section Name"))
        else:
            self.courseNameCardLabel.setText(_translate("MainWindow", course_info["course_name"]))
            self.courseCardSectionLabel.setText(_translate("MainWindow", course_info["section_id"]))
            
        
        
        
        # Create new attribute to Ui_Mainwindow
        # Syntax : setattr(obj, var, val)
        # Parameters :
        # obj : Object whose which attribute is to be assigned.
        # var : object attribute which has to be assigned.
        # val : value with which variable is to be assigned.
        setattr(self.ui, newName, self.courseCardWidget)
        
        self.ui.coursesGridLayout.addWidget(self.courseCardWidget, rowNumber, columnNumber, 1, 1)
        

    def createStudentWidget(self, rowNumber, columnNumber, student_info=None):
        newName = "studentFrame" + str(rowNumber) + "_" + str(columnNumber)

        self.studentCardWidget = QtWidgets.QWidget(self.ui.scrollAreaWidgetContents_5)
        self.studentCardWidget.setMaximumSize(QtCore.QSize(150, 150))
        self.studentCardWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.studentCardWidget.setObjectName("student" + student_info["student_id"] + "CardWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.studentCardWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_14 = QtWidgets.QWidget(self.studentCardWidget)
        self.widget_14.setMaximumSize(QtCore.QSize(150, 40))
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.widget_14)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.studentNameCardLabel = QtWidgets.QLabel(self.widget_14)
        self.studentNameCardLabel.setObjectName("student" + student_info["student_id"] + "CardLabel")
        self.horizontalLayout_13.addWidget(self.studentNameCardLabel)
        spacerItem9 = QtWidgets.QSpacerItem(59, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem9)
        self.verticalLayout_5.addWidget(self.widget_14)
        self.widget_4 = QtWidgets.QWidget(self.studentCardWidget)
        self.widget_4.setObjectName(str(student_info["student_id"]) + "StudentWidget")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.studentCardIDLabel = QtWidgets.QLabel(self.widget_4)
        self.studentCardIDLabel.setObjectName( "student" + student_info["student_id"] + "CardIDLabel")
        self.horizontalLayout_17.addWidget(self.studentCardIDLabel)
        spacerItem10 = QtWidgets.QSpacerItem(58, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem10)
        self.verticalLayout_5.addWidget(self.widget_4)
        self.widget_12 = QtWidgets.QWidget(self.studentCardWidget)
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
        icon1 = QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/blackIcons/BlackIcons/edit-3.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/whiteIcons/whiteIcons/edit-3.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_3.setAutoExclusive(True)
        self.pushButton_3.setObjectName("edit" + student_info["student_id"] + "Button")
        self.pushButton_3.clicked.connect(lambda: self.edit_student(student_info["student_id"]))
        self.horizontalLayout_12.addWidget(self.pushButton_3)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_13)
        self.pushButton_5.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/blackIcons/BlackIcons/trash-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/whiteIcons/whiteIcons/trash-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_5.setIcon(icon2)
        self.pushButton_5.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_5.setAutoExclusive(True)
        self.pushButton_5.setObjectName("delete" + student_info["student_id"] + "Button")
        self.pushButton_5.clicked.connect(lambda: self.delete_student(student_info["student_id"]))
        self.horizontalLayout_12.addWidget(self.pushButton_5)
        self.horizontalLayout_9.addWidget(self.widget_13)
        self.verticalLayout_5.addWidget(self.widget_12)

        if student_info:
            _translate = QtCore.QCoreApplication.translate
            self.studentNameCardLabel.setText(_translate("MainWindow", student_info.get("full_name", "Name")))
            self.studentCardIDLabel.setText(_translate("MainWindow", student_info.get("student_id", "Student ID")))

        setattr(self.ui, newName, self.studentCardWidget)
        self.ui.gridLayout_3.addWidget(self.studentCardWidget, rowNumber, columnNumber, 1, 1)
        print(f"Added student widget at ({rowNumber}, {columnNumber})")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())