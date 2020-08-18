from ._lexer import Lexer
from ._parser import Parser


class PropositionParser:
    def __init__(self):
        self.lexer = Lexer.build()
        self.parser = Parser.build()

    def parse(self, expression):
        return self.parser.parse(expression)

    @classmethod
    def operations(cls):
        return Parser().operations
