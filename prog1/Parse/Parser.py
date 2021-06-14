# Parser -- the parser for the Scheme printer and interpreter
#
# Defines
#
#   class Parser
#
# Parses the language
#
#   exp  ->  ( rest
#         |  #f
#         |  #t
#         |  ' exp
#         |  integer_constant
#         |  string_constant
#         |  identifier
#    rest -> )
#         |  exp+ [. exp] )
#
# and builds a parse tree.  Lists of the form (rest) are further
# `parsed' into regular lists and special forms in the constructor
# for the parse tree node class Cons.  See Cons.parseList() for
# more information.
#
# The parser is implemented as an LL(0) recursive descent parser.
# I.e., parseExp() expects that the first token of an exp has not
# been read yet.  If parseRest() reads the first token of an exp
# before calling parseExp(), that token must be put back so that
# it can be re-read by parseExp() or an alternative version of
# parseExp() must be called.
#
# If EOF is reached (i.e., if the scanner returns None instead of a token),
# the parser returns None instead of a tree.  In case of a parse error, the
# parser discards the offending token (which probably was a DOT
# or an RPAREN) and attempts to continue parsing with the next token.

import sys
from Tokens import TokenType
from Tree import *

class Parser:
    def __init__(self, s):
        self.scanner = s

    def parseExp(self):
        # TODO: write code for parsing an exp
        intake = self.scanner.getNextToken()
        return self.parseToken(intake) 

    def parseRest(self):
        # TODO: write code for parsing a rest
        intake = self.scanner.getNextToken()

        if intake.getType() == TokenType.RPAREN:
            return Nil.getInstance()
        elif intake.getType() == TokenType.DOT:
            return Cons(self.parseExp(), self.parseRest())
        elif intake == None:
            return None
        else:
            return Cons(self.parseToken(intake), self.parseRest())

    # TODO: Add any additional methods you might need
    def parseToken(self, intake):
        if intake.getType() == TokenType.LPAREN:
            return self.parseRest()
        elif intake.getType() == TokenType.FALSE:
            return BoolLit.getInstance(False)
        elif intake.getType() == TokenType.TRUE:
            return BoolLit.getInstance(True)
        elif intake.getType() == TokenType.QUOTE:
            return Cons(Ident("quote"), Cons(self.parseExp(), Nil.getInstance()))
        elif intake.getType() == TokenType.INT:
            return IntLit(intake.getIntVal())
        elif intake.getType() == TokenType.STR:
            return StrLit(intake.getStrVal())
        elif intake.getType() == TokenType.IDENT:
            return Ident(intake.getName())
        elif intake == None:
            return None
        else:
            #self.__error("Unexpected token: " + intake.getType())
            return self.parseExp()

    
    def __error(self, msg):
        sys.stderr.write("Parse error: " + msg + "\n")
