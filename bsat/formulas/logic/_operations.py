from abc import ABC, abstractmethod
from typing import Any, List

from .grammar import AND, OR, XOR, IFF, IMPLIES, NOT


class Expression(ABC):
    """Represents a Boolean logic operation (e.g. AND, OR, etc).
    """

    def __init__(self, operator=None, operand_1=None, operand_2=None):
        """ Creates a new Boolean operation.

        :param operator: The Boolean operator to use in the operation.
        """
        self.operator = operator
        self.operand_1 = operand_1 if not None else None
        self.operand_2 = operand_2 if not None else None

    @property
    def literals(self) -> List[Any]:
        return self._literals(self.parse_tree)

    @property
    @abstractmethod
    def parse_tree(self) -> List[Any]:
        pass

    def _literals(self, parse_tree: List[Any]) -> List[Any]:
        literals = set()
        for item in parse_tree:
            if isinstance(item, list):
                literals.update(self._literals(item))
            elif isinstance(item, str) and item not in [AND, OR, XOR, IFF, IMPLIES, NOT]:
                literals.add(item)

        return sorted(literals)

    def __eq__(self, obj):
        return isinstance(obj, Expression) and obj.parse_tree == self.parse_tree


class UnaryFormula(Expression):
    def __init__(self, operator: str, value: Expression):
        Expression.__init__(self, operator=operator, operand_1=value)

    def __str__(self) -> str:
        if isinstance(self.operand_1, UnaryFormula):
            return f'{self.operator}({self.operand_1})'
        else:
            return f'{self.operator}{self.operand_1}'

    @property
    def parse_tree(self) -> List[Any]:
        return [self.operator, self.operand_1.parse_tree]


class BinaryFormula(Expression):
    def __init__(self, operator: str, operand_1: Expression, operand_2: Expression):
        Expression.__init__(self, operator, operand_1, operand_2)

    def __str__(self) -> str:
        return f'({self.operand_1} {self.operator} {self.operand_2})'

    @property
    def parse_tree(self) -> List[Any]:
        return [self.operator, self.operand_1.parse_tree, self.operand_2.parse_tree]


class Literal(Expression):
    def __init__(self, value):
        Expression.__init__(self, operand_1=value)

    def __str__(self):
        return self.operand_1

    @property
    def parse_tree(self):
        return self.operand_1
