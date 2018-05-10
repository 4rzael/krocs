""" Python imports. """

import sys

""" Path tricks. """
sys.path.append('..')

""" PyQt5 imports. """

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QValidator
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
QFormLayout)

""" Proprietary imports. """

from utils import (SunkenHLine, StatusLabel, valid_color, intermediate_color,
critical_color)

class ConnectionWindow(QWidget):
    """ Connection to kRPC server window."""

    def __init__(self, conn):
        super(ConnectionWindow, self).__init__()

        """ Set window modality """
        self.setWindowModality(Qt.WindowModal)

        """ Connection object as attribute. """

        self.conn = conn
        self.conn.synced.connect(self._conn_synced)
        self.conn.unsynced.connect(self._conn_unsynced)

        """ Connection form attributes definitions. """

        name_lbl = QLabel("Connection name:")
        self.name = QLineEdit("Default")
        name_regexp = QRegExp("^[\w\-\s]+$")
        name_validator = QRegExpValidator(name_regexp)
        self.name.setValidator(name_validator)

        self.name.textChanged.connect(self.validate_form)
        addr_lbl = QLabel("Server address:")
        self.addr = QLineEdit("127.0.0.1")
        ipv4_regexp = QRegExp("((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}" +
        "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        ipv4_validator = QRegExpValidator(ipv4_regexp)
        self.addr.setValidator(ipv4_validator)
        self.addr.textChanged.connect(self.validate_form)

        rpc_port_lbl = QLabel("RPC port:")
        self.rpc_port = QLineEdit("50000")
        tcp_regexp = QRegExp("([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65" +
        "[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])")
        tcp_validator = QRegExpValidator(tcp_regexp)
        self.rpc_port.setValidator(tcp_validator)
        self.rpc_port.textChanged.connect(self.validate_form)

        stream_port_lbl = QLabel("Stream port:")
        self.stream_port = QLineEdit("50001")
        self.stream_port.setValidator(tcp_validator)
        self.stream_port.textChanged.connect(self.validate_form)

        self.sync_btn = QPushButton("Connect")
        self.sync_btn.setDefault(True)
        self.sync_btn.clicked.connect(lambda:self._request_sync())

        status_lbl = QLabel("Connection status:")
        self.status = StatusLabel("Not connected.")

        self.unsync_btn = QPushButton("Disconnect")
        if self.conn.connected == False:
            self.unsync_btn.setEnabled(False)
        self.unsync_btn.clicked.connect(lambda:self._request_unsync())

        """ Connection form layout definition. """

        fbox = QFormLayout()
        fbox.addRow(name_lbl, self.name)
        fbox.addRow(addr_lbl, self.addr)
        fbox.addRow(rpc_port_lbl, self.rpc_port)
        fbox.addRow(stream_port_lbl, self.stream_port)
        fbox.addRow(self.sync_btn)
        fbox.addRow(SunkenHLine())
        fbox.addRow(status_lbl, self.status)
        fbox.addRow(self.unsync_btn)

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
            self.sync_btn.setEnabled(True)
        else:
            self.sync_btn.setEnabled(False)

    def _request_sync(self):
        """ Requesting a connection object from a kRPC server. """
        self.conn.sync(self.name.text(), self.addr.text(),
        int(self.rpc_port.text()), int(self.stream_port.text()))

    def _request_unsync(self):
        """ Terminating a connection. """
        self.conn.unsync()
        self.unsync_btn = QPushButton("Close connection")

    def _conn_synced(self):
        """ Updating view if new connection. """
        self.status.setText("Connected to %s." % self.conn.addr)
        self.status.setValid()
        self.unsync_btn.setEnabled(True)

    def _conn_unsynced(self):
        """ Updating view if closed connection. """
        self.status.setText("Not connected.")
        self.status.setCritical()
        self.unsync_btn.setEnabled(False)
