from abc import ABC, abstractmethod
from typing import List

from bsat._core import SATProblem


class SATSolver(ABC):
    """Defines an interface for algorithms to solve CNF-SAT problems.
    """

    def solve_proposition(self, proposition: str) -> SATProblem:
        """Determines satisfiability a Boolean expression.

        :param proposition: The Boolean expression to solve.
        :return: The input expression formulated as a CNF-SAT problem, including its solutions (if any).
        """
        problem = SATProblem(proposition)
        problem.solutions = self.solve(problem)
        return problem

    @abstractmethod
    def solve(self, problem: SATProblem) -> List[str]:
        """Determines satisfiability of a SAT problem.

        :param problem: The SAT problem to solve.
        :return: List of assignments satisfying the problem, or an empty list if not satisfiable.
        """
        pass
