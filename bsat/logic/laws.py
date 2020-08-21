"""Defines the laws of propositional logic.
"""

from . import ExpressionBuilder, Expression, UnaryOperation, BinaryOperation
from .grammar import Operators


def distribute_ands(expr: Expression) -> Expression:
    """Applies distributive law where an OR occurs over an AND.

    Recursively applies the following distributive law until it is no longer applicable:
    a OR (b AND c) <=> (a OR b) AND (a OR c).

    Args:
        expr: The Boolean expression to apply the distributive law on.

    Returns:
        An equivalent Boolean expression with all ORs distributed over ANDs.
    """
    if isinstance(expr, BinaryOperation):
        pq = distribute_ands(expr.operand_1)
        qr = distribute_ands(expr.operand_2)
        op = expr.operator

        if op == Operators.OR and qr.operator == Operators.AND:
            p = pq.parse_tree
            q = qr.operand_1.parse_tree
            r = qr.operand_2.parse_tree

            expr_n = ExpressionBuilder.from_parse_tree([Operators.AND,
                                                        [Operators.OR, p, q],
                                                        [Operators.OR, p, r]])
            tree_n = [Operators.AND,
                      distribute_ands(expr_n.operand_1).parse_tree,
                      distribute_ands(expr_n.operand_2).parse_tree]

        elif op == Operators.OR and pq.operator == Operators.AND:
            p = pq.operand_1.parse_tree
            q = pq.operand_2.parse_tree
            r = qr.parse_tree

            expr_n = ExpressionBuilder.from_parse_tree([Operators.AND,
                                                        [Operators.OR, p, r],
                                                        [Operators.OR, q, r]])
            tree_n = [Operators.AND,
                      distribute_ands(expr_n.operand_1).parse_tree,
                      distribute_ands(expr_n.operand_2).parse_tree]

        else:
            tree_n = [op, pq.parse_tree, qr.parse_tree]

    elif isinstance(expr, UnaryOperation):
        tree_n = [expr.operator, distribute_ands(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)


def de_morgans_law(expr: Expression) -> Expression:
    """Moves negations inwards by repeatedly applying De Morgan's Law and removing double negations.

    De Morgan's Law States moves the negation inwards by inverting the truth value of both operands
    and switching AND with OR and vice versa. i.e.
        1) NOT(a OR b) <=> NOT(a) AND NOT(b)
        2) NOT(A AND B) <=> NOT(A)  OR NOT(B)

    This is a recursive implementation, which also removes double negations which may arise from
    application of De Morgan's law, or otherwise.

    Args:
        expr: The Boolean expression to apply De Morgan's law on.

    Returns:
        An equivalent Boolean expression with negations only over literals.
    """
    # De Morgan's is only applicable if current formula has the negation operator and the
    # operand itself is a binary formula with a conjunction or disjunction operator.
    if expr.operator == Operators.NOT and expr.operand_1.operator in [Operators.AND, Operators.OR]:
        if expr.operand_1.operator == Operators.AND:
            op = Operators.OR
        else:
            op = Operators.AND

        op1_neg = ExpressionBuilder.from_parse_tree([Operators.NOT, expr.operand_1.operand_1.parse_tree])
        t1 = de_morgans_law(op1_neg).parse_tree

        op2_neg = ExpressionBuilder.from_parse_tree([Operators.NOT, expr.operand_1.operand_2.parse_tree])
        t2 = de_morgans_law(op2_neg).parse_tree

        tree_n = [op, t1, t2]

    # In case current formula is a negation, and the child is also a negation, we simply
    # eliminate the double negation.
    elif expr.operator == Operators.NOT and expr.operand_1.operator == Operators.NOT:
        tree_n = expr.operand_1.parse_tree[-1]

    # In case current formula is itself binary, we check both operands for De Morgan's applicability.
    elif isinstance(expr, BinaryOperation):
        tree_n = [expr.operator,
                  de_morgans_law(expr.operand_1).parse_tree,
                  de_morgans_law(expr.operand_2).parse_tree]

    # Otherwise return the current formula as-is.
    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)
