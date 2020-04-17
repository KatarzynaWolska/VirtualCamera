class ActiveList:
    def __init__(self):
        self.edges = []

    def sort_order(self, ed):
        return ed.x

    def add_edge(self, edge):
        self.edges.append(edge)
        #self.edges.sort(key=lambda e: (-e.z, e.x))

        #print("----")
        #for e in self.edges:
        #    print(e.x)

    def sort_edges(self):
        self.edges.sort(key=lambda e: (-e.z, e.x))
