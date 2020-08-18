from abc import ABC, abstractmethod

from .logic import ExpressionBuilder
from .logic.grammar import PropositionParser


class NF(ABC):
    def __init__(self, formula, from_proposition=False):
        if from_proposition:
            assert isinstance(formula, str)
            formula = ExpressionBuilder.from_proposition(formula)

        self.expr = self._build(formula)

    @property
    def parse_tree(self):
        return self._parse_tree(self.expr.parse_tree)

    def _parse_tree(self, tree):
        if isinstance(tree, list) and len(tree) >= 2:
            operator = PropositionParser.operations()[tree[0]]
            return [operator] + list(map(self._parse_tree, tree[1:]))
        elif isinstance(tree, list) and len(tree) == 1:
            return self._parse_tree(tree[0])
        else:
            return tree

    @abstractmethod
    def _build(self, formula):
        return formula
