from math_module.calculations import MatrixTransformations
from file_module.file_handler import FileHandler
from PyQt5.QtGui import QPolygon, QPainter, QPainterPath, QPolygonF, QBrush, QColor
from PyQt5.QtCore import QPoint, Qt, QPointF
from PyQt5.QtWidgets import QMainWindow
import sys
import numpy
import itertools


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 1024
        self.height = 768
        self.distance = 200
        self.zoom_step = 20

        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Virtual Camera")
        self.matrix_trans = MatrixTransformations()
        file_handler = FileHandler()
        self.colors = itertools.cycle(file_handler.get_colors())
        self.rectangles = []


    def paintEvent(self, event): 
        self.painter = QPainter(self)
        #self.painter.translate(self.width/2, self.height/2)
        #self.painter.scale(1, -1)
        self.painter.setPen(Qt.black)
        self.projection()
        self.painter.end()


    def zoom(self, direction):
        self.distance = self.distance + direction * self.zoom_step


    def keyPressEvent(self, event):
        pressedKey = event.key()
        if pressedKey == Qt.Key_A:
            self.matrix_trans.move(1, 0, 0)
        elif pressedKey == Qt.Key_D:
            self.matrix_trans.move(-1, 0, 0)
        elif pressedKey == Qt.Key_W:
            self.matrix_trans.move(0, -1, 0)
        elif pressedKey == Qt.Key_S:
            self.matrix_trans.move(0, 1, 0)
        elif pressedKey == Qt.Key_C:
            self.matrix_trans.move(0, 0, 1)
        elif pressedKey == Qt.Key_V:
            self.matrix_trans.move(0, 0, -1)
        elif pressedKey == Qt.Key_Q:
            self.matrix_trans.rotate('x', 1)
        elif pressedKey == Qt.Key_E:
            self.matrix_trans.rotate('x', -1)
        elif pressedKey == Qt.Key_T:
            self.matrix_trans.rotate('y', 1)
        elif pressedKey == Qt.Key_Y:
            self.matrix_trans.rotate('y', -1)
        elif pressedKey == Qt.Key_Z:
            self.matrix_trans.rotate('z', 1)
        elif pressedKey == Qt.Key_X:
            self.matrix_trans.rotate('z', -1)
        elif pressedKey == Qt.Key_O:
            self.zoom(1)
        elif pressedKey == Qt.Key_P:
            self.zoom(-1)
        event.accept()
        self.repaint()


    def get_color(self, color):
        if color == 'blue':
            return Qt.blue
        elif color == 'red':
            return Qt.red
        elif color == 'yellow':
            return Qt.yellow
        elif color == 'green':
            return Qt.green


    def project_point(self, x, y, z):
        new_x = x * (self.distance / z)
        new_y = y * (self.distance / z)
        #return QPointF(new_x, new_y)
        return new_x, new_y, z

    
    def draw_rectangle(self, points):
        color = next(self.colors)
        self.painter.setPen(self.get_color(color))
        
        path = QPainterPath()
        polygon = QPolygonF()

        for line in points:
            polygon.append(QPointF(self.width / 2 + line[0][0], self.height / 2 -  line[0][1]))
            polygon.append(QPointF(self.width / 2 + line[1][0], self.height / 2 -  line[1][1]))
            
        path.addPolygon(polygon)
        self.painter.drawPath(path)
        self.painter.fillPath(path, QBrush(QColor(color)))


    def draw_rectangles(self):
        for rectangle, z in self.rectangles:
            self.draw_rectangle(rectangle)
    

    def add_rectangle(self, points):
        """if points[0][0][2] > points[0][1][2]:
            min_z = points[0][1][2]
        else:
            min_z = points[0][0][2]

        for i in range(1, len(points)):
            if points[i][0][2] < min_z:
                min_z = points[i][0][2]

            if points[i][1][2] < min_z:
                min_z = points[i][1][2]"""
        
        avg_z = 0
        for point in points:
            avg_z += (point[0][2] + point[1][2]) / 2
        
        self.rectangles.append((points, avg_z))


    def projection(self):
        self.rectangles = []
        polygons = self.matrix_trans.get_polygons()
        for j in range(0, len(polygons)):
            points = []
            coords = polygons[j]
            for i in range(0, len(coords)):
                point1 = coords[i]
                if i == (len(coords) - 1):
                    point2 = coords[0]
                else:
                    point2 = coords[i+1]

                res = self.prepare_points(point1, point2)    

                if res != None:
                    points.append(res)

            self.add_rectangle(points)
            #self.draw_rectangle(points)

        self.rectangles.sort(key=self.sort_order)
        self.draw_rectangles()

    
    def sort_order(self, rect):
        """points = rect[0]
        if points[0][0][0] < points[0][1][0]:
            min_x = points[0][0][0]
        else:
            min_x = points[0][1][0]

        if points[0][0][1] < points[0][1][1]:
            min_y = points[0][0][1]
        else:
            min_y = points[0][1][1]

        for i in range(1, len(points)):
            if points[i][0][0] < min_x:
                min_x = points[i][0][0]
            if points[i][1][0] < min_x:
                min_x = points[i][1][0]
            
            if points[i][0][1] < min_y:
                min_y = points[i][0][1]
            if points[i][1][1] < min_y:
                min_y = points[i][1][1]"""

        avg_x = 0
        avg_y = 0
        for points in rect[0]:
            avg_x += (points[0][0] + points[1][0]) / 2
            avg_y += (points[0][1] + points[1][1]) / 2

        return -abs(rect[1]), -abs(avg_x), -abs(avg_y)


    def prepare_points(self, point1, point2):
        if point1[2] < 1 and point2[2] < 1:
            return None
        
        res = None

        if point1[2] < 1:
            direction = numpy.array(point2 - point1)

            res = self.intersection(direction, point1)
            
            proj_point1 = self.project_point(res[0], res[1], res[2])
            proj_point2 = self.project_point(point2[0], point2[1], point2[2])

        elif point2[2] < 1:
            direction = numpy.array(point1 - point2)

            res = self.intersection(direction, point2)

            proj_point1 = self.project_point(point1[0], point1[1], point1[2])
            proj_point2 = self.project_point(res[0], res[1], res[2])

        else:    
            proj_point1 = self.project_point(point1[0], point1[1], point1[2])
            proj_point2 = self.project_point(point2[0], point2[1], point2[2])

        return (proj_point1, proj_point2)


    def intersection(self, direction, point):
        epsilon=1e-6
        planeNormal = numpy.array([0, 0, 1])
        planePoint = numpy.array([0, 0, 1])

        rayPoint = numpy.array([point[0], point[1], point[2]])

        ndotu = planeNormal.dot(direction) 

        if abs(ndotu) < epsilon:
            return None

        w = rayPoint - planePoint
        si = -planeNormal.dot(w) / ndotu
        Psi = w + si * direction + planePoint
        return Psi

