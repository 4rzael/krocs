""" PyQt5 imports. """
from PyQt5.QtWidgets import QFrame

class SunkenHLine(QFrame):
    def __init__(self):
        super(SunkenHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
