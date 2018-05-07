""" PyQt5 imports. """

from PyQt5.QtCore import QObject, pyqtSignal

""" Proprietary imports. """

from utils import SunkenHLine, valid_color, intermediate_color

class UniversalTime(QObject):
    """ Universal time wrapper. """

    updated = pyqtSignal()

    def __init__(self, conn):
        super(UniversalTime, self).__init__()

        """ Connection object as attribute. """

        self.conn = conn
        self.conn.connection_open.connect(self.conn_synced)
        self.conn.connection_close.connect(self.conn_unsynced)

        """ Attributes definition. """

        self.ut_stream = None
        self.ut = None

        """ Callback definition. """

    def update(self, ut):
        self.ut = ut
        self.updated.emit()

    def conn_synced(self):
        """ Updating view if new connection. """

        space_center = self.conn.conn.space_center
        self.ut_stream = self.conn.conn.add_stream(getattr, space_center, 'ut')
        self.ut_stream.add_callback(self.update)
        self.ut_stream.start()

    def conn_unsynced(self):
        """ Updating view if closed connection. """

        self.ut = None
