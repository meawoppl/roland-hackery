import cups
import tempfile
import os
import time
import subprocess
import pprint



def fmt(n: float) -> str:
    return str(round(n, 2))


UNITS_PER_MM = 100

def cvt(val: float):
    return int(round(val * UNITS_PER_MM, 0))


class RMDCommander:
    def __init__(self, taskName=""):
        self.taskName = taskName
        self.script = ""
        self._append_raw('^DF')
        self._append_raw('!MC0')

    def _append_raw(self, string: str):
        print('Adding Command: ' + string)
        self.script += string + ';\r\n'

    def _append_format(self, string: str, *args):
        self._append_raw(string.format(*args))

    def speed(self, v: float):
        """
        Set the maximum speed of 2d and 3d moves in mm/second
        """
        self._append_format('F{:.1}', v)
        self._append_format('V{:.1}', v)
        self._append_format('VS{:.1}', v)
        
    def dwell(self, timeMs: float):
        assert timeMs > 0 and timeMs < 32767, timeMs
        self._append_format('W{:.0f}', int(timeMs))

    def absXY(self, x: float, y: float):
        self._append_format("PA {}, {}", cvt(x), cvt(y))

    def absXYZ(self, x: float, y: float):
        self._append_raw('PA')
        self._append_format('Z{},{},{}', cvt(x), cvt(y), cvt(z))

    def relXY(self, x: float, y:float):
        self.relXYZ(x, y, 0.0)

    def relXYZ(self, x: float=0, y: float=0, z: float=0):
        self._append_raw('PR')
        self._append_format('Z{},{},{}', cvt(x), cvt(y), cvt(z))

    def spindleOn(self, speed: float):
        assert speed > 100 and speed < 10000, speed
        self._append_format("!RC {:.0f}", speed)
        self._append_raw("!MC1")

    def spindleOff(self):
        self._append_raw("!MC0")


    def getOutput(self):
        return self.script



class RolandMill:
    def __init__(self):
        self.conn = cups.Connection()

        print('Searching for a roland mill')
        for pKey, pVal in self.conn.getPrinters().items():
            if (pKey.startswith('Roland')):
                print("Found: " + pKey)
                self.name = pKey
                self.prop = pVal
                self.cancelPending()
                return
        raise RuntimeError('No Roland Devices Found in '.format(self.conn.getPrinters().keys()) )

    def cancelPending(self):
        self.conn.cancelAllJobs(uri=self.prop['device-uri'])


    def _printText(self, text: str, taskName: str):
        with tempfile.NamedTemporaryFile('w') as f:
            f.write(text)
            f.flush()
            return self._printFile(f.name, taskName)

    def _printFile(self, filename: str, taskName: str):
        assert os.path.exists(filename)
        return self.conn.printFile(self.name, filename, taskName, {})

    def runCommand(self, cmd: RMDCommander):
        return self._printText(cmd.getOutput(), cmd.taskName)

    def waitUntilDone(self):
        cmd = RMDCommander('WaitTask')
        cmd.dwell(10)
        waitJobID = self.runCommand(cmd)
        done = False
        while not done:
            results = self.conn.getJobAttributes(waitJobID)
            done = results['time-at-completed'] != None
            print("Waiting on job finish")
            pprint.pprint(results)
            if not done:
                time.sleep(1)



import numpy as np

def xyPlane(xyMin: tuple, xyMax: tuple, toolSize: float):
    # Determine the number of passes
    # Compute the x starting points
    # move to 
    # ^Y move to x

    halfTool = toolSize / 2
    xMin, yMin = (v + halfTool for v in xyMin) 
    xMax, yMax = (v - halfTool for v in xyMax) 

    dx = xMax - xMin
    dy = yMax - yMin

    cmd = RMDCommander()
    cmd.speed(2.0)

    # Box out the move to avoid leaving tails later
    cmd.absXY(xMin, yMin)
    cmd.absXY(xMax, yMin)    
    cmd.absXY(xMax, yMax)
    cmd.absXY(xMin, yMax)
    cmd.absXY(xMin, yMin)

    # Compute the line offsets to work in
    passes = int(np.ceil(dx / toolSize))
    offsets = np.linspace(xyMin[0], xyMax[0], passes)
    for n, xOffset in enumerate(offsets):
        if n % 2 == 0:
            cmd.absXY(xOffset, yMin)
            cmd.relXY(0.0, dy)
        else:
            cmd.absXY(xOffset, yMax)
            cmd.relXY(0.0, -dy)

    return cmd

mill = RolandMill()
cmd = xyPlane((-30, -30), (30, 30), 9.5)
mill.runCommand(cmd)
mill.waitUntilDone()

# mill = RolandMill()
# cmd = RMDCommander()
# cmd.absXY(-100, -100)

# mill.runCommand(cmd)
# mill.waitUntilDone()


def fun():
    d = 500

    for v in range(2, 5):
        cmd.speed(v)
        cmd.relXYZ(d, 0, 0)
        cmd.relXYZ(-d, 0, 0)
        cmd.relXYZ(0, +d, 0)
        cmd.relXYZ(0, -d, 0)
        cmd.relXYZ(0, 0, +d)
        cmd.relXYZ(0, 0, -d)
import math



def circle_test():
    r = 10
    x0 = r
    y0 = 0

    cmd = RMDCommander()
    cmd.spindleOn(2000)
    cmd.speed(0.5)

    for t in np.linspace(0, 2 * np.pi, 93):
        dx = r * np.cos(t)
        dy = r * np.sin(t)  
        cmd.relXY(x0 - dx, y0 - dy)
        x0 = dx
        y0 = dy

    cmd.spindleOff()

    job = mill.runCommand(cmd)
    mill.waitUntilDone()
