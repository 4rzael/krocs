""" PyQt5 imports. """

from PyQt5.QtWidgets import QMessageBox

def show_error(text, info_text, detail_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText(text)
    msg.setWindowTitle("Critical")
    if info_text is not None:
        msg.setInformativeText(info_text)
    if detail_text is not None:
        msg.setDetailedText(detail_text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.buttonClicked.connect(msg.close)
    msg.exec_()

def show_info(text, info_text, detail_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText(text)
    msg.setWindowTitle("Information")
    if info_text is not None:
        msg.setInformativeText(info_text)
    if detail_text is not None:
        msg.setDetailedText(detail_text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.buttonClicked.connect(msg.close)
    msg.exec_()
