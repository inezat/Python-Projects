# Regular -- Parse tree node strategy for printing regular lists

from Tree import Nil
from Print import Printer
from Special import Special

class Regular(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printRegular(t, n, p)

    def eval(self, exp, env):
        fname = exp.getCar().eval(env)
        #list elements following fname are eval via mapeval in util
        lstele = Special.util.mapeval(exp.getCdr(), env)
        return fname.apply(lstele)