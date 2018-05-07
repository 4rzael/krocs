""" Python imports. """

import errno

""" PyQt5 imports. """

from PyQt5.QtCore import QObject, pyqtSignal

""" Other external library imports. """

import krpc
from krpc.error import RPCError

""" Proprietary imports. """

from utils import show_error, show_info

class Vessels(QObject):
    """kRPC connection wrapper."""
    refreshed = pyqtSignal(list)

    def __init__(self, conn):
        super(Vessels, self).__init__()
        self.conn = conn
        self.vessels = None
        self.conn.connection_open.connect(self.on_connect)

    def on_connect(self):
        vessel_stream = self.conn.conn.add_stream(getattr, self.conn.conn.space_center, 'vessels')
        vessel_stream.add_callback(self.on_change)
        vessel_stream.start()

    def on_change(self, vessels):
        if type(vessels) is RPCError:
            show_error('RPCError received in vessels stream', '', str(vessels))
        elif self.vessels is None or len(self.vessels) is not len(vessels):
            self.vessels = vessels
            self.refreshed.emit(self.vessels)
