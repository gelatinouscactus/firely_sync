import math
import random

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import(QApplication, QGraphicsScene, QGraphicsView, QFrame, QGraphicsEllipseItem)
from PyQt5.QtGui import (QPainter, QPixmap, QRadialGradient)




class Firefly(QGraphicsView):
    def __init__(self, parent = None):
        super(Firefly, self).__init__(parent)

        self.scene = QGraphicsScene()
        self.fly = None

        self.setScene(self.scene)
        self.setupScene()

        
        self.timer_interval = 30
        timer = QTimer(self)
        timer.timeout.connect(self.animate)
        timer.setInterval(self.timer_interval)
        timer.start()

        self.freq_timer_int = 2000
        freq_timer = QTimer(self)
        freq_timer.timeout.connect(self.change_freq)
        freq_timer.setInterval(self.freq_timer_int)
        freq_timer.start()

        
        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameStyle(QFrame.NoFrame)


        self.angle = 0.0
        self.freq = 2   #freq of pulse in seconds
        self.omega = 5



    def setupScene(self):
        self.scene.setSceneRect(-300, -200, 600, 460)
        self.setBackgroundBrush(Qt.black)

        radialGrad = QRadialGradient(30, 30, 30)
        radialGrad.setColorAt(0, Qt.yellow)
        radialGrad.setColorAt(0.2, Qt.yellow)
        radialGrad.setColorAt(1, Qt.transparent)
        
        pixmap = QPixmap(60, 60)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(radialGrad)
        painter.drawEllipse(0, 0, 60, 60)
        painter.end()

        self.fly = self.scene.addPixmap(pixmap)
        self.fly.setZValue(2)


    def animate(self):
        self.angle += (math.pi / self.timer_interval)
        scale  = math.exp(self.omega*math.sin(self.freq*self.angle))/math.exp(self.omega)

        self.fly.setOpacity(scale)

        self.scene.update()



    def change_freq(self):
        self.freq = abs(random.gauss(0.75, 0.25))

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)

    firefly = Firefly()
    firefly.setWindowTitle('One pulsing firefly')
    firefly.resize(640, 480)
    firefly.show()

    sys.exit(app.exec_())
