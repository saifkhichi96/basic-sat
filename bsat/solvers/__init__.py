"""Provides a collection of SAT solvers.

This package implements different SAT solving algorithms and exposes a common API for using these \
solvers to find satisfiability of CNF-SAT problems. Available solvers include DPLLSolver.

    Typical usage example:

    solver = DPLLSolver()
    solution = solver.solve('some propositional logic formula')
    solution.formula     # returns the CNF representation of the input formula
    solution.assignments # returns assignments satisfying the formula (if any)
"""

from ._solvers import Assignment, SATSolution, SATSolver
from .dpll import DPLLSolver
