"""Builds a tokenizer for propositional logic expressions.

Defines a vocabulary for writing propositional logic expressions, and builds
a lexer which tokenizes the input text according to defined vocabulary.

    Typical usage example:

    lexer = Lexer.build()
"""

from enum import Enum

import ply.lex as lex


class _AutoName(Enum):
    """An enumeration with items named automatically after their values."""

    def _generate_next_value_(name, start, count, last_values):
        """See base class."""
        return name


class Operators(_AutoName):
    """An enumeration listing all permitted logical operations."""
    OR = '|'
    AND = '&'
    NOT = '~'
    XOR = '+'
    IFF = '<->'
    IMPLIES = '->'

    def __eq__(self, other):
        """Checks equality of two operators."""
        return str(self) == str(other)

    def __hash__(self):
        """Returns hashcode of the operator."""
        return id(self)

    def __str__(self):
        """Returns a printable representation of the operator."""
        return str(self.value)


# List of accepted tokens
tokens = (
    'LITERAL',
    'IFF',
    'XOR',
    'IMPLIES',
    'OR',
    'AND',
    'NOT',
    'LPAR',
    'RPAR',
    'FALSE',
    'TRUE'
)

# Symbols for the listed tokens
OR = Operators.OR
AND = Operators.AND
NOT = Operators.NOT
XOR = Operators.XOR
IFF = Operators.IFF
IMPLIES = Operators.IMPLIES
LPAR = '('
RPAR = ')'
FALSE = '0'
TRUE = '1'

# Precedence rules for boolean logic
precedence = (
    ('left', 'IFF'),
    ('left', "XOR"),
    ('left', 'IMPLIES'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)


class Lexer:
    @classmethod
    def build(cls):
        # Regular expression rules for simple tokens
        t_LITERAL = '[a-zA-Z]+'
        t_IFF = r'<->'
        t_XOR = r'\+'
        t_IMPLIES = r'->'
        t_OR = r'\|'
        t_AND = r'&'
        t_NOT = r'~'
        t_LPAR = r'\('
        t_RPAR = r'\)'

        # Rule for the special literal FALSE
        def t_FALSE(t):
            r'0'
            t.value = False
            return t

        # Rule for the special literal TRUE
        def t_TRUE(t):
            r'1'
            t.value = True
            return t

        # Rule for ignoring whitespaces
        t_ignore = ' \t\n'

        # Rule for error handling
        def t_error(t):
            raise RuntimeError("Illegal character '%s' at %d:%d" % (t.value[0], t.lineno, t.lexpos))

        return lex.lex()
