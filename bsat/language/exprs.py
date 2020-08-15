from abc import ABC, abstractmethod
from ..grammar import PBLParser
from ..grammar.lexer import AND, OR, XOR, IFF, IMPLIES, NOT


class Expression(ABC):
    def __init__(self, op=None, val1=None, val2=None):
        self.operator = op
        self.operand_1 = val1
        self.operand_2 = val2

    def __eq__(self, obj):
        return isinstance(obj, Expression) and obj.parse_tree == self.parse_tree

    @property
    @abstractmethod
    def parse_tree(self):
        return []

    def _literals(self, parse_tree):
        literals = set()
        for item in parse_tree:
            if isinstance(item, list):
                literals.update(self._literals(item))
            elif isinstance(item, str) and item not in [AND, OR, XOR, IFF, IMPLIES, NOT]:
                literals.add(item)

        return sorted(literals)

    @property
    def literals(self):
        return self._literals(self.parse_tree)

    def negate(self):
        return Expression.build_from_tree([NOT, self.parse_tree])

    def is_literal(self):
        if isinstance(self, Literal):
            return True
        elif isinstance(self, UnaryFormula) and self.operand_1.is_literal():
            return True
        else:
            return False

    def is_clause(self):
        if isinstance(self, BinaryFormula):
            return (self.operand_1.is_clause() or self.operand_1.is_literal) and \
                   (self.operand_2.is_clause() or self.operand_2.is_literal) and \
                   self.operator == OR

        else:
            return self.is_literal()

    @classmethod
    def build_from_tree(cls, parse_tree):
        if isinstance(parse_tree, list):
            if len(parse_tree) == 1:
                return Literal(parse_tree[0])

            elif len(parse_tree) == 2:
                assert (not isinstance(parse_tree[0], list))
                return UnaryFormula(parse_tree[0], parse_tree[1])

            elif len(parse_tree) == 3:
                assert (not isinstance(parse_tree[0], list))
                return BinaryFormula(parse_tree[0], parse_tree[1], parse_tree[2])

        elif isinstance(parse_tree, str) or isinstance(parse_tree, bool):
            return Literal(parse_tree)

        return None

    @classmethod
    def build_from_pbl(cls, proposition):
        parser = PBLParser()
        parse_tree = parser.parse(proposition)
        return Expression.build_from_tree(parse_tree)


class Literal(Expression):
    def __init__(self, value):
        Expression.__init__(self, val1=value)

    def __str__(self):
        return str(self.operand_1)

    @property
    def parse_tree(self):
        return self.operand_1


class UnaryFormula(Expression):
    def __init__(self, op, value):
        Expression.__init__(self, op=op, val1=Expression.build_from_tree(value))

    def __str__(self):
        if isinstance(self.operand_1, UnaryFormula):
            return f'{self.operator}({self.operand_1})'
        else:
            return self.operator + str(self.operand_1)

    @property
    def parse_tree(self):
        return [self.operator, self.operand_1.parse_tree]


class BinaryFormula(Expression):
    def __init__(self, op, v1, v2):
        Expression.__init__(self, op=op,
                            val1=Expression.build_from_tree(v1),
                            val2=Expression.build_from_tree(v2))

    def __str__(self):
        return f'({self.operand_1} {self.operator} {self.operand_2})'

    @property
    def parse_tree(self):
        return [self.operator, self.operand_1.parse_tree, self.operand_2.parse_tree]
