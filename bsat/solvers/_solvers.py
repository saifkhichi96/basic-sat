"""Defines core members of the 'solvers' package.

This is the internal definition of the package, with the private classes and other common operations defined \
here. Specific SAT solving algorithms are defined in their own modules. Only concrete solvers are exported \
for external use.
"""

from abc import ABC, abstractmethod
from typing import Any, List

from ..logic.grammar import TRUE, FALSE
from ..norm import CNF
from ..utils import remove_whitespaces


class Assignment:
    """Exactly one set of truth values which satisfy a Boolean formula.

    An assignment consists of truth values for all the variables in the Boolean formula
    such that the whole formula evaluates to True. If the formula is always satisfiable
    (i.e. it is a tautology), then the assignment is given as True. Similarly, if the
    formula is unsatisfiable, the assignment is given as False.

    Attributes:
        _truth: A dictionary with truth values of the variables, or a boolean.
    """

    def __init__(self, truth):
        """Inits an assignment by saving the truth values."""
        self._truth = truth

    def __eq__(self, other) -> bool:
        """Checks equality of two assignments.

        Two assignments are equal if both have same truth values for same variables."""
        return str(other) == str(self)

    def __str__(self) -> str:
        """Returns a printable string listing the truth values."""
        if isinstance(self._truth, bool):
            return TRUE if self._truth else FALSE

        elif isinstance(self._truth, dict):
            s = ['']
            for var, value in self._truth.items():
                s.append(f'{var} = {TRUE if value else FALSE}, ')
            return ''.join(s)[:-2]

        else:
            return str(self._truth)


class SATSolution:
    """Solution of a CNF-SAT problem.

    Attributes:
        problem: The CNF formula to check satisfiability.
    """

    def __init__(self, problem: CNF, assignments: List[Any]):
        """Inits a solution for a CNF-SAT problem.

        Args:
            problem: The CNF formula to check satisfiability.
            assignments: List of all assignments (if any) solving the formula.
        """
        self.problem = problem
        self._assignments = []
        for assignment in assignments:
            self._assignments.append(Assignment(assignment))

    @property
    def is_false(self) -> bool:
        """Checks if the problem is unsatisfiable."""
        return len(self) == 0 or (len(self) == 1 and self._assignments[0] == FALSE)

    @property
    def is_true(self) -> bool:
        """Checks if the problem is always satisfiable."""
        return (len(self) > 0 and len(self) == self.problem.max_solutions) or \
               (len(self) == 1 and self._assignments[0] == TRUE)

    @property
    def assignments(self) -> list:
        """List of assignments satisfying the formula (or empty list)."""
        return self._assignments

    def __eq__(self, other) -> bool:
        """Checks equality of two solutions.

        Two solutions are equal if all their assignments are equal.
        """
        if isinstance(other, bool):
            return self.is_true if other else self.is_false
        else:
            return str(other) == str(self)

    def __len__(self) -> int:
        """Number of assignments satisfying the formula."""
        return len(self._assignments)

    def __str__(self) -> str:
        """Returns a printable representation of the solution."""
        if self.is_true:
            return 'Tautology'
        elif self.is_false:
            return 'UNSAT'
        else:
            return ''.join([f'\t{idx + 1}) {it}' for idx, it in enumerate(self._assignments)])


class SATSolver(ABC):
    """Defines an interface for algorithms to solve CNF-SAT problems.
    """

    def solve(self, proposition: str) -> SATSolution:
        """Determines satisfiability a Boolean expression.

        Args:
             proposition: The Boolean expression to solve.

        Returns:
            The input expression formulated as a CNF-SAT problem, including its solutions (if any).
        """
        problem = CNF(remove_whitespaces(proposition))
        return self._solve(problem)

    @abstractmethod
    def _solve(self, problem: CNF) -> SATSolution:
        """Determines satisfiability of a CNF Boolean formula.

        Args:
            problem: The CNF-SAT problem to solve.

        Returns:
            Solution of the formula, including the assignments satisfying it (if any).
        """
        pass
