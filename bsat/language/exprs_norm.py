from abc import ABC, abstractmethod
from .exprs import Expression
from .laws import de_morgans_law, distribute_ands
from .equiv import simplify_operators
from ..grammar.lexer import AND, OR, NOT


class NF(ABC):
    def __init__(self, expr, from_pbl=False):
        if from_pbl:
            assert isinstance(expr, str)
            expr = Expression.build_from_pbl(expr)

        self.expr = self._build(expr)

    @abstractmethod
    def _build(self, expr):
        return None


class NNF(NF):
    def __init__(self, expr, from_pbl=False):
        NF.__init__(self, expr, from_pbl)

    def _build(self, expr):
        return de_morgans_law(expr)


class CNF(NF):
    def __init__(self, expr, from_pbl=False):
        NF.__init__(self, expr, from_pbl)

    def _build(self, expr):
        expr_n = simplify_operators(expr)
        for i in range(3):
            expr_n = distribute_ands(NNF(expr_n).expr)

        return expr_n

    def __clauses(self, parse_tree, op):
        clause = self._clauses(parse_tree)
        if op == AND and len(clause.strip()) != 0:
            clause += '\n'
        return clause

    def _clauses(self, parse_tree):
        """Returns list of the clauses in CNF as a string.
        """
        clause = ''
        if isinstance(parse_tree, str):
            clause += parse_tree + '  '

        elif isinstance(parse_tree, list):
            if len(parse_tree) == 3:
                op, t1, t2 = tuple(parse_tree)
                clause += self.__clauses(t1, op)
                clause += self.__clauses(t2, op)

            elif len(parse_tree) == 2:
                op, val = tuple(parse_tree)
                clause += op + self._clauses(val)

        return clause.replace('\n\n', '\n')

    @property
    def clauses(self):
        """Returns list of the clauses in CNF.
        """
        clauses = []
        for c in self._clauses(self.expr.parse_tree).split('\n'):
            c = c.strip()
            if c != '':
                clauses.append(c)

        return clauses

    def as_dimacs(self):
        clauses = self.clauses

        raw = ''
        for clause in clauses:
            raw += clause.replace(NOT, '-') + '  0\n'

        literals = self.expr.literals
        for lt in literals:
            raw = raw.replace(lt, f'{literals.index(lt) + 1}')

        return 'c a sample CNF formula\np cnf %d %d\n%s' % (len(literals), len(clauses), raw)

    def __str__(self):
        string = ''

        clauses = self.clauses
        for i, clause in enumerate(clauses):
            string += '('
            for j, item in enumerate(clause.split(' ')):
                item = item.strip()
                if item != '' and item != NOT:
                    string += item
                    string += f' {OR} '
            string = string[:-3]
            string += ')'
            if i + 1 != len(clauses):
                string += f' {AND} '

        return string
