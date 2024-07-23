import logging
import os
import sys
import time
from tkinter import messagebox
from PyQt5.uic import loadUi
# from PySide6.QtCore import QPoint
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage, QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import QPoint
import numpy as np
from AddStudentDialog import *
from AddCourseDialog import *
from mainWindowInterface import *
import testCaptureUI
from FireBaseDB import FaceRecognitionFirebaseDB
import cv2
import threading
from PyQt5.QtGui import QImage, QPixmap
from mainWindowInterface import Ui_MainWindow
from datetime import datetime
import pickle
from tkinter import messagebox
from firebase_admin import storage
import testCaptureUI
from studentManagementWindow import *
from dateSelectorHandler import CalendarDialog
import face_recognition
from Encoder import EncoderDB
import urllib.request
import io
from PyQt5.QtGui import QPixmap, QImage
from login import LoginForm  # Import the login form
from login_ui import Ui_LoginForm  # Adjust the import according to your project structure
from PyQt5.QtCore import pyqtSignal
import qasync
import asyncio
import threading


# class MainWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.db = FaceRecognitionFirebaseDB()   #-----> db here
#         self.ui.setupUi(self)
#         self.video_thread = None

#         self.current_course_info = None  # Add this line to maintain the current course context
#         self.camera_running = False  # Add this flag

#         # effect = QGraphicsDropShadowEffect(
#         # offset = QPoint(3, 3), blurRadius=25, color=QColor("#111")
#         # )
#         # self.ui.headerWidget.setGraphicsEffect(effect)
        


#         #Change default Font
#         QFontDatabase.addApplicationFont("UI/Font/Kamerik105Cyrillic-Bold.ttf")
#         custom_font = QFont("Kamerik105Cyrillic-Bold")
#         # custom_font.setWeight(18)
#         QApplication.setFont(custom_font, "QLabel")
#         # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#         # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


#         # Load face encodings

        
#         # Search for students
#         self.ui.studentSearchButton.clicked.connect(self.search_student)

#         # Adding students to DataBase
#         self.ui.addStudentButton_3.clicked.connect(self.show_add_student_dialog)
        
#         self.ui.takeAttendanceButton.clicked.connect(self.launch_capture)


#         # Connection student refresh button data
#         self.ui.refreshbutton.clicked.connect(lambda: self.refresh_student_data(self.ui.studentsViewGridLayout))

#         self.ui.searchCoursesButton.clicked.connect(self.search_courses)
        

        


#         # Adding Course to DataBase
#         self.ui.addCourseButton.clicked.connect(self.show_add_course_dialog)
#         self.ui.refreshCoursesButton.clicked.connect(self.refresh_course_data)
        
#         self.switchToManageCoursesPage()


#         #refreshing data
#         self.refresh_student_data(self.ui.studentsViewGridLayout)
#         self.refresh_course_data()



#         # Camera control buttons
#         # self.ui.camera_on_button.clicked.connect(self.start_camera)
#         # self.ui.camera_off_button.clicked.connect(self.stop_camera)

#         self.refresh_student_data(self.ui.studentsViewGridLayout)
#         self.refresh_course_data()


#         self.show()

#         # Initialize Firebase Database
#         self.face_recognition_db = FaceRecognitionFirebaseDB()
#         self.encoder_db = EncoderDB()
       

#         # self.ui.dateSelectorButton.clicked.connect(self.pickDate)
#         self.ui.manageStudentsAttendanceButton.clicked.connect(self.manageStudentsinClass)


#         #Menu switching buttons
#         # self.ui.attendanceMenuIconButton.clicked.connect(self.switchToAttendancePage)
#         # self.ui.attendanceMenuLabelButton.clicked.connect(self.switchToAttendancePage)

#         # self.ui.manageClassesMenuIconButton.clicked.connect(self.switchToManageCoursesPage)
#         # self.ui.manageClassesMenuLabelButton.clicked.connect(self.switchToManageCoursesPage)

#         # self.ui.manageStudentsMenuIconButton.clicked.connect(self.switchToManageStudentsPage)
#         # self.ui.manageStudentsMenuLabelButton.clicked.connect(self.switchToManageStudentsPage)

#         # Connect buttons to respective context menus
#         self.ui.userDropMenuButton.clicked.connect(self.user_context_menu)
#         self.ui.dateSelectorButton.clicked.connect(self.pickDate)

#         #set default screen
#         self.switchToManageCoursesPage()


