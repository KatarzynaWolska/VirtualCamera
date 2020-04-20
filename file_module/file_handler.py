import json
from numpy import array
from display_module.wall import Wall
import itertools

class FileHandler:
    def __init__(self):
        self.filepath = './file_module/config_file.json'
        self.read_file()
        self.colors = itertools.cycle(self.file_data['colors'])

    def read_file(self):
        with open(self.filepath) as f:
            self.file_data = json.load(f)

        """walls = []        
        for data in self.file_data['polygons']:
            color = next(self.colors)
            wall = Wall(color)
            points = array()
            for point in data:
                points.append(point)"""
            
            
        return array(self.file_data['polygons'])

    def get_colors(self):
        with open(self.filepath) as f:
            self.file_data = json.load(f)
            
        return self.file_data['colors']