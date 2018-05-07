""" PyQt5 imports. """

from PyQt5.QtCore import QObject, pyqtSignal

""" Other external library imports. """

from krpc.error import RPCError

""" Proprietary imports. """

from utils import show_error, show_info

class Vessels(QObject):
    """kRPC connection wrapper."""
    updated = pyqtSignal(list)

    def __init__(self, conn):
        super(Vessels, self).__init__()
        self.conn = conn
        self.value = None
        self.conn.conn_synced.connect(self._conn_synced)
    def _conn_synced(self):

        vessel_stream = self.conn.value.add_stream(getattr, self.conn.value.space_center, 'vessels')
        vessel_stream.add_callback(self._update)
        vessel_stream.start()

    def _update(self, vessels):
        if type(vessels) is RPCError:
            show_error('RPCError received in vessels stream', '', str(vessels))
        elif self.value is None or len(self.value) is not len(vessels):
            self.value = vessels
            self.updated.emit(self.value)
