import math, random

from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView)
from PyQt5.QtGui import (QPixmap, QPainter, QRadialGradient)
from PyQt5.QtCore import (qrand, qsrand, Qt, QTime, QTimer, QRectF)

class Firefly(QGraphicsItem):
    Pi = math.pi
    Tau = 2*Pi


    def __init__(self):
        super().__init__()

        self.freq = 1.0
        self.speed = 0.0
        self.angle = 0.0
        self.scale = 0.0
        self.omega = 1

        self.timer_interval = 30
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(self.timer_interval)


    def boundingRect(self):
        return QRectF(0, 0, 60, 60)


    def paint(self, painter, option, widget):

        
        radialGrad = QRadialGradient(30, 30, 30)
        radialGrad.setColorAt(0*self.scale, Qt.yellow)
        radialGrad.setColorAt(0.2*self.scale, Qt.yellow)
        radialGrad.setColorAt(1*self.scale, Qt.transparent)

        #pixmap = QPixmap(60, 60)
        #pixmap.fill(Qt.transparent)

        #painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(radialGrad)
        painter.drawEllipse(0, 0, 60, 60)
        #painter.end()


    def timerEvent(self):
        #implement movement, pulsing here
        self.angle += (Firefly.Pi / self.timer_interval)
        self.scale = math.exp(self.omega*math.sin(self.freq*self.angle))/math.exp(self.omega)

        self.update()


if __name__ == '__main__':
    import sys

    FlyCount = 4

    app = QApplication(sys.argv)
    qsrand(QTime(0, 0, 0,).secsTo(QTime.currentTime()))

    scene = QGraphicsScene()
    scene.setSceneRect(-300, -300, 600, 600)
    scene.setItemIndexMethod(QGraphicsScene.NoIndex)

    for i in range(FlyCount):
        fly = Firefly()
        fly.setPos(math.sin((i*Firefly.Tau) / FlyCount)*200,
                            math.cos((i*Firefly.Tau) / FlyCount) * 200)
        scene.addItem(fly)

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.setBackgroundBrush(Qt.black)
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    view.setDragMode(QGraphicsView.ScrollHandDrag)
    view.setWindowTitle('Colliding Mice')
    view.resize(400, 300)
    view.show()

    sys.exit(app.exec_())
B
