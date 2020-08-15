from .exprs import Expression, Literal, UnaryFormula, BinaryFormula
from ..grammar.lexer import XOR, IFF, IMPLIES, NOT, AND, OR


def remove_xor(expr):
    if isinstance(expr, BinaryFormula):
        t1 = remove_xor(expr.operand_1).parse_tree
        t2 = remove_xor(expr.operand_2).parse_tree
        op = expr.operator

        if op == XOR:
            tree_n = [NOT, [IFF, t1, t2]]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryFormula):
        tree_n = [expr.operator, remove_xor(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return Expression.build_from_tree(tree_n)


def remove_iff(expr):
    if isinstance(expr, BinaryFormula):
        t1 = remove_iff(expr.operand_1).parse_tree
        t2 = remove_iff(expr.operand_2).parse_tree
        op = expr.operator

        if op == IFF:
            tree_n = [AND, [IMPLIES, t1, t2], [IMPLIES, t2, t1]]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryFormula):
        tree_n = [expr.operator, remove_iff(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return Expression.build_from_tree(tree_n)


def remove_implies(expr):
    if isinstance(expr, BinaryFormula):
        t1 = remove_implies(expr.operand_1).parse_tree
        t2 = remove_implies(expr.operand_2).parse_tree
        op = expr.operator

        if op == IMPLIES:
            tree_n = [OR, [NOT, t1], t2]
        else:
            tree_n = [op, t1, t2]

    elif isinstance(expr, UnaryFormula):
        tree_n = [expr.operator, remove_implies(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return Expression.build_from_tree(tree_n)


def simplify_operators(expr):
    """Simplifies an expression by reducing all operators to AND, OR and NOT.
    """
    expr = remove_xor(expr)
    expr = remove_iff(expr)
    return remove_implies(expr)
