# Let -- Parse tree node strategy for printing the special form let

from Tree import Nil
from Tree import Environment
from Print import Printer
from Special import Special

class Let(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printLet(t, n, p)

    def eval(self, exp, env):
        env2 = Environment(env)
        cdrCdr = exp.getCdr().getCdr()
        cdrCar = exp.getCdr().getCar()
        expLen = Special.util.length(exp)
        if expLen < 3:
            self._error('expression is invalid')
            return Nil.getInstance()
        expLen = Special.util.length(cdrCar)
        if expLen < 1:
            self._error('expression is invalid')
            return Nil.getInstance()
        if self.det(cdrCar, env, env2) < 0:
            self._error('expression is invalid')
            return Nil.getInstance()
        return Special.util.begin(cdrCdr, env2)

    def det(self, cdrCar, env, env2):
        #cdrCar tests
        if cdrCar.isNull():
            return 0
        cdCarCar = cdrCar.getCar()
        if Special.util.length(cdCarCar) != 2:
            return -1
        
        a = cdCarCar.getCar()
        b = cdCarCar.getCdr().getCar().eval(env)
        env2.define(a, b)
        return self.det(cdrCar.getCdr(), env, env2)