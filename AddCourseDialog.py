from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import firebase_admin
from firebase_admin import credentials, db, storage



class AddCourseDialog(QtWidgets.QDialog):
    def __init__(self, param = None):
        super().__init__()
        self.setWindowTitle("Add Course")

        self.layout = QtWidgets.QFormLayout()

        self.courseName = QtWidgets.QLineEdit()
        self.sectionID = QtWidgets.QLineEdit()
        self.meetDays = QtWidgets.QLineEdit()
        self.capacity = QtWidgets.QSpinBox()

        self.layout.addRow("Course Name:", self.courseName)
        self.layout.addRow("Section ID:", self.sectionID)
        self.layout.addRow("Meeting Days (Comma separated):", self.meetDays)   # Comma separated
        self.layout.addRow("Class Capacity:", self.capacity)


        if param != None:
            self.courseName.setText(param["course_name"])
            self.sectionID.setText(param["section_id"])
            try:
                self.meetDays.setText(", ".join(param["meeting_days"]))
            except Exception as e:
                print("Error tryign to obtain Meeting days", e)
            self.capacity.setValue(param["class_capacity"])

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)
        self.setModal(True)

    def get_course_data(self):
        return {
            "course_name": self.courseName.text(),
            "section_id": self.sectionID.text(),
            "meeting_days": [x.strip().lower()            #only accepts valid days
                             for x in self.meetDays.text().split(",") 
                             if x.strip().lower() in ["monday", "tuesday", "wednesday","thursday", "friday"]],
            "class_capacity": self.capacity.value()
        }