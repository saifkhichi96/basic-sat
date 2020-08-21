"""Defines the grammar for writing Boolean formulas."""

from ._lexer import FALSE, TRUE, Operators
from ._lexer import Lexer as _Lexer
from ._parser import Parser as _Parser


class PropositionParser:
    """Parser to create trees from Boolean expressions provided as strings."""

    def __init__(self):
        self.lexer = _Lexer.build()
        self.parser = _Parser.build()

    def parse(self, expression: str):
        """Parses an expression.

        Args:
            expression: The expression to parse.
        """
        return self.parser.parse(expression)

    @classmethod
    def operations(cls) -> list:
        """Returns list of all operations supported by the parser."""
        return _Parser().operations
