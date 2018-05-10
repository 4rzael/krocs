""" PyQt5 imports. """

from PyQt5.QtWidgets import (QMainWindow, QMdiSubWindow, QAction, QStatusBar,
QLabel, QMdiArea, QTextEdit)

from .basic_vessel_widget import BasicVesselWidget

""" Proprietary imports. """

class VesselWindow(QMainWindow):

    def __init__(self, conn, objects, vessel, parent = None):
        super(VesselWindow, self).__init__(parent)

        """ Connection object as attribute. """

        self.conn = conn
        self.objects = objects
        self.vessel = vessel

        self.widgets = {
            'general': {
                'basic': BasicVesselWidget
            }
        }

        self.bar_menus = {}

        """ Populating menu bar. """
        bar = self.menuBar()
        for menu in self.widgets.keys():
            self.bar_menus[menu] = bar.addMenu(menu)

            """ Populating Remote menu. """
            for name, widget in self.widgets[menu].items():
                action = self.bar_menus[menu].addAction(name)
                action.setCheckable(True)

                def spawn_mdi():
                    sub = BasicVesselWidget(self.conn, self.objects, self.vessel, parent = self)
                    self.mdi.addSubWindow(sub)
                    sub.show()
                    self.mdi.tileSubWindows()

                action.toggled.connect(spawn_mdi)

        """ Define window layout. """
        self.setWindowTitle(self.vessel.name)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
