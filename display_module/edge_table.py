class EdgeTable:
    def __init__(self):
        self.edges = []

    def sort_order(self, ed):
        return ed.yMin

    def add_edge(self, edge):
        self.edges.append(edge)
        #self.edges.sort(key=lambda e: (-e.z, e.yMin))
        #print("----")
        #for e in self.edges:
        #    print(e.yMin)

    def sort_edges(self):
        self.edges.sort(key=lambda e: (-e.z, e.yMin))