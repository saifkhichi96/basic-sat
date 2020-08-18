from ._utils import remove_whitespaces
from .formulas import CNF


class SATProblem:
    def __init__(self, formula: str):
        """ Formulates a CNF-SAT problem from a propositional logic formula.

        :param formula: A propositional logic formula.
        """
        self.formula = CNF(remove_whitespaces(formula), from_proposition=True)
        self.solutions = None

    @property
    def is_contradiction(self):
        return self.solutions is not None and len(self.solutions) == 0
