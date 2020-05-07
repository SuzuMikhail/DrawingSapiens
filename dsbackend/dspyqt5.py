from enum import Enum

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DSpyqt5Backend(QWidget):
    class Point():
        def __init__(self, parent=None):
            self.pos = QPointF()
            self.pressure = 0
            self.rotation = 0

    class Valuator(Enum):
        PressureValuator = auto()
        TangentialPressureValuator = auto()
        TiltValuator = auto()
        VTiltValuator = auto()
        HTiltValuator = auto()
        NoValuator = auto()

    def __init__(self, parent=None):
        super(DSpyqt5Backend, self).__init__(parent)
        self.pen_is_down = False
        self.last_point = self.Point()

        self.pevent_called_times = 0

        self.alphaChannelValuator = Valuator.TangentialPressureValuator
        self.colorSaturationValuator = Valuator.NoValuator
        self.lineWidthValuator = Valuator.PressureValuator

        self.color = Qt.red
        self.pixmap = QPixmap()
        self.brush = None
        self.pen = None

        self.resize(800, 600)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_TabletTracking)

    def tabletEvent(self, tevent):
        if tevent.type() == QTabletEvent.TabletPress:
            self.pen_is_down = True
            self.event2last_point(tevent)
            self.text = "TabletPress"
        elif tevent.type() == QTabletEvent.TabletMove:
            self.pen_is_down = True
            painter = QPainter(self.pixmap)
            self.paint_pixmap(painter, tevent)
            self.event2last_point(tevent)
            self.text = "TabletMove"
        elif tevent.type() == QTabletEvent.TabletRelease:
            self.pen_is_down = False
            self.text = "TabletRelease"

        if self.pen_is_down:
            self.text += " Pen is down"
        else:
            self.text += " Pen is up"

        print(self.text)

        self.pevent_called_times += 1
        print(self.pevent_called_times)
        tevent.accept()
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        #qp.begin(self)
        if self.pixmap.isNull():
            self.init_pixmap()
        
        print('darwing')
        pixmap_portion = QRect(event.rect().topLeft() * 2,
                               event.rect().size() * 2)
        qp.drawPixmap(event.rect().topLeft(), self.pixmap, pixmap_portion)
        qp.end()

    def resizeEvent(self, event):
        pass




    def init_pixmap(self):
        dpr = self.devicePixelRatioF()
        new_pixmap = QPixmap(qRound(self.width() * dpr), qRound(self.height() * dpr))
        new_pixmap.setDevicePixelRatio(dpr)
        new_pixmap.fill(Qt.white)

        print('init_pixmap')

        painter = QPainter(new_pixmap)
        if not self.pixmap.isNull():
            painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        self.pixmap = new_pixmap
    

    def save_image(self, file):
        return self.pixmap.save(file)

    def load_image(self, file):
        success = self.pixmap.load(file)
        if success:
            self.update()
            return True
        return False

    def clear(self):
        pass

    def setAlphaChannelValuator(self, t):
        self.alphaChannelValuator = t

    def setColorSaturationValuator(self, t):
        self.colorSaturationValuator = t

    def setLineWidthType(self, t):
        self.lineWidthValuator = t
    
    def setColor(self, c):
        if c.isVaild():
            self.color = c

    def color(self):
        return self.color

    def setTabletDevice(self, event):
        self.updateCursor(event)



    def event2last_point(self, tevent):
        self.last_point.pos = tevent.posF()
        self.last_point.pressure = tevent.pressure()
        self.last_point.rotation = tevent.rotation()
        print(self.last_point.pos, self.last_point.pressure, self.last_point.rotation)
        
    def paint_pixmap(self, painter, event):
        painter.setRenderHint(QPainter.Antialiasing)
        
        device = event.device()

        if device is QTabletEvent.Airbrush:
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(event.posF(), 20, 20)
            self.update(QRect(event.pos() - QPoint(20, 20), QSize(40, 40)))
        elif device is QTabletEvent.RotationStylus:
            print("rotationStylus")
        else:
            painter.setPen(Qt.NoPen)
            painter.drawLine(self.last_point.pos, event.posF())
            #update(QRect(self.last_point.pos.toPoint(), event.pos()).normalized().adjusted())
            self.update()
            #print("unknown devices")
    
    def brushPattern(self, value):
        pass

    def updateBrush(self, event):
        pass

    def updateCursor(self, event):
        pass

