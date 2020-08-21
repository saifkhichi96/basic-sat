"""Defines Boolean identities which define equivalence of logic operators.
"""

from . import ExpressionBuilder, Expression, UnaryOperation, BinaryOperation
from .grammar import Operators


def xor_equivalence(expr: Expression) -> Expression:
    """Removes all XORs from a Boolean formula.

    All XOR operations are replaced by an equivalent logical operation. By definition, XOR
    is same as the negation of logical bi-conditional (IFF), i.e. a XOR b = NOT(a IFF b)

    Args:
        expr: The expression to remove the XORs from.

    Returns:
        An equivalent expression without XOR operations.
    """
    if isinstance(expr, BinaryOperation):
        t1 = xor_equivalence(expr.operand_1).parse_tree
        t2 = xor_equivalence(expr.operand_2).parse_tree
        op = expr.operator

        if op == Operators.XOR:
            tree_n = [Operators.NOT, [Operators.IFF, t1, t2]]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryOperation):
        tree_n = [expr.operator, xor_equivalence(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)


def iff_equivalence(expr: Expression) -> Expression:
    """Removes all logical bi-conditionals (IFF) from a Boolean formula.

    All logical bi-conditional (IFF) operations are replaced by an equivalent logical operation.
    By definition a bi-conditional is same as AND of two implications in both directions, i.e.
    a IFF b = (a IMPLIES b) AND (b IMPLIES a)

    Args:
        expr: The expression to remove the IFFs from.

    Returns:
        An equivalent expression without IFF operations.
    """
    if isinstance(expr, BinaryOperation):
        t1 = iff_equivalence(expr.operand_1).parse_tree
        t2 = iff_equivalence(expr.operand_2).parse_tree
        op = expr.operator

        if op == Operators.IFF:
            tree_n = [Operators.AND, [Operators.IMPLIES, t1, t2], [Operators.IMPLIES, t2, t1]]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryOperation):
        tree_n = [expr.operator, iff_equivalence(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)


def implication_equivalence(expr: Expression) -> Expression:
    """Removes all logical implications (IMPLIES) from a Boolean formula.

    All logical implication (IMPLIES) operations are replaced by an equivalent logical operation.
    By definition an implication has the following equivalence: a IMPLIES b = NOT(a) OR b

    Args:
        expr: the expression to remove the IMPLIES operations from.

    Returns:
        An equivalent expression without IMPLIES operations.
    """
    if isinstance(expr, BinaryOperation):
        t1 = implication_equivalence(expr.operand_1).parse_tree
        t2 = implication_equivalence(expr.operand_2).parse_tree
        op = expr.operator

        if op == Operators.IMPLIES:
            tree_n = [Operators.OR, [Operators.NOT, t1], t2]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryOperation):
        tree_n = [expr.operator, implication_equivalence(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)


def simplify_operators(expr: Expression) -> Expression:
    """Simplifies an expression by reducing all logical operators to AND, OR and NOT.

    Boolean identities are applied to systematically replace all exclusive OR, implication
    and logical bi-conditional operators with the three basic logic operators, AND, OR and
    NOT.

    Args:
        expr: The expression to simplify.

    Returns:
        An equivalent expression with no complex logical operators.
    """
    expr = xor_equivalence(expr)
    expr = iff_equivalence(expr)
    return implication_equivalence(expr)
