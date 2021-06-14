# If -- Parse tree node strategy for printing the special form if

from Tree import BoolLit
from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class If(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printIf(t, n, p)

    def eval(self, exp, env):
        size = Special.util.length(exp)
        comp = exp.getCdr().getCar()
        evtrue = exp.getCdr().getCdr().getCar()
        if size == 4:
            evfalse = exp.getCdr().getCdr().getCdr().getCar()
        else:
            evfalse = Nil.getInstance()
        if comp.eval(env) == BoolLit.getInstance(True):
            return evtrue.eval(env)
        elif size == 3:
            return Nil.getInstance()
        return evfalse.eval(env)