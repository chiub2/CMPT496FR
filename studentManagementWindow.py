import sys
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QFormLayout

class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setLayout(QFormLayout())
        
        self.name_input = QLineEdit()
        self.id_input = QLineEdit()
        self.email_input = QLineEdit()
        
        self.layout().addRow("Name:", self.name_input)
        self.layout().addRow("ID:", self.id_input)
        self.layout().addRow("Email:", self.email_input)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.layout().addWidget(self.submit_button)

class StudentManagementApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search students...")
        self.layout.addWidget(self.search_bar)
        
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "ID", "Email", "Status"])
        self.layout.addWidget(self.table)
        
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.open_add_student_dialog)
        button_layout.addWidget(self.add_button)
        
        self.remove_button = QPushButton("Remove Selected")
        button_layout.addWidget(self.remove_button)
        
        self.layout.addLayout(button_layout)
    
    def open_add_student_dialog(self):
        dialog = AddStudentDialog()
        if dialog.exec() == QDialog.Accepted:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(dialog.name_input.text()))
            self.table.setItem(row_position, 1, QTableWidgetItem(dialog.id_input.text()))
            self.table.setItem(row_position, 2, QTableWidgetItem(dialog.email_input.text()))
            self.table.setItem(row_position, 3, QTableWidgetItem("Active"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagementApp()
    window.show()
    sys.exit(app.exec_())
