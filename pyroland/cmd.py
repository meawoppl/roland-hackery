from contextlib import contextmanager

def fmt(n: float) -> str:
    return str(round(n, 2))


UNITS_PER_MM = 100

def cvt(val: float):
    return int(round(val * UNITS_PER_MM, 0))

SEP = ';\r\n'

class ComposableCommand:
    def __init__(self, taskName="", lines=[]):
        self.taskName = taskName
        self.lines = list(lines)

        self.feed_set = False
        self.speed_set = False

    def _append_raw(self, string: str):
        print('Adding Command: ' + string)
        self.lines.append(string)

    def _append_format(self, string: str, *args):
        self._append_raw(string.format(*args))

    def __add__(self, second):
        assert isinstance(second, self.__class__)
        summed = ComposableCommand(
            "Sum({},{})".format(self.taskName, second.taskName),
            self.lines + second.lines)
        summed.feed_set = self.feed_set | second.feed_set
        summed.speed_set = self.speed_set | second.speed_set
        return summed

    def get_output(self, default=True):
        preamble = []
        if default:
            preamble = ['^DF', '!MC0']

        return SEP.join(preamble + self.lines) 


class RMDCommander(ComposableCommand):
    def set_feed(self, v: float):
        """
        Set the maximum speed of 2d and 3d moves in mm/second
        """
        self._append_format('F{:.1f}', v)
        self._append_format('V{:.1f}', v)
        self._append_format('VS{:.1f}', v)
        self.feed_set = True

    def set_speed(self, speed: float):
        assert speed > 100 and speed <= 10000, speed
        self._append_format("!RC{:.0f}", speed)
        self.speed_set =  True

    def require_speeds_and_feeds_set(self):
        assert(self.speed_set)
        assert(self.feed_set)

    def dwell(self, timeMs: float):
        assert timeMs > 0 and timeMs < 32767, timeMs
        self._append_format('W{:.0f}', int(timeMs))

    def absXY(self, x: float, y: float):
        self._append_format("^PA;D{},{}", cvt(x), cvt(y))

    def absXYZ(self, x: float, y: float, z: float):
        self._append_format('^PA;Z{},{},{}', cvt(x), cvt(y), cvt(z))

    def relXY(self, x: float, y:float):
        self._append_format('^PR;Z{},{},0', cvt(x), cvt(y))

    def relXYZ(self, x: float, y: float, z: float):
        self._append_format('^PR;Z{},{},{}', cvt(x), cvt(y), cvt(z))

    def spindle_on(self):
        self._append_raw("!MC1")

    def spindle_off(self):
        self._append_raw("!MC0")

    def liftZ(self):
        self.relXYZ(0, 0, 1000)

    @contextmanager
    def cutting_context(self, speed=None, feed=None):
        if(speed is not None):
            self.set_speed(speed)
        if(feed is not None):
            self.set_feed(feed)
        self.spindle_on()
        try:
            yield
        finally:
            self.spindle_off()

