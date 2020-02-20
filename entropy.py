import math
import numpy as np

class EntropyWindow:
    def __init__(self, data, window):
        self.data = data
        self.window = window

    def range(self):
        return range(len(self.data))

    def __getitem__(self, key):
        f = max(0, key - int(self.window / 2))
        n = min(len(self.data), f + self.window) - f
        hist,_ = np.histogram(self.data[f:f+n], bins=range(256), range=(0,255), density=True)
        en = -sum([ v * math.log(v, 2) if v != 0 else 0 for v in hist ])
        return en


class Entropy:
    def __init__(self, fname = None, data = None):
        if fname:
            with open(fname, 'r') as fd:
                self.data = np.fromfile(fd, dtype=np.uint8)
        else:
            self.data = np.array(data)

    def compute(self, window):
        return EntropyWindow(self.data, window)
