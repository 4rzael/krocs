
""" PyQt5 imports. """
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QMainWindow, QAction, QStatusBar,
QLabel, QMdiArea)

""" Proprietary imports. """

from widgets import ConnectionWindow
from objects import UniversalTime, Vessels
from utils import StatusLabel
from .vessels_menu import VesselsMenu

class MainWindow(QMainWindow):

   def __init__(self, conn, parent = None):
      super(MainWindow, self).__init__(parent)

      """ Connection object as attribute. """

      self.conn = conn
      self.conn.synced.connect(self._conn_synced)
      self.conn.unsynced.connect(self._conn_unsynced)

      """ Dictionary of objects available to the window and widgets"""

      self.objects = {}
      self.objects['ut'] = UniversalTime(self.conn)
      self.objects['vessels'] = Vessels(self.conn)

      """ Populating menu bar. """

      bar = self.menuBar()
      remote_menu = bar.addMenu("Remote")
      vessels_menu = VesselsMenu(self, self.objects['vessels'], bar)

      """ Populating Remote menu. """

      def remote_action(q):
          if q.text() == "Connection to kRPC server":
              connection_window = ConnectionWindow(conn)
              connection_window.show()
      remote_menu.addAction("Connection to kRPC server")
      remote_menu.triggered[QAction].connect(remote_action)

      """ Populating status bar. """

      self.status_conn = StatusLabel("Not connected.")
      self.status_ut = StatusLabel("UT not synchronized.")
      self.status_bar = QStatusBar()
      self.status_bar.addWidget(self.status_conn)
      self.status_bar.addWidget(self.status_ut)
      self.objects['ut'].updated.connect(self._ut_updated)

      self.setStatusBar(self.status_bar)

      """ Define window layout. """

      self.setWindowTitle("Krocs")
      self.mdi = QMdiArea()
      self.setCentralWidget(self.mdi)

   """ Catch main window close event to close application. """
   def closeEvent(self, event):
       QCoreApplication.instance().quit()

   def _conn_synced(self):
       """ Updating view if new connection. """
       self.status_conn.setText("Connected to %s." % self.conn.addr)
       self.status_conn.setValid()

   def _conn_unsynced(self):
       """ Updating view if closed connection. """
       self.status_conn.setText("Not connected.")
       self.status_conn.setCritical()
       self.status_ut.setText("UT: Not synchronized.")
       self.status_ut.setCritical()

   def _ut_updated(self):
       """ Update view if UT changed. """
       self.status_ut.setText("UT: Y%02d/D%03d %d:%02d:%02d" %
       (int(self.objects['ut'].value) // 9203328,
       ((int(self.objects['ut'].value) // 21600000) % 42608) // 1000,
       (int(self.objects['ut'].value) // 3600) % 6,
       (int(self.objects['ut'].value) // 60) % 60,
       int(self.objects['ut'].value) % 60))
       self.status_ut.setValid()
