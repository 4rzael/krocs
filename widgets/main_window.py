""" Python imports. """

import sys

""" Path tricks. """
sys.path.append('..')

""" PyQt5 imports. """

from PyQt5.QtWidgets import (QMainWindow, QAction, QStatusBar,
QLabel, QMdiArea)

""" Proprietary imports. """

from widgets import ConnectionWindow
from objects import UniversalTime

class MainWindow(QMainWindow):

   def __init__(self, conn, parent = None):
      super(MainWindow, self).__init__(parent)

      """ Connection object as attribute. """

      self.conn = conn
      self.conn.connection_open.connect(self.conn_synced)
      self.conn.connection_close.connect(self.conn_unsynced)

      """ Attributes definition. """
      self.ut = UniversalTime(conn)
      self.ut.updated.connect(self.ut_updated)

      """ Populating menu bar. """

      bar = self.menuBar()
      remote = bar.addMenu("Remote")

      """ Populating file menu. """

      remote.addAction("Connection to kRPC server")
      remote.triggered[QAction].connect(self.remoteaction)

      """ Populating status bar. """

      self.status_bar = QStatusBar()
      self.status_conn = QLabel("Not connected.")
      self.status_ut = QLabel("UT not synchronized.")
      self.status_bar.addWidget(self.status_conn)
      self.status_bar.addWidget(self.status_ut)
      self.setStatusBar(self.status_bar)

      """ Define window layout. """

      self.setWindowTitle("Krocs")
      self.mdi = QMdiArea()
      self.setCentralWidget(self.mdi)

   def remoteaction(self, q):

       if q.text() == "Connection to kRPC server":
          connection_window = ConnectionWindow(self.conn)
          connection_window.show()

   def conn_synced(self):
       """ Updating view if new connection. """

       self.status_conn.setText("Connected to %s." % self.conn.addr)

   def conn_unsynced(self):
       """ Updating view if closed connection. """

       self.status_conn.setText("Not connected.")
       self.status_ut.setText("UT: Not synchronized.")

   def ut_updated(self):
       """ Update view if UT changed. """
       self.status_ut.setText("UT: %02d/%03d %d:%02d:%02d" % (int(self.ut.ut) // 9203328, ((int(self.ut.ut) // 21600000) % 42608) // 1000,
       (int(self.ut.ut) // 3600) % 6, (int(self.ut.ut) // 60) % 60, int(self.ut.ut) % 60))
