from grammar.parser import Parser
from solver import SATSolver


class SATInstance:
    def __init__(self, exprstr):
        self.parser = Parser()
        self.exprstr = self.__clean(exprstr)
        self.is_contradiction = False
        self.is_tautology = False

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
            operator = self.parser.operations[tree[0]]
            return [operator] + map(self.__get_expression, tree[1:])
        elif isinstance(tree, list) and len(tree) == 1:
            return self.__get_expression(tree[0])
        else:
            return tree

    def find_solutions(self):
        tree = self.parser.parse(self.exprstr)
        solutions = SATSolver().solve(self.__get_expression(tree))
        assignments = []
        count = 0
        for solution in solutions:
            s = ""
            count = len(solution.keys())
            for k, v in zip(solution.keys(), solution.values()):
                s += k + " = " + str(1 if v else 0) + ", "
            assignments.append(s[:-2])

        self.is_contradiction = len(assignments) == 0
        self.is_tautology = len(assignments) == 2 ** count
        return assignments
