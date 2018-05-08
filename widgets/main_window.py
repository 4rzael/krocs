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

from objects import Vessels

class MainWindow(QMainWindow):

   def __init__(self, conn, parent = None):
      super(MainWindow, self).__init__(parent)

      """ Connection object as attribute. """

      self.conn = conn
      self.conn.conn_synced.connect(self._conn_synced)
      self.conn.conn_unsynced.connect(self._conn_unsynced)

      """ Dictionary of objects available to the window and widgets"""

      self.objects = {}
      self.objects['ut'] = UniversalTime(self.conn)
      self.objects['vessels'] = Vessels(self.conn)

      """ Populating menu bar. """

      bar = self.menuBar()
      remote_menu = bar.addMenu("Remote")
      vessels_menu = bar.addMenu("Vessels")

      """ Populating Remote menu. """

      def remote_action(q):
          if q.text() == "Connection to kRPC server":
              connection_window = ConnectionWindow(conn)
              connection_window.show()
      remote_menu.addAction("Connection to kRPC server")
      remote_menu.triggered[QAction].connect(remote_action)

      """ Populating Vessels menu. """

      def vessels_updated(vessels):
          vessels_menu.clear()
          for vessel in vessels:
              vessels_menu.addAction(vessel.name)
      self.objects['vessels'].updated.connect(vessels_updated)

      """ Populating status bar. """

      self.status_conn = QLabel("Not connected.")
      self.status_ut = QLabel("UT not synchronized.")
      self.status_bar = QStatusBar()
      self.status_bar.addWidget(self.status_conn)
      self.status_bar.addWidget(self.status_ut)
      self.objects['ut'].updated.connect(self._ut_updated)

      self.setStatusBar(self.status_bar)

      """ Define window layout. """

      self.setWindowTitle("Krocs")
      self.mdi = QMdiArea()
      self.setCentralWidget(self.mdi)

   def _conn_synced(self):
       """ Updating view if new connection. """
       self.status_conn.setText("Connected to %s." % self.conn.addr)

   def _conn_unsynced(self):
       """ Updating view if closed connection. """
       self.status_conn.setText("Not connected.")
       self.status_ut.setText("UT: Not synchronized.")

   def _ut_updated(self):
       """ Update view if UT changed. """
       self.status_ut.setText("UT: Y%02d/D%03d %d:%02d:%02d" %
       (int(self.objects['ut'].value) // 9203328,
       ((int(self.objects['ut'].value) // 21600000) % 42608) // 1000,
       (int(self.objects['ut'].value) // 3600) % 6,
       (int(self.objects['ut'].value) // 60) % 60,
       int(self.objects['ut'].value) % 60))
