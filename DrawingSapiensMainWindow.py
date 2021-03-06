import pyglet
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from dsbackend.dspyglet import DSpygletBackend
from dsbackend.dspyqt5 import DSpyqt5Backend
import DSpyqt5MainWindow
import DSTabletApplication


class DSStartupCheck:
    def __init__(self):
        self.PYGLET_BACKEND = 0
        self.PYQT5_BACKEND = 1

    def tablet_detector(self):
        tablets = pyglet.input.get_tablets()
        
        if tablets:
            print("Tablet detected")
            for t in enumerate(tablets):
                print(t.name)
        else:
            print("Tablet are not detected")

    def backend_switcher(self):
        #i = self.PYGLET_BACKEND
        i = self.PYQT5_BACKEND
        
        if i is self.PYGLET_BACKEND:
            print("Launching pyglet backend")
            b = DSpygletBackend()
            b.run()
        elif i is self.PYQT5_BACKEND:
            print("pyqt5 is under constructing")
            #app = DSTabletApplication.TabletApplication(sys.argv, sys.args)
            app = DSTabletApplication.TabletApplication(sys.argv)
            canvas = DSpyqt5Backend()
            win = DSpyqt5MainWindow.DSpyqt5MainWindow(canvas)

            app.setCanvas(canvas)

            win.resize(800, 600)
            win.show()
            app.exec()
        else:
            print("No backend have been chosed.")

        

DSStartupCheck().backend_switcher()