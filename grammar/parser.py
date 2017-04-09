from ply import yacc

from grammar import *


class Parser:
    def __init__(self):
        self.operations = {
            '!': self._not,
            '&': self._and,
            '|': self._or
        }
        create()

    def _and(self, p, q):
        if isinstance(p, bool) and p:
            return q
        elif isinstance(p, bool) and not p:
            return False
        elif isinstance(q, bool) and q:
            return p
        elif isinstance(q, bool) and not q:
            return False

    def _or(self, p, q):
        if isinstance(p, bool) and p:
            return True
        elif isinstance(p, bool) and not p:
            return q
        elif isinstance(q, bool) and q:
            return True
        elif isinstance(q, bool) and not q:
            return p

    def _not(self, p):
        if isinstance(p, bool):
            return not p

    def parse(self, expression):
        parser = yacc.yacc()
        return parser.parse(expression)
