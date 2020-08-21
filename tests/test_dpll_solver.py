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
                solution = solver.solve(proposition)
                results[proposition] = solution.problem, solution

        return results

    def test_contradictions(self):
        results = self.solve_file(self.__files_path + 'contradiction.txt')
        for formula, (_, solution) in results.items():
            self.assertEqual(False, solution, formula + ' is satisfiable by ' + str(solution))

    def test_tautologies(self):
        results = self.solve_file(self.__files_path + 'tautology.txt')
        for formula, (_, solution) in results.items():
            self.assertEqual(True, solution, f'{formula} not a tautology but {solution}')

    def test_satisfiable_formulas(self):
        results = self.solve_file(self.__files_path + 'satisfiable.txt')
        for formula, (_, solution) in results.items():
            self.assertGreater(len(solution), 0, f'{formula} {solution}')
