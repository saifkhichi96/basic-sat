"""Provides APIs for writing and manipulating Boolean logic expressions..
"""

from ._logic import Expression, UnaryOperation, BinaryOperation, Literal
from .grammar import PropositionParser, Operators


class ExpressionBuilder:
    """Factory class for building Boolean expressions."""

    @classmethod
    def from_proposition(cls, proposition: str) -> Expression:
        """Builds a Boolean expression from a propositional formula.

        Args:
            proposition: The propositional formula to build the expression from.
        """
        parser = PropositionParser()
        parse_tree = parser.parse(proposition)
        return cls.from_parse_tree(parse_tree)

    @classmethod
    def from_parse_tree(cls, tree) -> Expression:
        """Builds a Boolean expression from a parse tree.

        Args:
            tree: The parse tree to build the expression from.
        """
        try:
            if isinstance(tree, list):
                if len(tree) == 1:
                    val = tree[0]
                    if val in list(Operators):
                        return Operators(val)

                    else:
                        return Literal(val)

                elif len(tree) == 2:
                    op = tree[0]
                    val1 = tree[1]
                    return UnaryOperation(Operators(op), ExpressionBuilder.from_parse_tree(val1))

                elif len(tree) == 3:
                    op = tree[0]
                    val1 = tree[1]
                    val2 = tree[2]
                    return BinaryOperation(Operators(op),
                                           ExpressionBuilder.from_parse_tree(val1),
                                           ExpressionBuilder.from_parse_tree(val2))

            elif isinstance(tree, str) or isinstance(tree, bool):
                val = tree
                if val in list(Operators):
                    return Operators(val)

                else:
                    return Literal(val)

        except AssertionError:
            raise RuntimeError('Error reading the parse tree.')
