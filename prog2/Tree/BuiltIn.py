# BuiltIn -- the data structure for built-in functions

# Class BuiltIn is used for representing the value of built-in functions
# such as +.  Populate the initial environment with
# (name, BuiltIn(name)) pairs.

# The object-oriented style for implementing built-in functions would be
# to include the Python methods for implementing a Scheme built-in in the
# BuiltIn object.  This could be done by writing one subclass of class
# BuiltIn for each built-in function and implementing the method apply
# appropriately.  This requires a large number of classes, though.
# Another alternative is to program BuiltIn.apply() in a functional
# style by writing a large if-then-else chain that tests the name of
# the function symbol.

import sys
from Parse import *
from Tree import Node
from Tree import BoolLit
from Tree import IntLit
from Tree import StrLit
from Tree import Ident
from Tree import Nil
from Tree import Cons
from Tree import TreeBuilder
#from Tree import Unspecific

class BuiltIn(Node):
    env = None
    util = None

    @classmethod
    def setEnv(cls, e):
        cls.env = e

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def __init__(self, s):
        self.symbol = s                 # the Ident for the built-in function

    def getSymbol(self):
        return self.symbol

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Built-In Procedure ")
        if self.symbol != None:
            self.symbol.print(-abs(n) - 1)
        sys.stdout.write('}')
        if n >= 0:
            sys.stdout.write('\n')
            sys.stdout.flush()

    # TODO: The method apply() should be defined in class Node
    # to report an error.  It should be overridden only in classes
    # BuiltIn and Closure.
    def apply(self, args):
        #figure out size of args, then figure out what to do from there
        size = BuiltIn.util.length(args)
        if size > 2:
            self._error("wrong number of arguments")
        if size == 0:
            return self.__apply0()
        if size == 1:
            return self.__apply1(args.getCar())
        return self.__apply2(args.getCar(), args.getCdr().getCar())

    ## The easiest way to implement BuiltIn.apply is as an
    ## if-then-else chain testing for the different names of
    ## the built-in functions.

    def __apply0(self):
        name = self.symbol.getName()

        if name == 'read':
            scanner = Scanner(sys.stdin)
            builder = TreeBuilder()
            parser = Parser(scanner, builder)
            root = parser.parseExp()
            if root != None:
                return tree
            
        elif name == 'newline':
            sys.stdout.write('\n')
            sys.stdout.flush()
            return Nil.getInstance()

        if name == 'interaction-environment':
            return BuiltIn.env

        self._error("invalid builtin function call for " + name)
        return Nil.getInstance()

    def __apply1(self, arg):
        name = self.symbol.getName()

        if name == 'symbol?':
            return BoolLit.getInstance(arg.isSymbol())

        elif name == ' number?':
            return BoolLit.getInstance(arg.isNumber())

        elif name == 'car':
            return arg.getCar()

        elif name == 'cdr':
            return arg.getCdr()

        elif name == 'null?':
            return BoolLit.getInstance(arg.isNull())

        elif name == 'pair':
            return BoolLit.getInstance(arg.isPair())

        elif name == 'procedure?':
            return BoolLit.getInstance(arg.isProcedure())

        elif name == 'write':
            arg.print(0)
            return Nil.getInstance()
        
        elif name == 'display':
            #TODO
            pass

        elif name == 'load':
            if not arg.isString():
                self._error("wrong type of argument")
                return Nil.getInstance()
            filename = arg.strVal
            try:
                scanner = Scanner(open(filename))
                builder = TreeBuilder()
                parser = Parser(scanner, builder)

                root = parser.parseExp()
                while root != None:
                    root.eval(BuiltIn.env)
                    root = parser.parseExp()
            except IOError:
                self._error("could not find file " + filename)
            return Nil.getInstance()
        
        self._error("invalid builtin function call for " + name)
        return Nil.getInstance()

    def __apply2(self, arg1, arg2):
        name = self.symbol.getName()

        #binary operators all start with b_
        if arg1.isNumber() and arg2.isNumber() and name[0] == 'b':
            if name == 'b>':
                return BoolLit.getInstance(arg1.intVal > arg2.intVal)
            elif name == 'b<':
                return BoolLit.getInstance(arg1.intVal < arg2.intVal)
            elif name == 'b+':
                return IntLit(arg1.intVal + arg2.intVal)
            elif name == 'b-':
                return IntLit(arg1.intVal - arg2.intVal)
            elif name == 'b*':
                return IntLit(arg1.intVal * arg2.intVal)
            elif name == 'b/':
                return IntLit(arg1.intVal / arg2.intVal)
            elif name == 'b=':
                return BoolLit.getInstance(arg1.intVal == arg2.intVal)
            self._error("invalid binary operation")

        elif name == 'cons':
            return Cons(arg1, arg2)

        elif name == 'set-car!':
            arg1.setCar(arg2)
            return Nil.getInstance()

        elif name == 'set-cdr!':
            arg1.setCdr(arg2)
            return Nil.getInstance()

        elif name == 'eq?':
            #TODO: fix error with two equal variables giving #f when eq?
            return BoolLit.getInstance(arg1 == arg2)

        elif name == 'eval':
            return arg1.eval(arg2)

        elif name == 'apply':
            return arg1.apply(arg2)

        self._error("invalid builtin function call for " + name)
        return Nil.getInstance()



