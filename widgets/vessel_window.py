""" PyQt5 imports. """

from PyQt5.QtWidgets import (QAction, QStatusBar,
QLabel, QMdiArea)

""" Proprietary imports. """

class VesselWindow(QMdiSubWindow):

   def __init__(self, conn, objects, vessel, parent = None):
      super(VesselWindow, self).__init__(parent)

      """ Connection object as attribute. """

      self.conn = conn
      self.objects = objects
      self.vessel = vessel
      self.conn.connection_open.connect(self.connected)
      self.conn.connection_close.connect(self.closed)

      """ Populating menu bar. """
      bar = self.menuBar()
      info_menu = bar.addMenu("info")

      """ Populating Remote menu. """
      remote_menu.addAction("Widget 1")
#      remote_menu.triggered[QAction].connect(self.remoteaction)

      """ Define window layout. """
      self.setWindowTitle(self.vessel.name)
      self.mdi = QMdiArea()
      self.setCentralWidget(self.mdi)

   def connected(self):
       """ Updating view if new connection. """
       pass

   def closed(self):
       """ Updating view if closed connection. """
       pass
