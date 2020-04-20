class Wall:
    def __init__(self, color):
        self.points = []
        self.color = color

    def add_point(self, point):
        self.points.append(point)

    def set_points(self, points):
        self.points = points