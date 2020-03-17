from file_module.file_handler import FileHandler
from PyQt5.QtCore import QPoint
import numpy


class MatrixTransformations:
    def __init__(self):
        file_handler = FileHandler()
        self.polygons = file_handler.read_file()
        self.step = 10


    def get_polygons(self):
        return self.polygons


    def move(self, tx, ty, tz): # UPROSCIC !!!!!!!!!!!!!!!
        matrix = numpy.array([
                [1, 0, 0, tx * self.step],
                [0, 1, 0, ty * self.step],
                [0, 0, 1, tz * self.step],
                [0, 0, 0, 1]])
        new_polygons = None
        for polygon in self.polygons:
            new_coords = None
            for coords in polygon:
                coords = numpy.append(coords, [1])
                result = numpy.matmul(matrix, numpy.array(coords))
                result = numpy.delete(result, 3, axis=None)
                new_coords = numpy.concatenate((new_coords, [result]), axis=0) if new_coords is not None else [result]
            new_polygons = numpy.concatenate((new_polygons, [new_coords]), axis=0) if new_polygons is not None else [new_coords]
        self.polygons = new_polygons
