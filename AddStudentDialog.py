from tkinter.filedialog import FileDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from mainWindowInterface import Ui_MainWindow  # Your actual UI file import
import firebase_admin
from firebase_admin import credentials, db, storage
from PyQt5.QtWidgets import QFileDialog


class AddStudentDialog(QtWidgets.QDialog):
    def __init__(self, param=None):
        super().__init__()
        self.setWindowTitle("Add Student")

        self.layout = QtWidgets.QFormLayout()
        
        self.student_id = QtWidgets.QLineEdit()
        self.full_name = QtWidgets.QLineEdit()
        self.major = QtWidgets.QLineEdit()
        self.minor = QtWidgets.QLineEdit()
        self.total_attendance = QtWidgets.QSpinBox()
        self.image_path = QtWidgets.QLineEdit()
        self.image_path.setReadOnly(True)
        self.upload_button = QtWidgets.QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)

        self.layout.addRow("Student ID:", self.student_id)
        self.layout.addRow("Full Name:", self.full_name)
        self.layout.addRow("Major:", self.major)
        self.layout.addRow("Minor:", self.minor)
        self.layout.addRow("Total Attendance:", self.total_attendance)
        self.layout.addRow("Image:", self.image_path)
        self.layout.addRow("", self.upload_button)

        if param is not None:
            self.student_id.setText(param["student_id"])
            self.full_name.setText(param["full_name"])
            self.major.setText(param["major"])
            self.minor.setText(param["minor"])
            self.total_attendance.setValue(param["total_attendance"])

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)
        self.setModal(True)

    def get_student_data(self):
        return {
            "student_id": self.student_id.text(),
            "full_name": self.full_name.text(),
            "major": self.major.text(),
            "minor": self.minor.text(),
            "total_attendance": self.total_attendance.value(),
            "image_path": self.image_path.text()
        }

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.image_path.setText(file_name)