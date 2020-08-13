from .formula import FormulaFactory
from grammar.parser import Parser
from .solver import SATSolver


class SATInstance:
    def __init__(self, exprstr):
        self.wff = self.__clean(exprstr)
        self.is_contradiction = False

    def __clean(self, string):
        string = string.replace("\n", " ")
        while True:
            r = string.replace("  ", " ")
            if r == string:
                break
            string = r

        return string

    def __get_expression(self, tree):
        if isinstance(tree, list) and len(tree) >= 2:
            operator = Parser().operations[tree[0]]
            return [operator] + list(map(self.__get_expression, tree[1:]))
        elif isinstance(tree, list) and len(tree) == 1:
            return self.__get_expression(tree[0])
        else:
            return tree

    def find_solutions(self):
        self.formula = FormulaFactory.create_cnf(self.wff)
        solutions = SATSolver().solve(self.__get_expression(self.formula.expression))
        assignments = []
        count = 0
        for solution in solutions:
            if isinstance(solution, bool):
                assignments.append(str(solution))
            else:
                s = ""
                count = len(solution.keys())
                for k, v in zip(solution.keys(), solution.values()):
                    s += k + " = " + str(1 if v else 0) + ", "
                assignments.append(s[:-2])

        self.is_contradiction = len(assignments) == 0
        return assignments
