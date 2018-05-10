from ..vessel_window import VesselWindow
from PyQt5.QtWidgets import QMainWindow

class VesselsMenu(object):
    def __init__(self, window, vessels, bar):
        self.window = window
        self.vessels = vessels
        self.bar = bar
        self.menu = self.bar.addMenu('Vessels')

        self.vessel_windows = {}

        def vessels_updated(vessels):
            self.menu.clear()
            for vessel in vessels:
                action = self.menu.addAction(vessel.name)
                action.setCheckable(True)
                action.toggled.connect(lambda *args: self.on_vessel_click(action, vessel))
        self.vessels.updated.connect(vessels_updated)


    def on_vessel_click(self, action, vessel):
        if vessel in self.vessel_windows.keys():
            self.on_vessel_deselection(action, vessel)
        else:
            self.on_vessel_selection(action, vessel)

    def on_vessel_selection(self, action, vessel):
        self.vessel_windows[vessel] = VesselWindow(
            self.window.conn,
            self.window.objects,
            vessel,
            self.window
        )
        self.vessel_windows[vessel].show()


    def on_vessel_deselection(self, action, vessel):
        self.window.mdi.removeSubWindow(self.vessel_windows[vessel])
        del self.vessel_windows[vessel]
