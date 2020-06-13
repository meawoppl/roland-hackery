import cups
import tempfile
import subprocess



class RolandMill:
    def __init__(self):
        self.conn = cups.Connection()

        print('Searching for a roland mill')
        for pKey, pVal in self.conn.getPrinters().items():
            if (pKey.startswith('Roland')):
                print("Found: " + pKey)
                self.name = pKey
                self.prop = pVal
                return
        raise RuntimeError('No Roland Devices Found in '.format(self.conn.getPrinters().keys()) )

    def printText(self, text: str):
        with tempfile.tempfile() as path:
            with open(path, 'w') as f:
                f.write(text)
            return self.printFile(path)

    def printFile(self, filename: str):
        pass


RolandMill()


def fmt(n: float) -> str:
    return str(round(n, 2))


class RMDCommander:
    def __init__(self):
        self.script = ""
        self._append_raw('^DF')
        self._append_raw('!MC0')

    def _append_raw(self, string: str):
        self.script += string + ';\r\n'

    def speed(self, v: float):
        """
        """
        self._append_raw('V{}'.format(fmt(v)))

    def rel(self, x: float=0, y: float=0, z: float=0):
        self._append_raw('^PR')
        self._append_raw('Z{},{},{}'.format(fmt(x), fmt(y), fmt(z)))

    def emit(self):
        print(self.script)

    def run(self):
        with open('scratchy.txt', 'w') as f:
            f.write(self.script)
        
        subprocess.check_call(('lpr', 'scratchy.txt'))





def basic_run():
    cmd = RMDCommander()

    d = 500

    for v in range(2, 5):
        cmd.speed(v)
        cmd.rel(d, 0, 0)
        cmd.rel(-d, 0, 0)
        cmd.rel(0, +d, 0)
        cmd.rel(0, -d, 0)
        cmd.rel(0, 0, +d)
        cmd.rel(0, 0, -d)

    cmd.emit()
    cmd.run()