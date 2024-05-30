from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import firebase_admin
from firebase_admin import credentials, db, storage



class AddCourseDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Course")

        self.layout = QtWidgets.QFormLayout()

        self.courseName = QtWidgets.QLineEdit()
        self.sectionID = QtWidgets.QLineEdit()
        self.meetDays = QtWidgets.QLineEdit()
        self.capacity = QtWidgets.QSpinBox()

        self.layout.addRow("Course Name:", self.courseName)
        self.layout.addRow("Section ID:", self.sectionID)
        self.layout.addRow("Meeting Days (Somma separated):", self.meetDays)   # Comma separated
        self.layout.addRow("Class Capacity:", self.capacity)

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_course_data(self):
        return {
            "course_name": self.courseName.text(),
            "section_id": self.sectionID.text(),
            "meeting_days": [x.strip().lower() 
                             for x in self.meetDays.text().split(",") 
                             if x.strip().lower() in ["monday", "tuesday", "wednesday","thursday", "friday"]],
            "class_capacity": self.capacity.text()
        }