from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class TabletApplication(QApplication):
    def __init__(self):
        self.canvas = None

    def event(self, event):
        t = event.type()
        if t is QEvent.TabletEnterProximity or t is QEvent.TabletLeaveProximity:
            self.canvas.setTabletDevice(event)
            return True
        return QApplication.event(event)

    def setCanvas(self, canvas):
        self.canvas = canvas