from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DSpyqt5MainWindow(QMainWindow):
    def __init__(self, canvas):
        self.canvas = canvas
        self.color_dialog = None

        self.create_menus()
        self.setWindowTitle("啊~画笔的力量~集于一身")
        self.setCentralWidget(self.canvas)
        QCoreApplication.setAttribute(Qt.AA_CompressHighFrequencyEvents)
        

    def set_brush_color(self):
        pass

    def set_alpha_valuator(self, action):
        pass

    def set_line_width_valuator(self, action):
        pass

    def set_saturation_valuator(self, action):
        pass

    def set_event_compression(self, compress):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def clear(self):
        pass

    def about(self):
        pass

    def create_menus(self):
        filemenu = menuBar().addMenu(tr("&File"))
        filemenu.addAction(tr("&Open"), self, self.load, QKeySequence.Open)
        filemenu.addAction(tr("&Save as"), self, self.save, QKeySequence.SaveAs)
        filemenu.addAction(tr("&New"), self, self.clear, QKeySequence.New)
        filemenu.addAction(tr("E&xit"), self, self.close, QKeySequence.Quit)

        brush_menu = menuBar().addMenu(tr("&Brush"))
        brush_menu.addAction(tr("&Brush Color"), this, self.set_brush_color, tr("Ctrl+B"))
        