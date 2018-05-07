""" Python imports. """
import sys

""" path tricks. """
sys.path.append('..')

""" PyQt5 imports. """

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QValidator
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
QFormLayout)

""" Proprietary imports. """

from utils import SunkenHLine, valid_color, intermediate_color

class ConnectionWindow(QWidget):
    """ Connection to kRPC server window."""

    def __init__(self, conn):
        super(ConnectionWindow, self).__init__()

        """ Connection object as attribute. """

        self.conn = conn
        self.conn.connection_open.connect(self.connected)
        self.conn.connection_close.connect(self.closed)

        """ Connection form attributes definitions. """

        name_lbl = QLabel("Connection name:")
        self.name = QLineEdit()
        name_regexp = QRegExp("^[\w\-\s]+$")
        name_validator = QRegExpValidator(name_regexp)
        self.name.setValidator(name_validator)

        self.name.textChanged.connect(self.validate_form)
        addr_lbl = QLabel("Server address:")
        self.addr = QLineEdit()
        ipv4_regexp = QRegExp("((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}" +
        "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        ipv4_validator = QRegExpValidator(ipv4_regexp)
        self.addr.setValidator(ipv4_validator)
        self.addr.textChanged.connect(self.validate_form)

        rpc_port_lbl = QLabel("RPC port:")
        self.rpc_port = QLineEdit()
        tcp_regexp = QRegExp("([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65" +
        "[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])")
        tcp_validator = QRegExpValidator(tcp_regexp)
        self.rpc_port.setValidator(tcp_validator)
        self.rpc_port.textChanged.connect(self.validate_form)

        stream_port_lbl = QLabel("Stream port:")
        self.stream_port = QLineEdit()
        self.stream_port.setValidator(tcp_validator)
        self.stream_port.textChanged.connect(self.validate_form)

        self.conn_btn = QPushButton("Connect")
        self.conn_btn.setDefault(True)
        self.conn_btn.clicked.connect(lambda:self.request_connect())

        status_lbl = QLabel("Connection status:")
        self.status = QLabel("Not connected.")

        self.close_btn = QPushButton("Close connection")
        self.close_btn.setEnabled(False)
        self.close_btn.clicked.connect(lambda:self.request_close())

        """ Connection form layout definition. """

        fbox = QFormLayout()
        fbox.addRow(name_lbl, self.name)
        fbox.addRow(addr_lbl, self.addr)
        fbox.addRow(rpc_port_lbl, self.rpc_port)
        fbox.addRow(stream_port_lbl, self.stream_port)
        fbox.addRow(self.conn_btn)
        fbox.addRow(SunkenHLine())
        fbox.addRow(status_lbl, self.status)
        fbox.addRow(self.close_btn)

        """ Connection window layout definition. """

        self.setLayout(fbox)
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)
        self.setWindowTitle("Connection to kRPC server")

        """ Signals emission to perform first validation fullfilling decoration
        purposes """

        self.name.textChanged.emit(self.name.text())
        self.addr.textChanged.emit(self.addr.text())
        self.rpc_port.textChanged.emit(self.rpc_port.text())
        self.stream_port.textChanged.emit(self.stream_port.text())

    def validate_form(self):
        """ form validation for each attributes, changing attributes background
        color and connection button enabled property. """

        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = valid_color
        elif state == QValidator.Intermediate:
            color = intermediate_color
        else:
            color = critical_color
        sender.setStyleSheet("QLineEdit { background-color: %s }" % color)

        name_validator = self.name.validator()
        addr_validator = self.addr.validator()
        rpc_port_validator = self.rpc_port.validator()
        stream_port_validator = self.stream_port.validator()

        name_state = name_validator.validate(self.name.text(), 0)[0]
        addr_state = addr_validator.validate(self.addr.text(), 0)[0]
        rpc_port_state = rpc_port_validator.validate(self.rpc_port.text(), 0)[0]
        stream_port_state = stream_port_validator.validate(
         self.stream_port.text(), 0)[0]

        if (name_state == QValidator.Acceptable and
            addr_state == QValidator.Acceptable and
            rpc_port_state == QValidator.Acceptable and
            stream_port_state == QValidator.Acceptable):
            self.conn_btn.setEnabled(True)
        else:
            self.conn_btn.setEnabled(False)

    def request_connect(self):
        """ Requesting a connection object from a kRPC server. """

        self.conn.setConn(self.name.text(), self.addr.text(),
        int(self.rpc_port.text()), int(self.stream_port.text()))

    def request_close(self):
        """ Terminating a connection. """

        self.conn.close()

    def connected(self):
        """ Updating view if new connection. """

        self.status.setText("Connected to %s." % self.conn.addr)
        self.close_btn.setEnabled(True)

    def closed(self):
        """ Updating view if closed connection. """
        self.status.setText("Not connected.")
        self.close_btn.setEnabled(False)
