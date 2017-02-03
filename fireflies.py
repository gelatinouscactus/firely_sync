from math import *
import random

from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView)
from PyQt5.QtGui import (QPixmap, QPainter, QRadialGradient)
from PyQt5.QtCore import (qrand, qsrand, Qt, QTime, QTimer, QRectF, QLineF, QPointF)

class Firefly(QGraphicsItem):

    MaxDist = 150 # distance from center before the fireflies turn around

    def __init__(self, freq=1.0, speed=0.1, angle=0.0, phase=0.0):
        super().__init__()

        self.freq = freq
        self.speed = speed
        self.angle = angle
        self.scale = 0.0
        self.omega = 1
        self.phase = phase

        
        self.timer_interval = 1000/33
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(self.timer_interval)


    def boundingRect(self):
        return QRectF(0, 0, 60, 60)


    @staticmethod
    def normalizeAngle(angle):
        while angle < 0:
            angle += 2*pi
        while angle > 2*pi:
            angle -= 2*pi
        return angle
    

    def paint(self, painter, option, widget):

        
        radialGrad = QRadialGradient(30, 30, 30)
        radialGrad.setColorAt(0, Qt.yellow)
        radialGrad.setColorAt(0.2, Qt.yellow)
        radialGrad.setColorAt(1, Qt.transparent)

        #pixmap = QPixmap(60, 60)
        #pixmap.fill(Qt.transparent)

        #painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(radialGrad)
        painter.drawEllipse(0, 0, 60, 60)
        #painter.end()


    def timerEvent(self):
        #implement movement, pulsing here
        self.phase += (pi / self.timer_interval)
        self.scale = exp(self.omega*sin(self.freq*self.angle))/exp(self.omega)
        self.setOpacity(exp(self.omega*sin(self.freq*self.phase))/exp(self.omega))

        #linetocenter
        ltc = QLineF(QPointF(0, 0,), self.mapFromScene(0, 0))

        if ltc.length() > Firefly.MaxDist:
            #angle to center
            atc = acos(ltc.dx() / ltc.length())

            if ltc.dy() < 0:
                atc = 2*pi - atc
            atc = Firefly.normalizeAngle((pi - atc) + pi / 2)

            if atc < pi and atc > pi / 4:
                #rotate left
                self.angle += [-0.25, 0.25][self.angle < -pi/2]

            elif atc >= pi and atc < (pi + pi/2 + pi/4):
                #rotate right
                self.angle += [-0.25, 0.25][self.angle < pi/2]

        elif sin(self.angle) < 0:
            self.angle += 0.25
        elif sin(self.angle) > 0:
            self.angle -= 0.25
                
        dist = self.speed * self.timer_interval
        dx = dist*cos(self.angle)
        dy = dist*sin(self.angle)
        dt = sin(self.angle)*10

        
        self.speed += (-50 + qrand() % 100)/100.0
        self.setPos(self.mapToParent(0, -(3 + sin(self.speed)*3)))
#        self.setPos(self.mapToParent(0, -self.speed))
#        self.setPos(self.x()+dx, self.y()+dy)
        self.setRotation(self.rotation() + self.angle)


        
if __name__ == '__main__':
    import sys

    FlyCount = 15

    app = QApplication(sys.argv)
    qsrand(QTime(0, 0, 0,).secsTo(QTime.currentTime()))

    scene = QGraphicsScene()
    scene.setSceneRect(-300, -300, 600, 600)
    scene.setItemIndexMethod(QGraphicsScene.NoIndex)

    for i in range(FlyCount):
        random_speed = (-50 + qrand()%100)/1000
        random_angle = (-pi + qrand()%(2*pi))/2*pi
        random_freq =  (0.25 + (qrand()%100)/100)
        fly = Firefly(speed=random_speed, angle=random_angle, freq=random_freq, phase = random_angle)
        fly.setPos(sin((i*2*pi) / FlyCount)*200,
                            cos((i*2*pi) / FlyCount) * 200)
        scene.addItem(fly)

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.setBackgroundBrush(Qt.black)
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.setDragMode(QGraphicsView.ScrollHandDrag)
    view.setWindowTitle('Fireflies')
    view.resize(600, 800)
    view.show()

    sys.exit(app.exec_())
