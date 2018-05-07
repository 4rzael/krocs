""" PyQt5 imports. """

from PyQt5.QtWidgets import (QMainWindow, QAction, QStatusBar,
QLabel, QMdiArea)

""" Proprietary imports. """

from connection_window import ConnectionWindow

class MainWindow(QMainWindow):

   def __init__(self, conn, parent = None):
      super(MainWindow, self).__init__(parent)

      """ Connection object as attribute. """

      self.conn = conn
      self.conn.connection_open.connect(self.connected)
      self.conn.connection_close.connect(self.closed)

      """ Populating menu bar. """

      bar = self.menuBar()
      remote = bar.addMenu("Remote")

      """ Populating file menu. """

      remote.addAction("Connection to kRPC server")
      remote.triggered[QAction].connect(self.remoteaction)

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
