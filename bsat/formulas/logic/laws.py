from . import UnaryFormula, BinaryFormula, ExpressionBuilder
from .grammar import NOT, AND, OR


def distribute_ands(expr):
    """Applies distributive law where an OR occurs over an AND.
    """
    if isinstance(expr, BinaryFormula):
        pq = distribute_ands(expr.operand_1)
        qr = distribute_ands(expr.operand_2)
        op = expr.operator

        if op == OR and qr.operator == AND:
            p = pq.parse_tree
            q = qr.operand_1.parse_tree
            r = qr.operand_2.parse_tree

            expr_n = ExpressionBuilder.from_parse_tree([AND, [OR, p, q], [OR, p, r]])
            tree_n = [AND,
                      distribute_ands(expr_n.operand_1).parse_tree,
                      distribute_ands(expr_n.operand_2).parse_tree]

        elif op == OR and pq.operator == AND:
            p = pq.operand_1.parse_tree
            q = pq.operand_2.parse_tree
            r = qr.parse_tree

            expr_n = ExpressionBuilder.from_parse_tree([AND, [OR, p, r], [OR, q, r]])
            tree_n = [AND,
                      distribute_ands(expr_n.operand_1).parse_tree,
                      distribute_ands(expr_n.operand_2).parse_tree]

        else:
            tree_n = [op, pq.parse_tree, qr.parse_tree]

    elif isinstance(expr, UnaryFormula):
        tree_n = [expr.operator, distribute_ands(expr.operand_1).parse_tree]

    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)


def de_morgans_law(expr):
    """Moves negations inwards by recursively applying De Morgan's Law.

    De Morgan's Law States moves the negation inwards by inverting the
    truth value of both operands and switching AND with OR and vice versa.
    i.e. 1) NOT(A  OR B) <=> NOT(A) AND NOT(B)
         2) NOT(A AND B) <=> NOT(A)  OR NOT(B)
    """
    # De Morgan's is only applicable if current formula has the negation
    # operator and the operand itself is a binary formula with a conjunction
    # or disjunction operator.
    if expr.operator == NOT and expr.operand_1.operator in [AND, OR]:
        if expr.operand_1.operator == AND:
            op = OR
        else:
            op = AND

        op1_neg = ExpressionBuilder.from_parse_tree([NOT, expr.operand_1.operand_1.parse_tree])
        t1 = de_morgans_law(op1_neg).parse_tree

        op2_neg = ExpressionBuilder.from_parse_tree([NOT, expr.operand_1.operand_2.parse_tree])
        t2 = de_morgans_law(op2_neg).parse_tree

        tree_n = [op, t1, t2]

    # In case current formula is a negation, and the child is also a
    # negation, we simply eliminate the double negation.
    elif expr.operator == NOT and expr.operand_1.operator == NOT:
        tree_n = expr.operand_1.parse_tree[-1]

    # In case current formula is itself binary, we check both operands
    # for De Morgan's applicability.
    elif isinstance(expr, BinaryFormula):
        tree_n = [expr.operator,
                  de_morgans_law(expr.operand_1).parse_tree,
                  de_morgans_law(expr.operand_2).parse_tree]

    # Otherwise return the current formula as-is.
    else:
        tree_n = expr.parse_tree

    return ExpressionBuilder.from_parse_tree(tree_n)
