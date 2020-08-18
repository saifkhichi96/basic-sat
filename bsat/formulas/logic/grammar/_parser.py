"""Creates a parser for propositional logic expressions.

Defines the grammar of the propositional logic language, which can then be
used to parse propositional boolean logic formulas.
"""
import ply.yacc as yacc

# Get the token map from the lexer. This is required.
from ._lexer import tokens, precedence, IMPLIES, XOR, IFF, AND, OR, NOT


class Parser:
    def __init__(self):
        self.operations = {
            IFF: self._iff,
            XOR: self._xor,
            IMPLIES: self._implies,
            OR: self._or,
            AND: self._and,
            NOT: self._not,
        }

    def _implies(self, p, q):
        if isinstance(p, bool) and p:
            return q
        elif isinstance(p, bool) and not p:
            return True
        elif isinstance(q, bool) and q:
            return True

    def _xor(self, p, q):
        return self._not(self._iff(p, q))

    def _iff(self, p, q):
        return self._and(self._implies(p, q), self._implies(q, p))

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

    @classmethod
    def build(cls):
        def p_expr_paren(p):
            """expr : LPAR expr RPAR"""
            p[0] = p[2]

        def p_expr_unary(p):
            """expr : NOT expr           %prec NOT"""
            p[0] = [p[1], p[2]]

        def p_expr_binop(p):
            """expr : expr IMPLIES expr  %prec IMPLIES
                    | expr IFF expr      %prec IFF
                    | expr XOR expr      %prec XOR
                    | expr OR expr       %prec OR
                    | expr AND expr      %prec AND
                    """
            p[0] = [p[2], p[1], p[3]]

        def p_expr_literal(p):
            """expr : literal"""
            p[0] = p[1]

        def p_literal(p):
            """literal : FALSE
                       | TRUE
                       | LITERAL"""
            p[0] = p[1]

        # Error rule for syntax errors
        def p_error(p):
            raise SyntaxError(p)

        return yacc.yacc()
