import json
from numpy import array


class FileHandler:
    def __init__(self):
        self.filepath = './file_module/config_file.json'
        self.read_file()


    def read_file(self):
        with open(self.filepath) as f:
            self.file_data = json.load(f)
            
        return array(self.file_data['polygons'])