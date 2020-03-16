from file_module.file_handler import FileHandler
from PyQt5.QtCore import QPoint


class MatrixTransformations:
    def __init__(self):
        file_handler = FileHandler()
        self.polygons = file_handler.read_file()


    def get_polygons(self):
        return self.polygons