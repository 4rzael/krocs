""" Python imports. """

import sys
import errno
from socket import error as socket_error

""" Path tricks. """

sys.path.append('..')

""" PyQt5 imports. """

from PyQt5.QtCore import QObject, pyqtSignal

""" Other external library imports. """

import krpc

""" Proprietary imports. """

from utils import show_error, show_info

class Connection(QObject):
    """kRPC connection wrapper."""
    connection_open = pyqtSignal()
    connection_close = pyqtSignal()

    def __init__(self):
        super(Connection, self).__init__()
        self.conn = None
        self.name = None
        self.addr = None
        self.rpc_port = None
        self.stream_port = None

    """ Set a new connection. """
    def setConn(self, name, addr, rpc_port, stream_port):
        if self.conn != None:
            self.close()
        try:
            conn = krpc.connect(
                name = name,
                address = addr,
                rpc_port = rpc_port,
                stream_port= stream_port)
            self.conn = conn
            self.name = name
            self.addr = addr
            self.rpc_port = rpc_port
            self.stream_port = stream_port
            self.connection_open.emit()
            show_info("Connection established.", "Successfully\
            connected to %s." % addr, "Connected to %s as %s\
            with rpc and stream ports respectively %s and %s" %
            (addr, name, rpc_port, stream_port))
        except (socket_error) as serr:
            if serr.errno == errno.ECONNREFUSED:
                show_error("Connection refused.", None, None)
            else:
                raise serr

    """ Terminate connection if any. """
    def close(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None
            self.name = None
            self.addr = None
            self.rpc_port = None
            self.stream_port = None
            self.connection_close.emit()
            show_info("Connection terminated.", None, None)
