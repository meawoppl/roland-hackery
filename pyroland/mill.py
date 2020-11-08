import cups
import tempfile
import os
import time
import subprocess
import pprint


from pyroland.cmd import RMDCommander

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
        return self._printText(cmd.get_output(), cmd.taskName)

    def waitUntilDone(self):
        cmd = RMDCommander('WaitTask')
        cmd.dwell(10)
        waitJobID = self.runCommand(cmd)
        done = False
        while not done:
            results = self.conn.getJobAttributes(waitJobID)
            if (results['job-state-reasons'] == "printer-stop"):
                raise Exception("Mill disabled.")
            done = results['time-at-completed'] != None
            print("Waiting on job finish")
            print("Job State", results['job-state'], "reason:", results['job-state-reasons'])
            # pprint.pprint(results)
            if not done:
                time.sleep(1)

