import json
import numpy
from numpy import array
from display_module.wall import Wall
import itertools

class FileHandler:
    def __init__(self):
        self.filepath = './file_module/file2.json'
        self.read_file()


    def read_file(self):
        with open(self.filepath) as f:
            self.file_data = json.load(f)
        
        colors = itertools.cycle(self.file_data['colors'])
        walls = []        
        for data in self.file_data['polygons']:
            color = next(colors)
            wall = Wall(color)
            points = []
            for point in data:
                points.append(point)
            
            points = numpy.array(points)
            wall.set_points(points)
            walls.append(wall)

        return walls


    def get_colors(self):
        with open(self.filepath) as f:
            self.file_data = json.load(f)
            
        return self.file_data['colors']