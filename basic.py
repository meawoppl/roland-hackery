import subprocess


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