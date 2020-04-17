from math_module.calculations import MatrixTransformations
from PyQt5.QtGui import QPolygon, QPainter
from PyQt5.QtCore import QPoint, Qt, QPointF
from PyQt5.QtWidgets import QMainWindow
from display_module.active_list import ActiveList
from display_module.edge_table import EdgeTable
from display_module.edge_bucket import EdgeBucket
import sys
import numpy
import itertools

COLORS = ('black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 1024
        self.height = 768
        self.distance = 200
        self.zoom_step = 10

        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Virtual Camera")
        self.matrix_trans = MatrixTransformations()

        self.edge_table = EdgeTable()
        self.active_list = ActiveList()
        self.scanline = 0
        self.colors = itertools.cycle(COLORS)

    def paintEvent(self, event): 
        self.painter = QPainter(self)
        self.painter.translate(self.width/2, self.height/2)
        self.painter.scale(1, -1)
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


    def project_point(self, x, y, z):
        new_x = x * (self.distance / z)
        new_y = y * (self.distance / z)
        #return QPointF(new_x, new_y)
        return new_x, new_y, z
        

    
    def draw_rectangle(self, points):
        color = next(self.colors)
        for line in points:
            if(line[0][1] != line[1][1]):
                if(line[1][2] >= line[0][2]):
                    edge_bucket = EdgeBucket(line[0][0], line[0][1], line[1][0], line[1][1], line[1][2], self.set_color(color))
                else:
                    edge_bucket = EdgeBucket(line[0][0], line[0][1], line[1][0], line[1][1], line[0][2], self.set_color(color))
                self.edge_table.add_edge(edge_bucket)

            #self.painter.setPen(Qt.red)
            #self.painter.drawLine(line[0], line[1])


    def process_edge_table(self):
        self.scanline = self.edge_table.edges[0].yMin
        while len(self.edge_table.edges) != 0:
            if len(self.active_list.edges) != 0:
                edges_to_remove = []
                for edge in self.active_list.edges:
                    if(edge.yMax == self.scanline):
                        edges_to_remove.append(edge)

                for edge in edges_to_remove:
                    self.active_list.edges.remove(edge)
                    self.edge_table.edges.remove(edge)

            for edge in self.edge_table.edges:
                if edge.yMin == self.scanline:
                    self.active_list.add_edge(edge)

            self.edge_table.sort_edges()
            self.active_list.sort_edges()

            """for edge in self.active_list.edges:
                p1 = QPointF(edge.xMin, self.scanline)
                p2 = QPointF(edge.xMax, self.scanline)
                #print(p1, p2)
                self.painter.setPen(edge.color)
                self.painter.drawLine(p1, p2)
            """
            #print(len(self.active_list.edges))
            print(len(self.active_list.edges))
            for i in range(0, len(self.active_list.edges)):
                e1 = self.active_list.edges[i]
                if(i == (len(self.active_list.edges) - 1)):
                    e2 = self.active_list.edges[0]
                else:
                    e2 = self.active_list.edges[i+1]
                
                #e2 = self.active_list.edges[i+1]

                p1 = QPointF(e1.x, self.scanline)
                p2 = QPointF(e2.x, self.scanline)

                self.painter.setPen(e1.color)
                self.painter.drawLine(p1, p2)

            self.scanline = self.scanline + 1

            for edge in self.active_list.edges:
                if edge.slope != None:
                    edge.sum = edge.sum + edge.dX
                    while edge.sum >= edge.dY:
                        edge.x = edge.x + edge.sign * 1
                        edge.sum = edge.sum - edge.dY
            #self.active_list.sort_edges()


    def projection(self):
        #self.edge_table = EdgeTable()
        #self.active_list = ActiveList()
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

            #self.edge_table = EdgeTable()
            #self.active_list = ActiveList()
            self.draw_rectangle(points)
        self.process_edge_table()


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

    def set_color(self, color):
        if color == 'black':
            return Qt.black
        elif color == 'red':
            return Qt.red
        elif color == 'blue':
            return Qt.blue
        elif color == 'yellow':
            return Qt.yellow
        elif color == 'green':
            return Qt.green
        elif color == 'cyan':
            return Qt.cyan
        elif color == 'magenta':
            return Qt.magenta