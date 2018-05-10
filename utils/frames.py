""" PyQt5 imports. """

from PyQt5.QtWidgets import QFrame, QLabel

""" Proprietary imports. """

from .colors import valid_color, intermediate_color, critical_color

class SunkenHLine(QFrame):
    def __init__(self):
        super(SunkenHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class StatusLabel(QLabel):
    def __init__(self, text):
        super(QLabel, self).__init__()
        self.setText(text)
        self.setAutoFillBackground(True)
        self.setStyleSheet(
        "QLabel { margin-left: 5px; border-radius: 5px; " +
        "background-color: %s; }" % critical_color)

    def setValid(self):
        self.setStyleSheet(
        "QLabel { margin-left: 5px; border-radius: 5px; " +
        "background-color: %s; }" % valid_color)

    def setIntermediate(self):
        self.setStyleSheet(
        "QLabel { margin-left: 5px; border-radius: 5px; " +
        "background-color: %s; }" % intermediate_color)

    def setCritical(self):
        self.setStyleSheet(
        "QLabel { margin-left: 5px; border-radius: 5px; " +
        "background-color: %s; }" % critical_color)
