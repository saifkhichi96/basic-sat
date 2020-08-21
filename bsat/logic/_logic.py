"""Defines the core members of the 'logic' package.

This is the internal definition of the package, with all the public and private classes defined here. \
Only the public classes are exported for external use.
"""

from abc import ABC, abstractmethod
from typing import Any, List

from .grammar import FALSE, TRUE, Operators


class Expression(ABC):
    """Abstract representation of a single Boolean logic operation.

    Operations are saved as recursive trees, where all operands in the operation may themselves
    be other Boolean operations.

    Attributes:
        operator: The logical operator in this operation (if any).
        operand_1: The first operand in the operation (if any).
        operand_2: The second operand in the operation (if any).
    """
    operator: Operators

    def __init__(self, operator=None, operand_1=None, operand_2=None):
        """Creates a new Boolean operation.

        Args:
            operator: The logical operator in this operation (if any).
            operand_1: The first operand in the operation (if any).
            operand_2: The second operand in the operation (if any).
        """
        self.operator = operator
        self.operand_1 = operand_1 if not None else None
        self.operand_2 = operand_2 if not None else None

    @property
    def literals(self) -> List[Any]:
        """List of unique literals in the recursive formula tree."""
        literals = set()
        for op in [self.operand_1, self.operand_2]:
            if op is not None:
                if isinstance(op, Literal):
                    literals.update(str(op))
                elif isinstance(op, Expression):
                    literals.update(op.literals)

        return sorted(literals)

    @property
    @abstractmethod
    def parse_tree(self) -> List[Any]:
        """Parse tree of the recursive Boolean operation as a preorder, nested list."""
        pass

    def __eq__(self, obj):
        """Checks equality of the two Boolean operations."""
        return isinstance(obj, Expression) and obj.parse_tree == self.parse_tree


class Literal(Expression):
    """A literal is a single variable with no operations."""

    def __init__(self, value):
        """Creates a new literal.

        Args:
            value: Value of the variable.
        """
        Expression.__init__(self, operand_1=value)

    @property
    def parse_tree(self):
        """See base class."""
        return self.operand_1

    def __str__(self):
        """Returns a printable representation of the literal."""
        if isinstance(self.operand_1, bool):
            return TRUE if self.operand_1 else FALSE

        else:
            return str(self.operand_1)


class UnaryOperation(Expression):
    """A unary operation consists of a unary operator applied on a single operand."""

    def __init__(self, operator: str, value: Expression):
        """Creates a new unary operation."""
        Expression.__init__(self, operator=operator, operand_1=value)

    @property
    def parse_tree(self) -> List[Any]:
        """See base class."""
        return [self.operator, self.operand_1.parse_tree]

    def __str__(self) -> str:
        """Returns a printable representation of the operation."""
        if isinstance(self.operand_1, UnaryOperation):
            return f'{self.operator}({self.operand_1})'
        else:
            return f'{self.operator}{self.operand_1}'


class BinaryOperation(Expression):
    """A binary operation consists of a binary operator applied to two different operands."""

    def __init__(self, operator: str, operand_1: Expression, operand_2: Expression):
        """Creates a new binary operation.

        Args:
            operator: The logical operator in this operation.
            operand_1: The first operand in the operation.
            operand_2: The second operand in the operation."""
        Expression.__init__(self, operator, operand_1, operand_2)

    @property
    def parse_tree(self) -> List[Any]:
        """See base class."""
        return [self.operator, self.operand_1.parse_tree, self.operand_2.parse_tree]

    def __str__(self) -> str:
        """Returns a printable representation of the operation."""
        return f'({self.operand_1} {self.operator} {self.operand_2})'
