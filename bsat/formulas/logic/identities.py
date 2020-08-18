from . import UnaryFormula, BinaryFormula, ExpressionBuilder
from .grammar import XOR, IFF, IMPLIES, NOT, AND, OR


def xor_equivalence(expr):
    if isinstance(expr, BinaryFormula):
        t1 = xor_equivalence(expr.operand_1).parse_tree
        t2 = xor_equivalence(expr.operand_2).parse_tree
        op = expr.operator

        if op == XOR:
            tree_n = [NOT, [IFF, t1, t2]]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryFormula):
        tree_n = [expr.operator, xor_equivalence(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)


def iff_equivalence(expr):
    if isinstance(expr, BinaryFormula):
        t1 = iff_equivalence(expr.operand_1).parse_tree
        t2 = iff_equivalence(expr.operand_2).parse_tree
        op = expr.operator

        if op == IFF:
            tree_n = [AND, [IMPLIES, t1, t2], [IMPLIES, t2, t1]]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryFormula):
        tree_n = [expr.operator, iff_equivalence(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)


def implication_equivalence(expr):
    if isinstance(expr, BinaryFormula):
        t1 = implication_equivalence(expr.operand_1).parse_tree
        t2 = implication_equivalence(expr.operand_2).parse_tree
        op = expr.operator

        if op == IMPLIES:
            tree_n = [OR, [NOT, t1], t2]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryFormula):
        tree_n = [expr.operator, implication_equivalence(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)


def simplify_operators(expr):
    """Simplifies an expression by reducing all operators to AND, OR and NOT.
    """
    expr = xor_equivalence(expr)
    expr = iff_equivalence(expr)
    return implication_equivalence(expr)
