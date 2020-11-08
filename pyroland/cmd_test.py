from unittest import TestCase

import numpy as np

import pyroland.cmd


class CmdTests(TestCase):
    def test_basic(self):
        cmd = pyroland.cmd.RMDCommander()
    
    def test_normal(self):
        cmd = pyroland.cmd.RMDCommander()

        d = 10
        cmd.set_feed(15)
        cmd.relXYZ(d, 0, 0)
        cmd.relXYZ(-d, 0, 0)
        cmd.relXYZ(0, +d, 0)
        cmd.relXYZ(0, -d, 0)
        cmd.relXYZ(0, 0, +d)
        cmd.relXYZ(0, 0, -d)

    def test_cut_context(self):
        cmd = pyroland.cmd.RMDCommander()

        with cmd.cutting_context(1000, 20):
            cmd.absXYZ(0, 1, 0)
        
        results = cmd.getOutput()
        lines = results.split(pyroland.cmd.SEP)
        print(lines)
        self.assertEqual(lines[-1], "!MC0")
        self.assertIn("!MC1", lines)

    def test_circle_cut(self):
        r = 10
        x0 = r
        y0 = 0
        
        cmd = pyroland.cmd.RMDCommander()
        cmd.spindle_on()
        cmd.set_speed(2000)
        cmd.set_feed(0.5)
        for t in np.linspace(0, 2 * np.pi, 93):
            dx = r * np.cos(t)
            dy = r * np.sin(t)  
            cmd.relXY(x0 - dx, y0 - dy)
            x0 = dx
            y0 = dy
            cmd.spindle_off()

    def test_aggregation(self):
        cmd = pyroland.cmd.RMDCommander()
        cmd.spindle_on()
        cmd.set_speed(2000)
        cmd.set_feed(0.5)

        for t in np.linspace(0, 2 * np.pi, 93):
            dx = np.cos(t)
            dy = np.sin(t)  
        
        agg = cmd + cmd

        self.assertEqual(len(cmd.lines) * 2, len(agg.lines) )