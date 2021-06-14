# Quote -- Parse tree node strategy for printing the special form quote

import sys
from Special import Special
from Tree import Nil

class Quote(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        sys.stdout.write("'")
        t.getCdr().print(0,True)
