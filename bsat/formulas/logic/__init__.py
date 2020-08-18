from ._operations import Expression, UnaryFormula, BinaryFormula, Literal
from .grammar import PropositionParser


class ExpressionBuilder:
    @classmethod
    def from_proposition(cls, proposition):
        parser = PropositionParser()
        parse_tree = parser.parse(proposition)
        return cls.from_parse_tree(parse_tree)

    @classmethod
    def from_parse_tree(cls, parse_tree):
        if isinstance(parse_tree, list):
            if len(parse_tree) == 1:
                return Literal(parse_tree[0])

            elif len(parse_tree) == 2:
                assert (not isinstance(parse_tree[0], list))
                return UnaryFormula(parse_tree[0],
                                    ExpressionBuilder.from_parse_tree(parse_tree[1]))

            elif len(parse_tree) == 3:
                assert (not isinstance(parse_tree[0], list))
                return BinaryFormula(parse_tree[0],
                                     ExpressionBuilder.from_parse_tree(parse_tree[1]),
                                     ExpressionBuilder.from_parse_tree(parse_tree[2]))

        elif isinstance(parse_tree, str) or isinstance(parse_tree, bool):
            return Literal(parse_tree)
