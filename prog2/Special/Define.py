# Define -- Parse tree node strategy for printing the special form define

from Tree import Ident
from Tree import Nil
from Tree import Cons
#from Tree import Void
from Print import Printer
from Special import Special

class Define(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printDefine(t, n, p)

    def eval(self, exp, env):
        size = Special.util.length(exp)
        vname = exp.getCdr().getCar()
        #simple define, eg. (define x 5), (define x '(list))
        if vname.isSymbol() and size == 3:
            definition = exp.getCdr().getCdr().getCar()
            env.define(vname, definition.eval(env))
            return Nil.getInstance()
        #complex define, eg. defining functions
        #needs lambda, which I think needs Closure
        fname = vname.getCar()
        definition = vname.getCdr()
        rest = exp.getCdr().getCdr()
        fun = Cons(Ident('lambda'), Cons(definition, rest))
        env.define(fname, fun.eval(env))
        return Nil.getInstance()
