""" PyQt5 imports. """

from PyQt5.QtCore import QObject, pyqtSignal

""" Other external library imports. """

from krpc.error import RPCError

""" Proprietary imports. """

from utils import SunkenHLine, valid_color, intermediate_color, show_error

class UniversalTime(QObject):
    """ Universal time wrapper. """

    updated = pyqtSignal(float)

    def __init__(self, conn):
        super(UniversalTime, self).__init__()

        """ Connection object as attribute. """

        self.conn = conn
        self.conn.synced.connect(self._conn_synced)

        """ Attributes definition. """

        self.stream = None
        self.value = None

        """ Callback definition. """

    def _update(self, value):
        if type(value) is RPCError:
            show_error('RPCError received in ut stream', '', str(value))
        else:
            self.value = value
            self.updated.emit(self.value)

    def _conn_synced(self):
        """ Updating view if new connection. """

        self.stream = self.conn.value.add_stream(getattr,
        self.conn.value.space_center, 'ut')
        self.stream.add_callback(self._update)
        self.stream.start()
