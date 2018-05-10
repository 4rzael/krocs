""" PyQt5 imports. """

from PyQt5.QtWidgets import (QMainWindow, QAction, QStatusBar,
QLabel, QMdiArea)

""" Proprietary imports. """

from widgets import ConnectionWindow
from objects import Vessels
from .vessels_menu import VesselsMenu

class MainWindow(QMainWindow):

   def __init__(self, conn, parent = None):
      super(MainWindow, self).__init__(parent)

      """ Connection object as attribute. """

      self.conn = conn
      self.conn.connection_open.connect(self.connected)
      self.conn.connection_close.connect(self.closed)

      """ Dictionary of objects available to the window and widgets"""

      self.objects = {}
      self.objects['vessels'] = Vessels(self.conn)

      """ Populating menu bar. """

      bar = self.menuBar()
      remote_menu = bar.addMenu("Remote")
      vessels_menu = VesselsMenu(self, self.objects['vessels'], bar)

      """ Populating Remote menu. """

      remote_menu.addAction("Connection to kRPC server")
      remote_menu.triggered[QAction].connect(self.remoteaction)

      """ Populating status bar. """

      self.status_bar = QStatusBar()
      self.status_conn = QLabel("Not connected.")
      self.status_bar.addWidget(self.status_conn)
      self.setStatusBar(self.status_bar)

      """ Define window layout. """

      self.setWindowTitle("Krocs")
      self.mdi = QMdiArea()
      self.setCentralWidget(self.mdi)

   def remoteaction(self, q):
       if q.text() == "Connection to kRPC server":
          connection_window = ConnectionWindow(self.conn)
          connection_window.show()

   def connected(self):
       """ Updating view if new connection. """

       self.status_conn.setText("Connected to %s." % self.conn.addr)

   def closed(self):
       """ Updating view if closed connection. """

       self.status_conn.setText("Not connected.")
