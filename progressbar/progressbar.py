#!/usr/bin/python
#Filename : progressbar.py

import time, os

class ProgressBar():
    """docstring for progressbar"""
    def __init__(self, width=50):
        self.pointer = 0
        self.width = width

    def __call__(self, x):
        # x in percent
        self.pointer = int(self.width*(x/100.0))
        return "|" + "#"*self.pointer + "-"*(self.width-self.pointer)+\
            "|\n %d percent done" % int(x)

if __name__ == '__main__':
    pb = ProgressBar()
    for i in range(101):
        # os.system('clear')
        print pb(i)
        time.sleep(0.1)
