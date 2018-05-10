""" PyQt5 imports. """

from PyQt5.QtWidgets import (QWidget, QLabel, QFormLayout)

""" Proprietary imports. """

class BasicVesselWidget(QWidget):

   def __init__(self, conn, objects, vessel, parent = None):
      super(BasicVesselWidget, self).__init__(parent)

      """ Connection object as attribute. """

      self.conn = conn
      self.objects = objects
      self.vessel = vessel

      name_label = QLabel()
      name_label.setText(vessel.name)

      fbox = QFormLayout()
      fbox.addRow(name_label)

      self.setLayout(fbox)

      self.setMaximumSize(400, 300)
