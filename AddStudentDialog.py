from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from mainWindowInterface import Ui_MainWindow  # Your actual UI file import
import firebase_admin
from firebase_admin import credentials, db, storage



class AddStudentDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")

        self.layout = QtWidgets.QFormLayout()

        self.student_id = QtWidgets.QLineEdit()
        self.full_name = QtWidgets.QLineEdit()
        self.major = QtWidgets.QLineEdit()
        self.minor = QtWidgets.QLineEdit()
        self.total_attendance = QtWidgets.QSpinBox()

        self.layout.addRow("Student ID:", self.student_id)
        self.layout.addRow("Full Name:", self.full_name)
        self.layout.addRow("Major:", self.major)
        self.layout.addRow("Minor:", self.minor)
        self.layout.addRow("Total Attendance:", self.total_attendance)

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_student_data(self):
        return {
            "student_id": self.student_id.text(),
            "full_name": self.full_name.text(),
            "major": self.major.text(),
            "minor": self.minor.text(),
            "total_attendance": self.total_attendance.value()
        }