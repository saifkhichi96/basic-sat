from .lexer import Lexer
from .parser import Parser


class PBLParser:
    def __init__(self):
        self.lexer = Lexer.build()
        self.parser = Parser.build()

    def parse(self, expression):
        return self.parser.parse(expression)
