from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dsbackend import dspyqt5

class DSpyqt5MainWindow(QMainWindow):
    def __init__(self, canvas):
        self.canvas = canvas
        self.color_dialog = None

        self.create_menus()
        self.setWindowTitle("啊~画笔的力量~集于一身")
        self.setCentralWidget(self.canvas)
        QCoreApplication.setAttribute(Qt.AA_CompressHighFrequencyEvents)
        

    def set_brush_color(self):
        if not self.color_dialog:
            self.color_dialog = QColorDialog(self)
            self.color_dialog.setModal(false)
            self.color_dialog.setCurrentColor(self.canvas.color())
            connect(self.color_dialog, QColorDialog.colorSelected, self.canvas, dspyqt5.setColor)
        self.color_dialog.setVisible(True)

    def set_alpha_valuator(self, action):
        self.canvas.set_alpha_valuator(action.data().value())

    def set_line_width_valuator(self, action):
        pass

    def set_saturation_valuator(self, action):
        pass

    def set_event_compression(self, compress):
        pass

    def save(self):
        path = QDir.currentPath() + "/Untitled.png"
        filename = QFileDialog.getSaveFileName(self, tr("Save Picture"), path)
        success = self.canvas.save_image(filename)
        if not success:
            QMessageBox.information(self, "Error", "Could not save the image")
        return success

    def load(self):
        filename = QFileDialog.getOpenFileName(this, tr("Open file"), QDir.currentPath)
        if not self.canvas.load_image(filename):
            QMessageBox.information(self, "Error", "Could not load the image")

    def clear(self):
        pass

    def about(self):
        QMessageBox.about(self, tr("About"), tr("test"))

    def create_menus(self):
        filemenu = menuBar().addMenu(tr("&File"))
        filemenu.addAction(tr("&Open"), self, self.load, QKeySequence.Open)
        filemenu.addAction(tr("&Save as"), self, self.save, QKeySequence.SaveAs)
        filemenu.addAction(tr("&New"), self, self.clear, QKeySequence.New)
        filemenu.addAction(tr("E&xit"), self, self.close, QKeySequence.Quit)

        brush_menu = menuBar().addMenu(tr("&Brush"))
        brush_menu.addAction(tr("&Brush Color"), this, self.set_brush_color, tr("Ctrl+B"))
        