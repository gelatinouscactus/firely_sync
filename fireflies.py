from math import *
from random import *
from time import sleep


from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView)
from PyQt5.QtGui import (QPixmap, QPainter, QRadialGradient)
from PyQt5.QtCore import (qrand, qsrand, Qt, QTime, QTimer, QRectF, QLineF, QPointF)


speed_mod = 1

class Firefly(QGraphicsItem):

    MaxDist = 300 # distance from center before the fireflies turn around
    
    def __init__(self, freq=0.125, speed=10, angle=0.0, phase=0.0, size = 60.0, stim = None):
        super().__init__()

        self.freq = freq
        self.speed = speed
        self.angle = angle
        self.scale = 0.0
        self.omega = 10/self.freq
        self.phase = phase
        self.size = size
        
        self.timer_interval = 1000/33
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(self.timer_interval)
        

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)


    @staticmethod
    def normalizeAngle(angle):
        while angle < 0:
            angle += 2*pi
        while angle > 2*pi:
            angle -= 2*pi
        return angle
    

    def paint(self, painter, option, widget):
        
        radialGrad = QRadialGradient(self.size/2, self.size/2, self.size )
        radialGrad.setColorAt(0, Qt.yellow)
        radialGrad.setColorAt(0.2, Qt.yellow)
        radialGrad.setColorAt(1, Qt.transparent)

        #pixmap = QPixmap(60, 60)
        #pixmap.fill(Qt.transparent)

        #painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(radialGrad)
        painter.drawEllipse(0, 0, self.size, self.size)
        #painter.end()

        
    def timerEvent(self):
        #implement movement, pulsing here
        self.phase += (self.timer_interval/1000)
        
        self.setOpacity(exp(self.omega*sin(self.freq*2*pi*self.phase))/exp(self.omega))


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
                
        v = self.speed
        self.speed += (-v/2 + qrand() % v)/v
        self.setPos(self.mapToParent(0, -(speed_mod + sin(self.speed)*speed_mod)))
#        self.setPos(self.mapToParent(0, -self.speed))
#        self.setPos(self.x()+dx, self.y()+dy)
        self.setRotation(self.rotation() + self.angle)


        
if __name__ == '__main__':
    import sys

    FlyCount = 25

    app = QApplication(sys.argv)
    qsrand(QTime(0, 0, 0,).secsTo(QTime.currentTime()))

    scene = QGraphicsScene()
    scene.setSceneRect(-300, -300, 600, 600)
    scene.setItemIndexMethod(QGraphicsScene.NoIndex)

    targ = None
    for i in range(FlyCount):
        random_speed = (-50 + qrand()%100)/1000
        random_angle = qrand()%(2*pi)
        random_x = (-150 + qrand()%300)
        random_y = (-150 + qrand()%300)
        random_phase = random()*4*pi
        fly = Firefly(angle=random_angle, phase = random_phase, size = 30)
        fly.setPos(random_x, random_y)
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
