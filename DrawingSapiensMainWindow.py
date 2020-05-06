import pyglet
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from dsbackend.dspyglet import DSpygletBackend
from dsbackend.dspyqt5 import DSpyqt5Backend


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
            app = QApplication(sys.argv)
            b = DSpyqt5Backend()
            b.show()

            app.exec()
        else:
            print("No backend have been chosed.")

        

DSStartupCheck().backend_switcher()