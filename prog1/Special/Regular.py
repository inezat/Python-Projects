# Regular -- Parse tree node strategy for printing regular lists

import sys
from Special import Special
from Tree import *

class Regular(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        if p == False:
            sys.stdout.write("(")
        #Nil.getInstance()
        t.getCar().print(0)
        if not t.getCdr().isNull():
            sys.stdout.write(" ")
        t.getCdr().print(0, True)
