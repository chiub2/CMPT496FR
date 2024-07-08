import sys
from PyQt5.QtWidgets import QApplication,  QVBoxLayout
from PyQt5 import QtWidgets, QtCore

class CalendarDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pick a Date")

        self.setGeometry(100, 100, 500, 400)
        self.layout = QVBoxLayout(self)
        self.calendarDialog =  QtWidgets.QVBoxLayout()
        
        self.calendarWidget = QtWidgets.QCalendarWidget()
        self.layout.addWidget(self.calendarWidget)

        self.buttonHBox = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.buttonHBox)

        self.selectDateButton = QtWidgets.QPushButton()
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
        self.selectDateButton.setText("Select Date")
        self.buttonHBox.addWidget(self.selectDateButton)
        
       
        self.selectDateButton.clicked.connect(self.returnDate)
        self.setModal(True)
    
    def returnDate(self):
        self.close()
        ''' 
        Date Format:    DAYofWeek MONTH DD YYYY
                    E.g: Tue Jul 16 2024                 
        '''
        return(self.calendarWidget.selectedDate().toString())

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarDialog()
    window.show()
    sys.exit(app.exec_())