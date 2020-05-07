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
        self.brush = self.color
        self.pen = QPen(self.brush, 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        self.resize(800, 600)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_TabletTracking)

    def tabletEvent(self, tevent):
        if tevent.type() == QTabletEvent.TabletPress:
            if not self.pen_is_down:
                self.pen_is_down = True
                self.event2last_point(tevent)
                self.text = "TabletPress"
        elif tevent.type() == QTabletEvent.TabletMove:
            if self.pen_is_down:
                self.updateBrush(tevent)
                painter = QPainter(self.pixmap)
                self.paint_pixmap(painter, tevent)
                self.event2last_point(tevent)
                self.text = "TabletMove"
        elif tevent.type() == QTabletEvent.TabletRelease:
            if self.pen_is_down and tevent.buttons() is Qt.NoButton:
                self.pen_is_down = False
            self.update()

        if self.pen_is_down:
            self.text += " Pen is down"
        else:
            self.text += " Pen is up"

        print(self.text)

        self.pevent_called_times += 1
        print(self.pevent_called_times)

        tevent.accept()
        #self.update()

    def paintEvent(self, event):
        if self.pixmap.isNull():
            self.init_pixmap()

        qp = QPainter(self)
        print('darwing')
        dpr = self.devicePixelRatioF()
        pixmap_portion = QRect(event.rect().topLeft() * dpr,
                               event.rect().size() * dpr)
        qp.drawPixmap(event.rect().topLeft(), self.pixmap, pixmap_portion)
        #qp.end()

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
        maxPenRadius = self.pressureToWidth(1.0)
        painter.setRenderHint(QPainter.Antialiasing)
        
        device = event.device()

        if device is QTabletEvent.Airbrush:
            painter.setPen(Qt.NoPen)
            grad = QRadialGradient(self.last_point.pos, self.pen.widthF() * 10.0)
            color = self.brush.color()
            color.setAlphaF(color.alphaF() * 0.25)
            grad.setColorAt(0, self.brush.color())
            grad.setColorAt(0.5, Qt.transparent)
            painter.setBrush(grad)
            radius = grad.radius()
            painter.drawEllipse(event.posF(), radius, radius)
            self.update(QRect(event.pos() - QPoint(radius, radius), QSize(radius * 2, radius * 2)))
        elif device is QTabletEvent.RotationStylus:
            self.brush.setStyle(Qt.SolidPattern)
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.brush)
            poly = QPolygonF()
            halfWidth = self.pressureToWidth(self.last_point.pressure)
            brushAdjust = QPointF(qSin(qDegressToRadians(-self.last_point.rotation)) * halfWidth,
                                  qCos(qDegressToRadians(-self.last_point.rotation)) * halfWidth)
            
            poly << self.last_point.pos + brushAdjust
            poly << self.last_point.pos - brushAdjust

            halfWidth = self.pen.widthF()
            brushAdjust = QPointF(qSin(qDegressToRadians(-event.rotation())) * halfWidth,
                                  qCos(qDegressToRadians(-event.rotation())) * halfWidth)

            poly << event.posF() - brushAdjust
            poly << event.posF() + brushAdjust
            painter.drawConvexPolygon(poly)
            self.update(poly.boundingRect.toRect())
        else:
            painter.setPen(Qt.NoPen)
            painter.drawLine(self.last_point.pos, event.posF())
            self.update(QRect(self.last_point.pos.toPoint(), event.pos().normalized()
                        .adjusted(-maxPenRadius, -maxPenRadius, maxPenRadius, maxPenRadius)))
                
    def brushPattern(self, value):
        pass

    def updateBrush(self, event):
        hue, saturation, value, alpha = None
        self.color.getHsv(hue, saturation, value, alpha)

        vValue = int(((event.yTlit() + 60.0) / 120.0) * 255)
        hValue = int(((event.xTlit() + 60.0) / 120.0) * 255)

        v = self.alphaChannelValuator
        if v is Valuator.PressureValuator:
            self.color.setAlphaF(event.pressure())
        elif v is Valuator.TangentialPressureValuator:
            if event.device() is QTabletEvent.Airbrush:
                self.color.setAlphaF(max(0.01, (event.tangentialPressure() + 1.0) / 2.0))
            else
                self.color.setAlpha(255)
        elif v is Valuator.TiltValuator:
            self.color.setAlpha(max(abs(vValue - 127), abs(hValue - 127)))
        else:
            self.color.setAlpha(255)

        v = self.colorSaturationValuator
        if v is Valuator.VTiltValuator:
            self.color.setHsv(hue, vValue, value, alpha)
        elif v is Valuator.HTiltValuator:
            self.color.setHsv(hue, hValue, value, alpha)
        elif v is Valuator.PressureValuator:
            self.color.setHsv(hue, int(event.pressure() * 255.0), value, alpha)
        else:
            pass

        v = self.lineWidthValuator
        if v is Valuator.PressureValuator:
            self.pen.setWidthF(pressureToWidth(event.pressure()))
        elif v is Valuator.TiltValuator:
            self.pen.setWidthF(max(abs(vValue - 127), abs(hValue - 127)) / 12)
        else:
            self.pen.setWidthF(1)

        if event.pointerType() is QTabletEvent.Eraser:
            self.brush.setColor(Qt.white)
            self.pen.setColor(Qt.white)
            self.pen.setWidthF(event.pressure() * 10 + 1)
        else:
            self.brush.setColor(self.color)
            self.pen.setColor(self.color)



    def updateCursor(self, event):
        pass

