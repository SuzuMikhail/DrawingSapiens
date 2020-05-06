from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DSpyqt5Backend(QWidget):
    def __init__(self, parent=None):
        super(DSpyqt5Backend, self).__init__(parent)
        self.pen_is_down = False
        self.pen_x = 0
        self.pen_y = 0
        self.pen_pressure = 0
        self.text = ""

        self.pevent_called_times = 0

        self.resize(640, 480)
        self.setWindowTitle("画 图 人")

    def tabletEvent(self, tevent):
        self.pen_x = tevent.globalX()
        self.pen_y = tevent.globalY()
        self.pen_pressure = int(tevent.pressure() * 100)

        print(tevent.PointerType)
        print(tevent.TabletDevice)

        if tevent.type() == QTabletEvent.TabletPress:
            self.pen_is_down = True
            self.text = "TabletPress"
        elif tevent.type() == QTabletEvent.TabletMove:
            self.pen_is_down = True
            self.text = "TabletMove"
        elif tevent.type() == QTabletEvent.TabletRelease:
            self.pen_is_down = False
            self.text = "TabletRelease"

        self.text += " at x={0}, y={1}, pressure={2}%,".format(self.pen_x,
                                                              self.pen_y,
                                                              self.pen_pressure)

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
        text = self.text
        i = text.find("\n\n")
        
        if i >= 0:
            text = text.left(i)
        
        qp = QPainter()
        qp.begin(self)
        qp.setFont(QFont('SimHei', 40))
        qp.drawText(self.rect(), Qt.AlignTop | Qt.AlignLeft, text)
        qp.end()


