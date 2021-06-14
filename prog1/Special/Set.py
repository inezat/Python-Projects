# Set -- Parse tree node strategy for printing the special form set!
import sys
from Special import Special

class Set(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass
    
    def print(self, t, n, p):
        if p == False:
            sys.stdout.write("(set!")
        #t.getCar().print(0)
        if not t.getCdr().isNull():
            sys.stdout.write(" ")
        t.getCdr().print(0, True)

