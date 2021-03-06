#!/usr/bin/env python3
""" Python imports. """

import sys
import signal

""" PyQt5 imports. """

from PyQt5.QtWidgets import QApplication

""" Other external library imports. """

import krpc

""" Proprietary imports. """

from widgets import MainWindow
from objects import Connection

def window():
   app = QApplication(sys.argv)
   conn = Connection()

   win = MainWindow(conn)

   win.show()
   sys.exit(app.exec_())

if __name__ == "__main__":
   """ Catch Ctrl^C in console mod. """
   signal.signal(signal.SIGINT, signal.SIG_DFL)

   window()
