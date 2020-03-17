from math_module.calculations import MatrixTransformations
from PyQt5.QtGui import QPolygon, QPainter
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 1024
        self.height = 768
        self.distance = 150

        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Virtual Camera")
        self.matrix_trans = MatrixTransformations()
        #self.projection()


    def paintEvent(self, event): 
        self.painter = QPainter(self)
        #self.painter.translate(0, self.height)
        #self.painter.scale(1, -1)
        self.painter.setPen(Qt.black)
        self.projection()
        self.painter.end()


    def keyPressEvent(self, event):
        pressedKey = event.key()
        if pressedKey == Qt.Key_A:
            self.matrix_trans.move(-1, 0, 0)
        elif pressedKey == Qt.Key_D:
            self.matrix_trans.move(1, 0, 0)
        elif pressedKey == Qt.Key_W:
            self.matrix_trans.move(0, -1, 0)
        elif pressedKey == Qt.Key_S:
            self.matrix_trans.move(0, 1, 0)
        event.accept()
        self.repaint()


    def project_point(self, x, y, z):
        new_x = x * (self.distance / z)
        new_y = y * (self.distance / z)
        #new_x = self.width / 2 + (self.distance * x / z)
        #new_y = self.height / 2 - (self.distance * y / z)
        return QPoint(new_x, new_y)


    def draw_rectangle(self, points):
        for i in range(0, len(points)):
            if i == (len(points) - 1):
                self.painter.drawLine(points[i], points[0])
            else:
                self.painter.drawLine(points[i], points[i+1])


    def projection(self):
        polygons = self.matrix_trans.get_polygons()

        i = 0
        for polygon in polygons:
            #if i == 0:
            points = []
            for coords in polygon:
                points.append(self.project_point(coords[0], coords[1], coords[2]))

            self.draw_rectangle(points)
            i = i + 1