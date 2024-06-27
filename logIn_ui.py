# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logIn.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_(object):
    def setupUi(self, __qt_fake_top_level):
        if not __qt_fake_top_level.objectName():
            __qt_fake_top_level.setObjectName(u"__qt_fake_top_level")
        self.widget_10 = QWidget(__qt_fake_top_level)
        self.widget_10.setObjectName(u"widget_10")
        self.widget_10.setGeometry(QRect(429, 186, 250, 100))
        self.widget_10.setMinimumSize(QSize(250, 100))
        self.widget_10.setMaximumSize(QSize(250, 100))
        self.widget_10.setStyleSheet(u"background-color: rgb(247, 251, 255);")
        self.horizontalLayout = QHBoxLayout(self.widget_10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_11 = QWidget(self.widget_10)
        self.widget_11.setObjectName(u"widget_11")
        self.verticalLayout_13 = QVBoxLayout(self.widget_11)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.widget_20 = QWidget(self.widget_11)
        self.widget_20.setObjectName(u"widget_20")
        self.horizontalLayout_12 = QHBoxLayout(self.widget_20)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_2 = QLabel(self.widget_20)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_12.addWidget(self.label_2)


        self.verticalLayout_13.addWidget(self.widget_20)

        self.widget_19 = QWidget(self.widget_11)
        self.widget_19.setObjectName(u"widget_19")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_19)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_6 = QLabel(self.widget_19)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_13.addWidget(self.label_6)


        self.verticalLayout_13.addWidget(self.widget_19)


        self.horizontalLayout.addWidget(self.widget_11)

        self.widget_12 = QWidget(self.widget_10)
        self.widget_12.setObjectName(u"widget_12")
        self.widget_12.setMaximumSize(QSize(30, 150))
        self.horizontalLayout_14 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.widget_12)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(25, 50))
        self.pushButton.setMaximumSize(QSize(25, 150))
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"    }\n"
"                              \n"
"QPushButton:hover{\n"
"	background-color: #b3b3b3;\n"
"}")

        self.horizontalLayout_14.addWidget(self.pushButton)


        self.horizontalLayout.addWidget(self.widget_12)


        self.retranslateUi(__qt_fake_top_level)

        QMetaObject.connectSlotsByName(__qt_fake_top_level)
    # setupUi

    def retranslateUi(self, __qt_fake_top_level):
        self.label_2.setText(QCoreApplication.translate("", u"Class Name:", None))
        self.label_6.setText(QCoreApplication.translate("", u"Section ID:", None))
        self.pushButton.setText(QCoreApplication.translate("", u"menu", None))
        pass
    # retranslateUi

