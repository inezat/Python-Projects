# Scanner -- The lexical analyzer for the Scheme printer and interpreter

import sys
import io
from Tokens import *

class Scanner:
    def __init__(self, i):
        self.In = i
        self.buf = []
        self.ch_buf = None

    def read(self):
        if self.ch_buf == None:
            return self.In.read(1)
        else:
            ch = self.ch_buf
            self.ch_buf = None
            return ch
    
    def peek(self):
        if self.ch_buf == None:
            self.ch_buf = self.In.read(1)
            return self.ch_buf
        else:
            return self.ch_buf

    @staticmethod
    def isDigit(ch):
        return ch >= '0' and ch <= '9'

    #White space defined via ASCII code (\t : \r, SPACE)
    @staticmethod
    def isWS(ch):
        return (ord(ch) >= 9 and ord(ch) <= 13) or ch == ' '

    @staticmethod
    def isLetter(ch):
        return (ch >= 'A' and ch <= 'Z') or (ch >= 'a' and ch <= 'z') or ch in ['!', '+', '-', '*', '/']
    def getNextToken(self):
        try:
            # It would be more efficient if we'd maintain our own
            # input buffer for a line and read characters out of that
            # buffer, but reading individual characters from the
            # input stream is easier.
            ch = self.read()

            # TODO: Skip white space and comments (WS DONE, NEED TO TEST)
            if (self.isWS(ch)):
                return self.getNextToken()
            if (ch == ';'):
                #On comment read, discard characters until read \n
                while (self.peek() != '\n'):
                    self.read()
                return self.getNextToken()

            # Return None on EOF
            if ch == "":
                return None
    
            # Special characters
            elif ch == '\'':
                return Token(TokenType.QUOTE)
            elif ch == '(':
                return Token(TokenType.LPAREN)
            elif ch == ')':
                return Token(TokenType.RPAREN)
            elif ch == '.':
                #  We ignore the special identifier `...'.
                return Token(TokenType.DOT)

            # Boolean constants
            elif ch == '#':
                ch = self.read()

                if ch == 't':
                    return Token(TokenType.TRUE)
                elif ch == 'f':
                    return Token(TokenType.FALSE)
                elif ch == "":
                    sys.stderr.write("Unexpected EOF following #\n")
                    return None
                else:
                    sys.stderr.write("Illegal character '" +
                                     chr(ch) + "' following #\n")
                    return self.getNextToken()

            # String constants
            elif ch == '"':
                self.buf = []
                # TODO: scan a string into the buffer variable buf (NEED TO TEST)
                while self.peek() != '"':
                    self.buf.append(self.read())
                    
                return StrToken("".join(self.buf))

            # Integer constants
            elif self.isDigit(ch):
                i = ord(ch) - ord('0')
                # TODO: scan the number and convert it to an integer (NEED TO TEST)
                while (self.isDigit(self.peek())):
                       ch = self.read()
                       i = i*10 + ord(ch) - ord('0')
                # make sure that the character following the integer
                # is not removed from the input stream
                return IntToken(i)
    
            # Identifiers
            elif self.isLetter(ch):
                # or ch is some other valid first character
                # for an identifier
                self.buf = []
                self.buf.append(ch)
                # TODO: scan an identifier into the buffer variable (NEED TO TEST)
                while (self.isLetter(self.peek())):
                       ch = self.read()
                       self.buf.append(ch.lower())
                # make sure that the character following the identifier
                # is not removed from the input stream
                return IdentToken("".join(self.buf))

            # Illegal character
            else:
                sys.stderr.write("Illegal input character '" + ch + "'\n")
                return self.getNextToken()

        except IOError:
            sys.stderr.write("IOError: error reading input file\n")
            return None


if __name__ == "__main__":
    scanner = Scanner(sys.stdin)
    tok = scanner.getNextToken()
    tt = tok.getType()
    print(tt)
    if tt == TokenType.INT:
        print(tok.getIntVal())