from generateTeacherEncoding import generate_teacher_encodings
from Encoder import EncoderDB
from Encoder import EncoderDB, read_images_from_firebase, findEncodings, main as run_encoder
generate_teacher_encodings()
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.login_form = LoginForm()
        # self.login_form.show()
        # self.login_form.login_successful.connect(self.show_main_window)
        self.face_detection_thread = None
        self.show_main_window()

    def show_main_window(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = FaceRecognitionFirebaseDB()   #-----> db here
        self.video_thread = None
        self.current_course_info = None  # Add this line to maintain the current course context
        self.camera_running = False  # Add this flag

        self.setup_ui_connections()
        self.refresh_data()

        self.show()

        # Initialize Firebase Database
        self.face_recognition_db = FaceRecognitionFirebaseDB()
        self.encoder_db = EncoderDB()

    def setup_ui_connections(self):
        # Change default Font
        QFontDatabase.addApplicationFont("UI/Font/Kamerik105Cyrillic-Bold.ttf")
        custom_font = QFont("Kamerik105Cyrillic-Bold")
        QApplication.setFont(custom_font, "QLabel")

        # Search for students
        self.ui.studentSearchButton.clicked.connect(self.search_student)

        # Adding students to DataBase
        self.ui.addStudentButton_3.clicked.connect(self.show_add_student_dialog)
        
        self.ui.takeAttendanceButton.clicked.connect(self.launch_capture)

        # Connection student refresh button data
        self.ui.refreshbutton.clicked.connect(lambda: self.refresh_student_data(self.ui.studentsViewGridLayout))

        self.ui.searchCoursesButton.clicked.connect(self.search_courses)

        # Adding Course to DataBase
        self.ui.addCourseButton.clicked.connect(self.show_add_course_dialog)
        self.ui.refreshCoursesButton.clicked.connect(self.refresh_course_data)

        self.ui.userDropMenuButton.clicked.connect(self.user_context_menu)
        self.ui.dateSelectorButton.clicked.connect(self.pickDate)

        self.ui.manageStudentsAttendanceButton.clicked.connect(self.manageStudentsinClass)

        self.switchToManageCoursesPage()

    def refresh_data(self):
        attendance_status = self.get_attendance_status()
        self.refresh_student_data(self.ui.studentsViewGridLayout, attendance_status)
        self.refresh_course_data()


#==============================Date picker actions


    def get_current_day(self):
        """Returns the current day of the week in lowercase (e.g., 'monday')"""
        return datetime.now().strftime('%A').lower()

    def normalize_day(self, day):
        """Normalizes common day abbreviations and formats to lowercase full day names"""
        day = day.strip().lower()
        day_mapping = {
            "mon": "monday",
            "tue": "tuesday",
            "tues": "tuesday",
            "wed": "wednesday",
            "thu": "thursday",
            "thur": "thursday",
            "fri": "friday",
            "sat": "saturday",
            "sun": "sunday"
        }
        return day_mapping.get(day, day)

    def is_meeting_day(self, meeting_days):
        """Checks if today is one of the meeting days"""
        current_day = self.get_current_day()
        normalized_meeting_days = [self.normalize_day(day) for day in meeting_days]
        return current_day in normalized_meeting_days
    

    def clear_current_course_info_ui(self):
        # Clear any UI elements related to the current course info
        self.ui.attendancePage_classNameLabel.setText("Attendance: None")

    def pickDate(self):
        self.pickDatesDialog = CalendarDialog()
        if self.pickDatesDialog.exec_() == QDialog.Accepted:
            print("dialog ended")
        else:  
            ''' 
            Date Format:    DAYofWeek MONTH DD YYYY
                        E.g: Tue Jul 16 2024                 
            '''
            self.attendanceDate = self.pickDatesDialog.returnDate()
            print("Calendar Dialog ended")
            print("Selected Date: ", self.attendanceDate)


        return
    
    
    # def pickDate(self):
    #     self.pickDatesDialog = CalendarDialog()
    #     self.pickDatesDialog.dateSelected.connect(self.setAttendanceDate)
    #     self.pickDatesDialog.exec_()

    # def setAttendanceDate(self, date):
    #     self.attendanceDate = date
    #     print("Selected Date: ", self.attendanceDate)
#==============================Manage students in class
    def manageStudentsinClass(self):
        if self.current_course_info:
            self.manageStudents = StudentManagementApp(self.current_course_info, self.db)
            if self.manageStudents.exec_() == QtWidgets.QDialog.Accepted:
                pass
            attendance_status = self.get_attendance_status()
            self.displayEnrolledStudents(self.ui.studentsAttendanceGrid, self.getEnrolledStudents(), attendance_status, show_attendance_icons=True)
        else:
            QMessageBox.warning(self, "No Course Selected", "Please select a course before managing students.")





        
    def getEnrolledStudents(self):
        if self.current_course_info is None:
            logging.error("Current course info is not set.")
            return {}

        course_name = self.current_course_info["course_name"]
        section_id = self.current_course_info["section_id"]
        
        # Add debug logging to verify correct retrieval
        logging.debug(f"Fetching enrolled students for course: {course_name}, section: {section_id}")
        
        enrolledStudentsIDs = self.db.getEnrolledStudents(course_name, section_id)
        logging.debug(f"Enrolled Students IDs: {enrolledStudentsIDs}")
        
        retDict = self.db.getStudentinfofromList(enrolledStudentsIDs)
        logging.debug(f"Enrolled Students Info: {retDict}")
        return retDict

    

    def displayEnrolledStudents(self, container, students, attendance_status, show_attendance_icons=False):
        for i in reversed(range(container.count())):
            widget = container.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.populate_student_grid(container, False, students, show_attendance_icons=show_attendance_icons, attendance_status=attendance_status)






    def get_attendance_status(self):
        """Fetches and returns the current attendance status from the database."""
        if self.current_course_info is None:
            return {}

        course_name = self.current_course_info["course_name"]
        section_id = self.current_course_info["section_id"]
        today_date = datetime.now().strftime('%Y-%m-%d')
        
        attendance_status = self.db.getAttendanceStatus(course_name, section_id, today_date)
        return attendance_status



#===================================================Camera Control
   
    def start_camera(self):
        logging.debug("Starting camera")
        self.video_thread = threading.Thread(target=testCaptureUI.launch, args=(self.ui.camera_interface, self.face_recognition_db, self.current_course_info["course_name"], self.current_course_info["section_id"]))
        self.video_thread.start()
        self.camera_running = True

    def stop_camera(self):
        logging.debug("Stopping camera")
        if self.face_detection_thread:
            testCaptureUI.stop(self.face_detection_thread)  # Pass the thread here
            self.face_detection_thread = None
        self.clear_camera_interface()
        self.camera_running = False

    def clear_camera_interface(self):
        self.ui.camera_interface.clear()
        black_image = QImage(640, 480, QImage.Format_RGB888)
        black_image.fill(QtCore.Qt.black)
        pixmap = QPixmap.fromImage(black_image)
        self.ui.camera_interface.setPixmap(pixmap)
        logging.debug("Camera interface cleared")


#===================================================Adding Courses to Database
    def show_add_course_dialog(self):
        dialog = AddCourseDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            course_data = dialog.get_course_data()
            self.add_course_to_db(course_data)
    
    def add_course_to_db(self, course_data):
        course_data["students"] = [0]   #-----> student 0 doesn't exist //needed so student list is not empty
        course_name = course_data["course_name"]
        section_id = course_data["section_id"]
        course_dict = {f"{course_name}-{section_id}": course_data}
        print(course_dict)
        self.db.addCourse(course_dict)
        QMessageBox.information(self, "Success", "Course added successfully!")
        self.refresh_course_data()

    def refresh_course_data(self):
        if self.camera_running:
            self.stop_camera()
        self.current_course_info = None
        for i in reversed(range(self.ui.coursesGridLayout.count())):
            widget = self.ui.coursesGridLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        courses = self.db.getAllCourses()
        row = 0
        col = 0
        print(courses)
        if isinstance(courses, list):
            if courses != None:
                for course in courses:
                    if course != None:
                        self.createCourseWidget2(row, col, course)
                        col += 1
                        if col == 3:
                            col = 0
                            row += 1
        elif isinstance(courses, dict):
            for course_name, course_info in courses.items():
                self.createCourseWidget2(row, col, course_info)
                col += 1
                if col == 3:
                    col = 0
                    row += 1
        elif courses == None:
            return
        
    def edit_course(self, course_name, section_id):
        try:
            course_data = self.db.getCourse(course_name, section_id)
            old_course_name = course_data["course_name"]
            old_section_id = course_data["section_id"]
            dialog = AddCourseDialog(course_data)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                updated_data = dialog.get_course_data()
                self.db.updateCourseData(updated_data["course_name"],updated_data["section_id"], old_course_name, old_section_id, updated_data)
                self.refresh_course_data()
        except Exception as e:
            print(f"Error during edit: {e}")

    def delete_course(self, course_name, section_id):
        try:
            reply = QMessageBox.question(self, 'Delete Student', f"Are you sure you want to delete the course with ID: {course_name}-{section_id}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                print(f"Attempting to delete course with ID: {course_name}-{section_id}")
                logging.debug(f"Attempting to delete course with ID: {course_name}-{section_id}")
                self.db.deleteCourse(course_name, section_id)
                self.refresh_course_data()
                print(f"Course with ID {course_name}-{section_id} deleted successfully.")
        except Exception as e:
            print(f"Error during delete: {e}")
            logging.error(f"Error during delete: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while deleting the Course: {str(e)}")


#====================================searching for courses
            
    def search_courses(self):
        try:
            search_text = self.ui.lineEdit.text().lower()
            allcourses = self.db.getAllCourses()
            filtered_courses = {course_id: data for course_id, data in allcourses.items() if search_text in data.get("course_name", "").lower() or search_text in course_id.lower()}
            self.populate_courses_grid(filtered_courses)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during search: {str(e)}")

    def populate_courses_grid(self, courses=None):
        if courses is None:
            courses = self.face_recognition_db.getAllCourses()

        for i in reversed(range(self.ui.coursesGridLayout.count())):
            widget = self.ui.coursesGridLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        row = 0
        col = 0
        for course_info in courses.values():
            if course_info is not None:
                self.createCourseWidget2(row, col, course_info)
                col += 1
                if col == 3:
                    col = 0
                    row += 1
            else:
                logging.warning(f"Course info is None, skipping...")


#===================================================Adding students to Database

    def search_student(self):
        try:
            search_text = self.ui.lineEdit_3.text().lower()
            all_students = self.db.getAllStudents()
            filtered_students = {sid: data for sid, data in all_students.items() if search_text in data.get("full_name", "").lower() or search_text in sid.lower()}
            self.populate_student_grid(self.ui.studentsViewGridLayout, True, filtered_students)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during search: {str(e)}")

    def populate_student_grid(self, container, menuOption, students, show_attendance_icons=False):
        row = 0
        col = 0
        for student_id, student_info in students.items():
            if student_info is not None:
                status = attendance_status.get(student_id, False) if attendance_status else False
                self.createStudentWidget(row, col, container, menuOption, student_info, show_attendance_icons, status)
                col += 1
                if col == 3:  # Adjust based on your grid layout
                    col = 0
                    row += 1
            else:
                logging.warning(f"Student info for {student_id} is None, skipping...")


    def show_add_student_dialog(self):
        dialog = AddStudentDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            student_data = dialog.get_student_data()
            self.add_student_to_db(student_data)

    def add_student_to_db(self, student_data):
        student_id = student_data["student_id"]
        student_dict = {student_id: student_data}
        self.face_recognition_db.addStudent(student_dict)

        # Handle the image upload and encoding
        if student_data["image_path"]:
            image_path = student_data["image_path"]
            self.handle_image_upload(student_id, image_path)
        
        QMessageBox.information(self, "Success", "Student added successfully!")
        self.refresh_student_data(self.ui.studentsViewGridLayout)



    def handle_image_upload(self, student_id, image_path):
        img = cv2.imread(image_path)
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img_rgb)[0]

            # Load the existing encoder file
            encoder_file_path = "EncodeFile.p"
            encode_list_known, student_ids = [], []
            if os.path.exists(encoder_file_path):
                with open(encoder_file_path, 'rb') as file:
                    encode_list_known, student_ids = pickle.load(file)

            # Add the new encoding and student ID
            encode_list_known.append(encode)
            student_ids.append(student_id)

            # Save the updated encoder file
            with open(encoder_file_path, 'wb') as file:
                pickle.dump([encode_list_known, student_ids], file)

            # Upload the updated encoder file to Firebase
            encoder_db = EncoderDB()
            encoder_db.uploadFile(encoder_file_path, "Resources/EncodeFile.p")

            # Upload the image to Firebase Storage using the student ID as the filename
            remote_image_path = f"Images/{student_id}.png"
            encoder_db.uploadFile(image_path, remote_image_path)

            # Get the URL of the uploaded image
            image_url = encoder_db.get_file_url(remote_image_path)

            # Update the student record with the image URL
            self.db.updateStudentImage(student_id, image_url)
        else:
            QMessageBox.warning(self, "Error", "Failed to load the image for encoding.")

    def fillStudentAttendanceGrid(self, course_info):
        try:
            for i in reversed(range(self.ui.studentsAttendanceGrid.count())):
                widget = self.ui.studentsAttendanceGrid.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            students = self.db.getAllStudentsinClass()
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
                            self.createStudentWidget(row, col, self.ui.studentsViewGridLayout, True, student)
                            col += 1
                            if col == 3:
                                col = 0
                                row += 1
            elif isinstance(students, dict):
                for student_id, student_info in students.items():
                    self.createStudentWidget(row, col, self.ui.studentsViewGridLayout, True, student_info)
                    col += 1
                    if col == 3:
                        col = 0
                        row += 1
        except Exception as e:
            print(f"Error during refresh: {e}")

        return
    

    def refresh_student_data(self, studentGridContainer, attendance_status=None):
        try:
            for i in reversed(range(studentGridContainer.count())):
                widget = studentGridContainer.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            students = self.db.getAllStudents()
            row = 0
            col = 0
            if attendance_status is None:
                attendance_status = {}

            for student_id, student_info in students.items():
                status = attendance_status.get(student_id, False)
                self.createStudentWidget(row, col, studentGridContainer, True, student_info, show_attendance_icons=True, attendance_status=status)
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
            print(student_data, type(student_data))
            dialog = AddStudentDialog(student_data)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                updated_data = dialog.get_student_data()
                self.db.updateStudent(student_id, oldID, updated_data)
                self.refresh_student_data(self.ui.studentsViewGridLayout)
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
                self.refresh_student_data(self.ui.studentsViewGridLayout)
                print(f"Student with ID {student_id} deleted successfully.")
        except Exception as e:
            print(f"Error during delete: {e}")
            logging.error(f"Error during delete: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while deleting the student: {str(e)}")



    #Methods to show context menus
    def user_context_menu(self):

        self.show_custom_context_menu(self.ui.userDropMenuButton, ["My Classes", "My Students", "Reports", "Exit"])


    def show_custom_context_menu(self, button, menu_items):
        menu = QMenu(self)

        #Set style sheet
        menu.setStyleSheet("""
                           
                           QMenu{
                           background-color: black;
                           color: white;
                           }
                           

                           QMenu:selected{
                           background-color:white;
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
            case "Profile":
                self.switchToProfilePage()
            case "My Classes":
                self.switchToManageCoursesPage()
            case "My Students":
                self.switchToManageStudentsPage()
            case "Reports":
                self.switchToReportsPage()
            case "Exit":
                sys.exit(0)
            # case "Temp-Take Attendance":
            #     self.switchToAttendancePage()
            case _:
                pass
    

    # def switchToAttendancePage(self, course_info):
    #     self.ui.stackedWidget.setCurrentIndex(0)
    #     self.curCourse = course_info
    #     self.ui.attendancePage_classNameLabel.setText(f"""Attendance: {course_info["course_name"]}-{course_info["section_id"]}""")
    #     self.displayEnrolledStudents(self.ui.studentsAttendanceGrid, self.getEnrolledStudents())
        

    def switchToAttendancePage(self, course_info):
        # Stop the camera if it is running
        if self.camera_running:
            self.stop_camera()

        # Switch to the attendance page
        self.ui.stackedWidget.setCurrentIndex(0)
        self.current_course_info = course_info  # Set the current course context
        logging.debug(f"Switching to attendance page for course: {course_info}")

        self.ui.attendancePage_classNameLabel.setText(f"""Attendance: {course_info["course_name"]}-{course_info["section_id"]}""")
        
        attendance_status = self.get_attendance_status()  # Get attendance status
        logging.debug(f"Attendance status fetched: {attendance_status}")

        self.displayEnrolledStudents(self.ui.studentsAttendanceGrid, self.getEnrolledStudents(), attendance_status, show_attendance_icons=True)







    
    def switchToManageStudentsPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        # Must populate student tiles here
        # set flag so you don't need to repopulate everytime

    def switchToManageCoursesPage(self):
        self.current_course_info = None
        self.ui.stackedWidget.setCurrentIndex(3)
        # Must populate course tiles here
        # set flag so you don't need to repopulate everytime

    def switchToReportsPage(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def switchToProfilePage(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def getEnrolledStudents(self):
        if self.current_course_info is None:
            logging.error("Current course info is not set.")
            return []

        course_name = self.current_course_info["course_name"]
        section_id = self.current_course_info["section_id"]
        
        # Add debug logging to verify correct retrieval
        logging.debug(f"Fetching enrolled students for course: {course_name}, section: {section_id}")
        
        enrolledStudentsIDs = self.db.getEnrolledStudents(course_name, section_id)
        logging.debug(f"Enrolled Students IDs from DB: {enrolledStudentsIDs}")
        
        retDict = self.db.getStudentinfofromList(enrolledStudentsIDs)
        logging.debug(f"Enrolled Students Info: {retDict}")
        return retDict


    

    # def launch_capture(self):
    #     if self.current_course_info:
    #         course_name = self.current_course_info["course_name"]
    #         section_id = self.current_course_info["section_id"]
    #         meeting_days = self.current_course_info.get("meeting_days", [])
            
    #         if not self.is_meeting_day(meeting_days):
    #             QMessageBox.warning(self, "Not a Meeting Day", f"Today is not a scheduled meeting day for {course_name}-{section_id}.")
    #             return

    #         if not self.camera_running:  # Start the camera only if it's not running
    #             def update_present_students(detected_student_ids):
    #                 for student_id in detected_student_ids:
    #                     self.mark_student_present(student_id)
    #             testCaptureUI.launch(self.ui.widget_21, self.face_recognition_db, course_name, section_id, update_present_students)
    #             self.camera_running = True
    #     else:
    #         QMessageBox.warning(self, "No Course Selected", "Please select a course before taking attendance.")


    def launch_capture(self):
        if self.current_course_info:
            course_name = self.current_course_info["course_name"]
            section_id = self.current_course_info["section_id"]
            meeting_days = self.current_course_info.get("meeting_days", [])
            
            if not self.is_meeting_day(meeting_days):
                QMessageBox.warning(self, "Not a Meeting Day", f"Today is not a scheduled meeting day for {course_name}-{section_id}.")
                return

            if not self.camera_running:  # Start the camera only if it's not running
                def update_present_students(detected_student_ids):
                    for student_id in detected_student_ids:
                        self.mark_student_present(student_id)

                # Stop the existing thread if it is running
                if self.face_detection_thread is not None:
                    self.stop_camera()

                self.face_detection_thread = testCaptureUI.launch(
                    self.ui.widget_21, self.face_recognition_db,
                    course_name, section_id, update_present_students
                )
                self.camera_running = True
        else:
            QMessageBox.warning(self, "No Course Selected", "Please select a course before taking attendance.")







    
                
    # Context Menu operations for ================================ course card widgets:
    def course_context_menu(self, triggerButton, course_info):

        self.show_course_custom_context_menu(triggerButton, ["Edit", "Delete", "Take Attendance"], course_info)


    def show_course_custom_context_menu(self, button, menu_items, course_info):
        menu = QMenu(self)

        #Set style sheet
        menu.setStyleSheet("""
                           
                           QMenu{
                           background-color: black;
                           color: white;
                           }
                           

                           QMenu:selected{
                           background-color:white;
                           color: #12B298;
                           }
                           """)

        #Add actions to the menu
        for item_text in menu_items:
            action = QAction(item_text, self)
            action.triggered.connect(lambda: self.handle_course_menu_item_click(course_info) )
            menu.addAction(action)

        # Show the menu
        menu.move(button.mapToGlobal(button.rect().topLeft()))
        menu.exec()
    
    def handle_course_menu_item_click(self, course_info):
        text = self.sender().text()
        match text:
            case "Edit":
                self.edit_course(course_info["course_name"], course_info["section_id"])
            case "Delete":
                self.delete_course(course_info["course_name"], course_info["section_id"])
            case "Take Attendance":
                self.switchToAttendancePage(course_info)
                self.launch_capture()  # Start the camera when switching to the attendance page

            case _:
                pass

    def createCourseWidget2(self, rowNumber, columnNumber, course_info = None):

        # CREATE NEW UNIQUE NAMES FOR THE WIDGETS ---> dev check. REMOVE BEFORE DEPLOY
        newName = "frame" + course_info["course_name"]

        print(newName)

        self.courseCard = QtWidgets.QWidget()
        self.courseCard.setMinimumSize(QtCore.QSize(250, 120))
        self.courseCard.setMaximumSize(QtCore.QSize(250, 120))
        self.courseCard.setStyleSheet("background-color: rgb(247, 251, 255);\n"
                                        "\n"
                                        "QPushButton{\n"
                                        "    padding-left:10px;\n"
                                        "    padding-right:10px;\n"
                                        "    border: 1px solid gray;\n"
                                        "    border-radius: 10px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "   background-color: #b3b3b3;\n"
                                        "}")
        self.courseCard.setObjectName("courseCard")
        self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.courseCard)
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        self.widget_111 = QtWidgets.QWidget(self.courseCard)
        self.widget_111.setObjectName("widget_111")
        self.verticalLayout_131 = QtWidgets.QVBoxLayout(self.widget_111)
        self.verticalLayout_131.setObjectName("verticalLayout_131")
        self.classNameWidget = QtWidgets.QWidget(self.widget_111)
        self.classNameWidget.setObjectName("classNameWidget")
        self.horizontalLayout_121 = QtWidgets.QHBoxLayout(self.classNameWidget)
        self.horizontalLayout_121.setObjectName("horizontalLayout_121")
        self.classNameLabel = QtWidgets.QLabel(self.classNameWidget)
        self.classNameLabel.setObjectName("classNameLabel")
        self.horizontalLayout_121.addWidget(self.classNameLabel)
        self.verticalLayout_131.addWidget(self.classNameWidget)
        self.sectionIDWidget = QtWidgets.QWidget(self.widget_111)
        self.sectionIDWidget.setObjectName("sectionIDWidget")
        self.horizontalLayout_131 = QtWidgets.QHBoxLayout(self.sectionIDWidget)
        self.horizontalLayout_131.setObjectName("horizontalLayout_131")
        self.sectionLabel = QtWidgets.QLabel(self.sectionIDWidget)
        self.sectionLabel.setObjectName("sectionLabel")
        self.horizontalLayout_131.addWidget(self.sectionLabel)
        self.verticalLayout_131.addWidget(self.sectionIDWidget)
        self.horizontalLayout1.addWidget(self.widget_111)
        self.cardMenuButtonWidget = QtWidgets.QWidget(self.courseCard)
        self.cardMenuButtonWidget.setMaximumSize(QtCore.QSize(30, 150))
        self.cardMenuButtonWidget.setObjectName("cardMenuButtonWidget")
        self.horizontalLayout_141 = QtWidgets.QHBoxLayout(self.cardMenuButtonWidget)
        self.horizontalLayout_141.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_141.setSpacing(0)
        self.horizontalLayout_141.setObjectName("horizontalLayout_141")
        self.courseCardMenuButton = QtWidgets.QPushButton(self.cardMenuButtonWidget)
        self.courseCardMenuButton.setMinimumSize(QtCore.QSize(25, 50))
        self.courseCardMenuButton.setMaximumSize(QtCore.QSize(25, 150))
        self.courseCardMenuButton.setStyleSheet("QPushButton{\n"
                "                                  border:none;\n"
                "                                    }\n"
                "                                                              \n"
                "                                QPushButton:hover{\n"
                "                                  background-color: #b3b3b3;\n"
                "                                }")
        self.courseCardMenuButton.setObjectName("courseCardMenuButton")

        # Add pixmap Icon to menu button
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("UI/UI resources/BlackIcons/threeDotMenu.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.courseCardMenuButton.setIcon(icon2)
        self.courseCardMenuButton.setIconSize(QtCore.QSize(20, 30))

        self.horizontalLayout_141.addWidget(self.courseCardMenuButton)
        self.horizontalLayout1.addWidget(self.cardMenuButtonWidget)

        #retranslate functions
        _translate = QtCore.QCoreApplication.translate
        if course_info == None:
            self.classNameLabel.setText(_translate("MainWindow", "Course Name"))
            self.sectionLabel.setText(_translate("MainWindow", "Section Name"))
        else:
            self.classNameLabel.setText(_translate("MainWindow", course_info["course_name"]))
            self.sectionLabel.setText(_translate("MainWindow", course_info["section_id"]))

        # Create new attribute to Ui_Mainwindow
        # Syntax : setattr(obj, var, val)
        # Parameters :
        # obj : Object whose which attribute is to be assigned.
        # var : object attribute which has to be assigned.
        # val : value with which variable is to be assigned.
        setattr(self.ui, newName, self.courseCard)

        #$To uniquely identify each card menu button
        setattr(self.ui, "cardMenuButton" + newName, self.courseCardMenuButton)
        menuButton = getattr(self.ui, "cardMenuButton" + newName)
        self.courseCardMenuButton.clicked.connect(lambda: self.course_context_menu(menuButton, course_info))
        
        self.ui.coursesGridLayout.addWidget(self.courseCard, rowNumber, columnNumber, 1, 1)
        self.courseCard.setGraphicsEffect(QGraphicsDropShadowEffect(
        offset = QPoint(3, 3), blurRadius=10, color=QColor("#b3b3b3")
        ))


    # Context Menu operations for ================================ student card widgets:
    def student_context_menu(self, triggerButton, student_info):

        self.show_student_custom_context_menu(triggerButton, ["Edit", "Delete"], student_info)


    def show_student_custom_context_menu(self, button, menu_items, student_info):
        menu = QMenu(self)

        #Set style sheet
        menu.setStyleSheet("""
                           
                           QMenu{
                           background-color: black;
                           color: white;
                           }
                           

                           QMenu:selected{
                           background-color:white;
                           color: #12B298;
                           }
                           """)

        #Add actions to the menu
        for item_text in menu_items:
            action = QAction(item_text, self)
            action.triggered.connect(lambda: self.handle_student_menu_item_click(student_info) )
            menu.addAction(action)

        # Show the menu
        menu.move(button.mapToGlobal(button.rect().topLeft()))
        menu.exec()
    
    def handle_student_menu_item_click(self, student_info):
        text = self.sender().text()
        match text:
            case "Edit":
                self.edit_student(student_info["student_id"])
            case "Delete":
                self.delete_student(student_info["student_id"])
            case _:
                pass

    # New Student card creator
    def createStudentWidget(self, rowNumber, columnNumber, parentContainer, menuOption=True, student_info=None, show_attendance_icons=False, attendance_status=False):
        newName = "studentFrame" + student_info["student_id"]

        self.studentCard = QtWidgets.QWidget()
        self.studentCard.setMinimumSize(QtCore.QSize(250, 120))
        self.studentCard.setMaximumSize(QtCore.QSize(250, 120))
        self.studentCard.setStyleSheet("background-color: rgb(247, 251, 255);\n"
                                        "\n"
                                        "QPushButton{\n"
                                        "    padding-left:10px;\n"
                                        "    padding-right:10px;\n"
                                        "    border: 1px solid gray;\n"
                                        "    border-radius: 10px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "   background-color: #b3b3b3;\n"
                                        "}")
        self.studentCard.setObjectName("studentCard")
        self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.studentCard)
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        self.widget_111 = QtWidgets.QWidget(self.studentCard)
        self.widget_111.setObjectName("widget_111")
        self.verticalLayout_131 = QtWidgets.QVBoxLayout(self.widget_111)
        self.verticalLayout_131.setObjectName("verticalLayout_131")

        self.studentNameLayout = QtWidgets.QHBoxLayout()
        self.studentNameLayout.setObjectName("studentNameLayout")

        self.student_name_label = QtWidgets.QLabel(self.widget_111)
        self.student_name_label.setObjectName("student_name_label")
        self.studentNameLayout.addWidget(self.student_name_label)

        if show_attendance_icons:
            self.attendanceIconLabel = QtWidgets.QLabel(self.widget_111)
            self.attendanceIconLabel.setObjectName("attendanceIconLabel")
            if attendance_status:
                self.attendanceIconLabel.setText("✔️")
                self.attendanceIconLabel.setStyleSheet("color: green; font-size: 24px;")
            else:
                self.attendanceIconLabel.setText("❌")
                self.attendanceIconLabel.setStyleSheet("color: red; font-size: 24px;")
            self.studentNameLayout.addWidget(self.attendanceIconLabel)

        self.verticalLayout_131.addLayout(self.studentNameLayout)

        self.studentIDWidget = QtWidgets.QWidget(self.widget_111)
        self.studentIDWidget.setObjectName("studentIDWidget")
        self.horizontalLayout_131 = QtWidgets.QHBoxLayout(self.studentIDWidget)
        self.horizontalLayout_131.setObjectName("horizontalLayout_131")
        self.studentIDLabel = QtWidgets.QLabel(self.studentIDWidget)
        self.studentIDLabel.setObjectName("studentIDLabel")
        self.horizontalLayout_131.addWidget(self.studentIDLabel)
        self.verticalLayout_131.addWidget(self.studentIDWidget)

        self.horizontalLayout1.addWidget(self.widget_111)
        if menuOption:
            self.cardMenuButtonWidget = QtWidgets.QWidget(self.studentCard)
            self.cardMenuButtonWidget.setMaximumSize(QtCore.QSize(30, 150))
            self.cardMenuButtonWidget.setObjectName("cardMenuButtonWidget")
            self.horizontalLayout_141 = QtWidgets.QHBoxLayout(self.cardMenuButtonWidget)
            self.horizontalLayout_141.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_141.setSpacing(0)
            self.horizontalLayout_141.setObjectName("horizontalLayout_141")
            self.studentCardMenuButton = QtWidgets.QPushButton(self.cardMenuButtonWidget)
            self.studentCardMenuButton.setMinimumSize(QtCore.QSize(25, 50))
            self.studentCardMenuButton.setMaximumSize(QtCore.QSize(150, 50))
            self.studentCardMenuButton.setStyleSheet("QPushButton{\n"
                    "                                  border:none;\n"
                    "                                    }\n"
                    "                                                              \n"
                    "                                QPushButton:hover{\n"
                    "                                  background-color: #b3b3b3;\n"
                    "                                }")
            self.studentCardMenuButton.setObjectName("studentCardMenuButton")

            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("UI/UI resources/BlackIcons/threeDotMenu.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.studentCardMenuButton.setIcon(icon2)
            self.studentCardMenuButton.setIconSize(QtCore.QSize(20, 30))

            self.horizontalLayout_141.addWidget(self.studentCardMenuButton)
            self.horizontalLayout1.addWidget(self.cardMenuButtonWidget)

        _translate = QtCore.QCoreApplication.translate
        if student_info is None:
            self.student_name_label.setText(_translate("MainWindow", "Full Name"))
            self.studentIDLabel.setText(_translate("MainWindow", "Student ID"))
        else:
            self.student_name_label.setText(_translate("MainWindow", student_info["full_name"]))
            self.studentIDLabel.setText(_translate("MainWindow", student_info["student_id"]))

        setattr(self.ui, newName, self.studentCard)
        if menuOption:
            setattr(self.ui, "cardMenuButton" + newName, self.studentCardMenuButton)
            menuButton = getattr(self.ui, "cardMenuButton" + newName)
            self.studentCardMenuButton.clicked.connect(lambda: self.student_context_menu(menuButton, student_info))

        parentContainer.addWidget(self.studentCard, rowNumber, columnNumber, 1, 1)
        self.studentCard.setGraphicsEffect(QGraphicsDropShadowEffect(
        offset = QPoint(3, 3), blurRadius=10, color=QColor("#b3b3b3")
        ))




    def mark_student_present(self, student_id):
        if not self.current_course_info:
            logging.error("Current course info is not set.")
            return

        course_name = self.current_course_info["course_name"]
        section_id = self.current_course_info["section_id"]

        for i in range(self.ui.studentsAttendanceGrid.count()):
            widget = self.ui.studentsAttendanceGrid.itemAt(i).widget()
            if widget is not None:
                studentIDLabel = widget.findChild(QtWidgets.QLabel, "studentIDLabel")
                if studentIDLabel and studentIDLabel.text() == student_id:
                    attendanceIconLabel = widget.findChild(QtWidgets.QLabel, "attendanceIconLabel")
                    if attendanceIconLabel:
                        attendanceIconLabel.setText("✔️")  # Use a Unicode green check mark character
                        attendanceIconLabel.setStyleSheet("color: green; font-size: 24px;")
                        widget.update()
                        # Update the attendance status in the database
                        today_date = datetime.now().strftime('%Y-%m-%d')
                        self.db.updateAttendanceStatus(course_name, section_id, student_id, today_date, True)
                    break



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run_encoder()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

