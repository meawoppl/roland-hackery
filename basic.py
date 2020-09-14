from pyroland.cmd import RMDCommander
from pyroland.mill import RolandMill


import numpy as np


class EnhancedCommand(RMDCommander):
    def fillInside(self, xyMin: tuple, xyMax: tuple, toolSize: float, zHeight: float):
        halfTool = toolSize / 2
        xyMin = (v + halfTool for v in xyMin) 
        xyMax = (v - halfTool for v in xyMax) 

        # Box out the move to avoid leaving tails later
        self.fillRect(xyMin, xyMax, toolSize, zHeight)

    def fillRect(self, xyMin: tuple, xyMax: tuple, toolSize: float, zHeight: float):
        # Determine the number of passes
        # Compute the x starting points
        # move to 
        # ^Y move to x

        xMin, yMin = xyMin 
        xMax, yMax = xyMax

        dx = xMax - xMin
        dy = yMax - yMin
        
        # Box out the move to avoid leaving tails later
        self.strokeRect(xyMin, xyMax, zHeight)

        # Compute the line offsets to work in
        passes = int(np.ceil(dx / (toolSize*0.9)))
        offsets = np.linspace(xMin, xMax, passes)
        for n, xOffset in enumerate(offsets):
            if n % 2 == 0:
                self.absXYZ(xOffset, yMin, zHeight)
                self.absXYZ(xOffset, yMax, zHeight)
            else:
                self.absXYZ(xOffset, yMax, zHeight)
                self.absXYZ(xOffset, yMin, zHeight)

    def strokeRect(self, xyMin: tuple, xyMax: tuple, zHeight: float):
        xMin, yMin = xyMin 
        xMax, yMax = xyMax 

        self.absXY(xMin, yMin)
        self.absXYZ(xMin, yMin, zHeight)    
        self.absXYZ(xMax, yMin, zHeight)    
        self.absXYZ(xMax, yMax, zHeight)
        self.absXYZ(xMin, yMax, zHeight)
        self.absXYZ(xMin, yMin, zHeight)

    def strokeInside(self, xyMin: tuple, xyMax: tuple, toolSize: float, zHeight: float):
        # Determine the number of passes
        # Compute the x starting points
        # move to 
        # ^Y move to x

        halfTool = toolSize / 2
        xyMin = (v + halfTool for v in xyMin) 
        xyMax = (v - halfTool for v in xyMax) 

        # Box out the move to avoid leaving tails later
        self.strokeRect(xyMin, xyMax, zHeight)



mill = RolandMill()

def cutting_board_outline():
    edge_min = (-190, -290)
    edge_max = (151, 105)
    bit_size = 9.5 - 1.63
    cmd = EnhancedCommand()
    with cmd.cutting_context(10000, 40):
        for z in np.linspace(-58, -86, 30):
            cmd.strokeInside(edge_min, edge_max, bit_size, z)
        cmd.liftZ()

    mill.runCommand(cmd)
    mill.waitUntilDone()

# Rounded inlay
def inlay():
    edge_min = (-170, -270)
    edge_max = (131, 85)
    bit_size = 9.5 - 1.63
    z = -56
    cmd = EnhancedCommand()
    with cmd.cutting_context(10000, 40):
        cmd.strokeInside(edge_min, edge_max, bit_size, z)
        cmd.liftZ()

    mill.runCommand(cmd)
    mill.waitUntilDone()


def face():
    bit_size = 9.5

    edge_min = (-200.895, -290.585)
    edge_max = (130.105, 95.415)

    cmd = EnhancedCommand()
    cmd.liftZ()
    with cmd.cutting_context(10000, 20):
        for zHeight in [-44.5]:
            cmd.fillRect(edge_min, edge_max, bit_size, zHeight)
    
    mill.runCommand(cmd)


def pockets():
    bit_size = 9.5

    edge_min = (-205.895, -295.585)
    edge_max = (135.105, 99.415)

    edge_min = tuple(v + 30 for v in edge_min)
    edge_max = tuple(v - 30 for v in edge_max)

    x1, x2, x3, x4 = np.linspace(edge_min[0], edge_max[0], 4)
    y1, y2, y3, y4 = np.linspace(edge_min[1], edge_max[1], 4)

    cmd = EnhancedCommand()
    with cmd.cutting_context(10000, 40):
        for z in np.linspace(-50, -75, 10):
            cmd.liftZ()
            cmd.fillRect((x1, y1), (x4, y2), bit_size, z)

            cmd.liftZ()
            cmd.fillRect((x1, y3), (x4, y4), bit_size, z)

            cmd.liftZ()
            cmd.fillRect((x1, y2-5), (x2, y3+5), bit_size, z)

            cmd.liftZ()
            cmd.fillRect((x3, y2-5), (x4, y3+5), bit_size, z)

    mill.runCommand(cmd)

pockets()