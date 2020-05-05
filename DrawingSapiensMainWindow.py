import pyglet
from dsbackend.dspyglet import DSpygletBackend

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
        i = self.PYGLET_BACKEND

        if i is self.PYGLET_BACKEND:
            print("Launching pyglet backend")
            pygletb = DSpygletBackend()
            pygletb.run()
        elif i is self.PYQT5_BACKEND:
            print("pyqt5 is under constructing")
        else:
            print("No backend have been chosed.")

DSStartupCheck().backend_switcher()