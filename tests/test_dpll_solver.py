import os
from unittest import TestCase

from solvers import DPLLSolver


class SolverTests(TestCase):
    __files_path = os.path.dirname(os.path.realpath(__file__)) + '/examples/'

    def solve_file(self, file: str):
        solver = DPLLSolver()
        results = {}
        with open(file, "r") as f:
            for proposition in f.readlines():
                problem = solver.solve_proposition(proposition)
                results[proposition] = (not problem.is_contradiction), problem.formula, problem.solutions

        return results

    def test_contradictions(self):
        results = self.solve_file(self.__files_path + 'contradiction.txt')
        for formula, (solvable, _, solutions) in results.items():
            self.assertFalse(solvable, formula + ' is satisfiable by ' + str(solutions))

    def test_tautologies(self):
        results = self.solve_file(self.__files_path + 'tautology.txt')
        for formula, (solvable, _, _) in results.items():
            self.assertTrue(solvable, formula + ' is UNSAT')

    def test_satisfiable_formulas(self):
        results = self.solve_file(self.__files_path + 'satisfiable.txt')
        for formula, (solvable, _, _) in results.items():
            self.assertTrue(solvable, formula + ' is UNSAT')
