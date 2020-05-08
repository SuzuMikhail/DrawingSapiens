from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dsbackend import dspyqt5

class DSpyqt5MainWindow(QMainWindow):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.color_dialog = None

        self.create_menus()
        self.setWindowTitle("啊~画笔的力量~集于一身")
        self.setCentralWidget(self.canvas)
        QCoreApplication.setAttribute(Qt.AA_CompressHighFrequencyEvents)
        

    def set_brush_color(self):
        if not self.color_dialog:
            # Under constructing
            self.color_dialog = QColorDialog(self)
            self.color_dialog.setModal(False)
            #self.color_dialog.setCurrentColor(self.canvas.color())
            self.color_dialog.setCurrentColor(self.canvas.color)
            #connect(self.color_dialog, QColorDialog.colorSelected, self.canvas, dspyqt5.setColor)
            #self.connect(self.color_dialog, QColorDialog.colorSelected, self.canvas, dspyqt5.setColor)
            #pyqtSignal().connect(self.color_dialog, QColorDialog.colorSelected, self.canvas, dspyqt5.setColor)
            #self.color_dialog.returnPressed.connect()
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
        filename = QFileDialog.getSaveFileName(self, self.tr("Save Picture"), path)
        success = self.canvas.save_image(filename)
        if not success:
            QMessageBox.information(self, "Error", "Could not save the image")
        return success

    def load(self):
        filename = QFileDialog.getOpenFileName(self, self.tr("Open file"), QDir.currentPath)
        if not self.canvas.load_image(filename):
            QMessageBox.information(self, "Error", "Could not load the image")

    def clear(self):
        pass

    def about(self):
        QMessageBox.about(self, tr("About"), tr("test"))

    def create_menus(self):
        filemenu = self.menuBar().addMenu(self.tr("&File"))
        """
        filemenu.addAction(self.tr("&Open"), self, self.load, QKeySequence.Open)
        filemenu.addAction(self.tr("&Save as"), self, self.save, QKeySequence.SaveAs)
        filemenu.addAction(self.tr("&New"), self, self.clear, QKeySequence.New)
        filemenu.addAction(self.tr("E&xit"), self, self.close, QKeySequence.Quit)
        """

        filemenu.addAction(self.tr("&Open"), self.load, QKeySequence.Open)
        filemenu.addAction(self.tr("&Save as"), self.save, QKeySequence.SaveAs)
        filemenu.addAction(self.tr("&New"), self.clear, QKeySequence.New)
        filemenu.addAction(self.tr("E&xit"), self.close, QKeySequence.Quit)
        

        brush_menu = self.menuBar().addMenu(self.tr("&Brush"))
        brush_menu.addAction(self.tr("&Brush Color"), self.set_brush_color, self.tr("Ctrl+B"))
        