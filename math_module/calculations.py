from file_module.file_handler import FileHandler
from PyQt5.QtCore import QPoint
import numpy
import math


class MatrixTransformations:
    def __init__(self):
        file_handler = FileHandler()
        self.polygons = file_handler.read_file()
        self.step = 10
        self.angle_step = math.pi / 30


    def get_polygons(self):
        return self.polygons


    def move(self, tx, ty, tz):
        matrix = numpy.array([
                [1, 0, 0, tx * self.step],
                [0, 1, 0, ty * self.step],
                [0, 0, 1, tz * self.step],
                [0, 0, 0, 1]])
        self.calculate_matrix(matrix)

    
    def rotate(self, axis, direction):
        angle = self.angle_step * direction
        if axis == 'x':
            matrix = numpy.array([
                [1, 0, 0, 0],
                [0, math.cos(angle), -1 * math.sin(angle), 0],
                [0, math.sin(angle), math.cos(angle), 0],
                [0, 0, 0, 1]])
        elif axis == 'y':
            matrix = numpy.array([
                [math.cos(angle), 0, math.sin(angle), 0],
                [0, 1, 0, 0],
                [-1 * math.sin(angle), 0, math.cos(angle), 0],
                [0, 0, 0, 1]])
        elif axis == 'z':
            matrix = numpy.array([
                [math.cos(angle), -1 * math.sin(angle), 0, 0],
                [math.sin(angle), math.cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
        self.calculate_matrix(matrix)


    def calculate_matrix(self, matrix):
        new_polygons = None
        for polygon in self.polygons:
            new_coords = None
            for coords in polygon:
                coords = numpy.append(coords, [1])
                result = numpy.matmul(matrix, coords)
                result = numpy.delete(result, 3, axis=None)
                new_coords = numpy.concatenate((new_coords, [result]), axis=0) if new_coords is not None else [result]
            new_polygons = numpy.concatenate((new_polygons, [new_coords]), axis=0) if new_polygons is not None else [new_coords]
        self.polygons = new_polygons
        #print("Polygons")
        #print(new_polygons)