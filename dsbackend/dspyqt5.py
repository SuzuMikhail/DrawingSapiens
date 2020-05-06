from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DSpyqt5Backend(QWidget):
    class Point():
        def __init__(self, parent=None):
            self.pos = QPointF()
            self.pressure = 0
            self.rotation = 0

    def __init__(self, parent=None):
        super(DSpyqt5Backend, self).__init__(parent)
        self.pen_is_down = False
        self.pen_x = 0
        self.pen_y = 0
        self.pen_pressure = 0

        self.last_point = self.Point()

        self.pevent_called_times = 0

        self.resize(800, 600)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_TabletTracking)

    def event2last_point(self, tevent):
        self.last_point.pos = tevent.posF()
        self.last_point.pressure = tevent.pressure()
        self.last_point.rotation = tevent.rotation()
        print(self.last_point.pos, self.last_point.pressure, self.last_point.rotation)
        

    def tabletEvent(self, tevent):
        """
        self.pen_x = tevent.globalX()
        self.pen_y = tevent.globalY()
        self.pen_pressure = int(tevent.pressure() * 100)
        """

        if tevent.type() == QTabletEvent.TabletPress:
            self.pen_is_down = True
            self.event2last_point(tevent)
            self.text = "TabletPress"
        elif tevent.type() == QTabletEvent.TabletMove:
            self.pen_is_down = True
            self.event2last_point(tevent)
            self.text = "TabletMove"
        elif tevent.type() == QTabletEvent.TabletRelease:
            self.pen_is_down = False
            self.text = "TabletRelease"

        #self.text += " at x={0}, y={1}, pressure={2}%,".format(self.pen_x,
         #                                                     self.pen_y,
          #                                                    self.pen_pressure)


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
        print('darwing')
        qp.setBackground(Qt.white)
        #qp.setPen(Qt.NoPen)
        qp.setBrush(Qt.black)
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        #qp.drawPoint(self.pen_x, self.pen_y)
        #qp.drawRect(self.pen_x, self.pen_y, 20, 20)
        #qp.drawEllipse(self.pen_x, self.pen_y, 20, 20)
        qp.drawEllipse(self.last_point.pos, 20, 20)
        #qp.end()


