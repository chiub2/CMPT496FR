import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QFormLayout
from PyQt5.QtCore import Qt
# from face_recognition import *
class AddStudentDialog_Attendance(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setLayout(QFormLayout())
        
        self.name_input = QLineEdit()
        self.id_input = QLineEdit()
        self.major_input = QLineEdit()
        self.minor_input = QLineEdit()
        
        self.layout().addRow("Full Name:", self.name_input)
        self.layout().addRow("ID:", self.id_input)
        self.layout().addRow("Major:", self.major_input)
        self.layout().addRow("Major:", self.minor_input)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.layout().addWidget(self.submit_button)

class StudentManagementApp(QDialog):
    def __init__(self, curCourse, db = None):
        super().__init__()
        self.db = db
        self.curCourse = db.getCourse(curCourse["course_name"], curCourse["section_id"])
        self.setWindowTitle("Student Management")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search students...")
        self.layout.addWidget(self.search_bar)
        
        #=================Students from course
        try:
            self.allStudents = db.getAllStudents() #returns dictionary
            
            # do not delete!! if there are no students enrolled, error occurs
            enrolled_students_id = self.curCourse["students"] 
            
            # sort by full name           ---TO DO---
            print("These are all the students in the DB:\n\n")
            print(self.allStudents)

            for studentID in self.allStudents.keys(): 
                if self.allStudents[studentID]["student_id"] in enrolled_students_id: # Student is enrolled
                    self.allStudents[studentID].update({"enrollment_status":"enrolled"})
                else: # Student isn't enrolled
                    self.allStudents[studentID].update({"enrollment_status":"not enrolled"})
            # At the end of this loop, enrolled students have been tagged
                    
        except KeyError as e:
            print("No students enrolled at this time", e)
            for studentID in self.allStudents.keys(): 
                self.allStudents[studentID].update({"enrollment_status":"not enrolled"})
        
        self.table = QTableWidget(0, 5)
        self.layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels(["Full Name", "ID", "Major", "Minor", "Enrollment Status"])
        
        # Insert students in table
        row_position = 0
        for student in self.allStudents.values(): # change from allstudents to enrolled students
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(student["full_name"]))
            self.table.setItem(row_position, 1, QTableWidgetItem(student["student_id"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(student["major"]))
            self.table.setItem(row_position, 3, QTableWidgetItem(student["minor"]))
            statusItem = QTableWidgetItem()
            statusItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            if student["enrollment_status"].lower() == "enrolled":
                statusItem.setCheckState(Qt.CheckState.Checked)  # set as enrolled in dialog
            else:
                statusItem.setCheckState(Qt.CheckState.Unchecked)   # set as unenrolled in dialog
            self.table.setItem(row_position, 4, statusItem)
            row_position += 1

        button_layout = QHBoxLayout()
        
        
        self.close_Button = QPushButton("Save Updates & Close Dialog")
        self.close_Button.clicked.connect(self.close_button)
        button_layout.addWidget(self.close_Button)
        
        
        self.layout.addLayout(button_layout)

    def returnEnrolledStudents(self):
        studentsResult = {}
        for student_index in range(self.table.rowCount()):
            student = self.getRowData(student_index)
            studentsResult.update(student)
        self.close()
        enrolledStudents = [x["student_id"] for x in studentsResult.values() if x["enrollment_status"].lower() == "enrolled"]
        self.db.setEnrolledStudents(self.curCourse["course_name"], self.curCourse["section_id"], enrolledStudents)
        print("Final Students Results::\n\n",studentsResult)
        return studentsResult


    def close_button(self) -> dict:
        studentsResult = self.returnEnrolledStudents()
        self.close()
        return studentsResult

    def getRowData(self, row_position:int):
        # Assumes student id is valid, not secure
        key_list = ["full_name", "student_id", "major", "minor"]
        student_id = self.table.item(row_position,1).text()
        student_data = {student_id:{}}
        for index in range(4):
            student_data[student_id].update({key_list[index]: self.table.item(row_position,index).text()})
        
        if self.table.item(row_position,4).checkState() == Qt.CheckState.Checked:
            student_data[student_id].update({"enrollment_status": "enrolled"})
        else:
            student_data[student_id].update({"enrollment_status": "not enrolled"})

        '''
        student_data Structure:
        {
        "student_id": {
                        "full_name" : ...
                        "student_id": ...
                        ...
                        "status": ... ["enrolled"  OR "not enrolled"]
                        }
        }
        '''
        return student_data

    
    def open_add_student_dialog(self):
        dialog = AddStudentDialog_Attendance()
        if dialog.exec() == QDialog.Accepted:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(dialog.name_input.text()))
            self.table.setItem(row_position, 1, QTableWidgetItem(dialog.id_input.text()))
            self.table.setItem(row_position, 2, QTableWidgetItem(dialog.major_input.text()))
            self.table.setItem(row_position, 3, QTableWidgetItem(dialog.minor_input.text()))
            statusItem = QTableWidgetItem("Active")
            statusItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            statusItem.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row_position, 4, statusItem)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagementApp()
    window.show()
    sys.exit(app.exec_())
