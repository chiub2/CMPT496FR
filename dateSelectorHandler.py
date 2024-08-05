import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QDialog, QPushButton, QCalendarWidget, QHBoxLayout
from PyQt5 import QtCore

class CalendarDialog(QDialog):
    dateSelected = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pick a Date")
        self.setGeometry(100, 100, 500, 400)
        
        self.layout = QVBoxLayout(self)
        self.calendarWidget = QCalendarWidget()
        self.layout.addWidget(self.calendarWidget)

        self.buttonHBox = QHBoxLayout()
        self.layout.addLayout(self.buttonHBox)

        self.selectDateButton = QPushButton("Select Date")
        self.selectDateButton.setMinimumSize(QtCore.QSize(100, 30))
        self.selectDateButton.setMaximumSize(QtCore.QSize(100, 30))
        self.selectDateButton.setStyleSheet("QPushButton{\n"
                                            "    padding-left:10px;\n"
                                            "    padding-right:10px;\n"
                                            "    border: 1px solid gray;\n"
                                            "    border-radius: 10px;\n"
                                            "    background-color: #e3dadc;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "   background-color: #b3b3b3;\n"
                                            "}")
        self.buttonHBox.addWidget(self.selectDateButton)
        self.selectDateButton.clicked.connect(self.acceptDate)
        self.setModal(True)
    
    def acceptDate(self):
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.dateSelected.emit(selected_date)
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarDialog()
    window.show()
    sys.exit(app.exec_())
