class EdgeBucket:
    def __init__(self, x1, y1, x2, y2, z, color):
        self.z = z
        self.color = color
        if(y1 > y2):
            self.yMin = y2
            self.yMax = y1
            self.x = x2
        elif (y2 > y1):
            self.yMin = y1
            self.yMax = y2
            self.x = x1
        else:
            self.yMin = y1
            self.yMax = y1
            self.x = x2 #hmmmm
        
        if(x1 > x2):
            self.xMin = x2
            self.xMax = x1
        elif (x2 > x1):
            self.xMin = x1
            self.xMax = x2
        else:
            self.xMin = x1
            self.xMax = x1
        
        if(x2 == x1):
            self.slope = None
        else:
            self.slope = (y2 - y1) / (x2 - x1)
    
        if(self.slope == None):
            self.sign = None
        elif(self.slope > 0):
            self.sign = 1
        elif(self.slope < 0):
            self.sign = -1
        elif(self.slope == 0):
            self.sign = 0
        
        self.dX = abs(x1 - x2)
        self.dY = abs(y1 - y2)
        self.sum = 0
    
