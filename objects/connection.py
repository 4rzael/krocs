""" Python imports. """

import errno
from socket import error as socket_error

""" PyQt5 imports. """

from PyQt5.QtCore import QObject, pyqtSignal

""" Other external library imports. """

import krpc

""" Proprietary imports. """

from utils import show_error, show_info

class Connection(QObject):
    """kRPC connection wrapper."""
    synced = pyqtSignal()
    unsynced = pyqtSignal()

    def __init__(self):
        super(Connection, self).__init__()
        self.connected = False
        self.value = None
        self.name = None
        self.addr = None
        self.rpc_port = None
        self.stream_port = None

    """ Set a new connection. """
    def sync(self, name, addr, rpc_port, stream_port):
        if self.value != None:
            self.close()
        try:
            value = krpc.connect(
                name = name,
                address = addr,
                rpc_port = rpc_port,
                stream_port= stream_port)
            self.value = value
            self.name = name
            self.addr = addr
            self.rpc_port = rpc_port
            self.stream_port = stream_port
            self.connected = True
            self.synced.emit()
            show_info("Connection established.", "Successfully\
            connected to %s." % addr, "Connected to %s as %s\
            with rpc and stream ports respectively %s and %s" %
            (addr, name, rpc_port, stream_port))
        except (socket_error) as serr:
            if serr.errno == errno.ECONNREFUSED:
                show_error("Connection refused.", None, None)
            else:
                raise serr
        except krpc.error.ConnectionError as cerr:
            show_error("Connection Error.",
            "Connection to krpc server raised error.",
            str(cerr))

    """ Terminate connection if any. """
    def unsync(self):
        if self.value != None:
            self.value.close()
            self.value = None
            self.name = None
            self.addr = None
            self.rpc_port = None
            self.stream_port = None
            self.connected = False
            self.unsynced.emit()
            show_info("Connection terminated.", None, None)
