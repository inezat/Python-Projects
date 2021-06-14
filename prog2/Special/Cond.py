# Cond -- Parse tree node strategy for printing the special form cond

from Tree import BoolLit
from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class Cond(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printCond(t, n, p)

    def eval(self, exp, env):
        return self.modeval(exp.getCdr(), env)

    #Due to potential arbitrary number of conditionals, we need to strip the Cond node via exp.getCdr() before doing eval
    def modeval(self, exp, env):
        condition = exp.getCar().getCar()
        rest = exp.getCar().getCdr()
        #when we hit the else condition, we need to eval regardless
        if condition.isSymbol() and condition.getName() == 'else':
            return Special.util.begin(rest, env)
        #figure out what the eval is for our condition
        #if true we run the bit in front of us
        #if false, recursively call eval on cdr(exp), which should be the cons with next condition
        condeval = condition.eval(env)
        if condeval == BoolLit.getInstance(True):
            if rest.getCar().isSymbol():
                return Special.util.begin(rest, env)
            return Special.util.begin(rest, env)
        return self.modeval(exp.getCdr(), env)
