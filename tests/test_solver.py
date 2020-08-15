import os
import unittest
import sys

from bsat import solve_file


dir_path = os.path.dirname(os.path.realpath(__file__))


class ContradictionsTestCase(unittest.TestCase):
    def runTest(self):
        print('Testing UNSAT formulas...')
        results = solve_file(dir_path + '/examples/contradiction.txt')
        for wff, (solvable, cnf, solutions) in results.items():
            print (wff, '<=>', cnf, 'SAT' if solvable else 'UNSAT')
            self.assertFalse(solvable, wff + ' is satisfiable by ' + str(solutions))
        print()


class TautologyTestCase(unittest.TestCase):
    def runTest(self):
        print('Testing tautologies (i.e. always SAT)...')
        results = solve_file(dir_path + '/examples/tautology.txt')
        for wff, (solvable, cnf, solutions) in results.items():
            print (wff, '<=>', cnf, 'SAT' if solvable else 'UNSAT', f' solutions={solutions}')
            self.assertTrue(solvable, wff + ' is UNSAT')
        print()


class SatisfiableTestCase(unittest.TestCase):
    def runTest(self):
        print('Testing SAT formulas...')
        results = solve_file(dir_path + '/examples/satisfiable.txt')
        for wff, (solvable, cnf, solutions) in results.items():
            print (wff, '<=>', cnf, 'SAT' if solvable else 'UNSAT', f' solutions={solutions}')
            self.assertTrue(solvable, wff + ' is UNSAT')
        print()
