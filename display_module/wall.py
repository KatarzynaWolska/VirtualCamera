class Wall:
    def __init__(self, color):
        self.edges = []
        self.color = color
    
    def add_edge(self, edge):
        self.edges.append(edge)