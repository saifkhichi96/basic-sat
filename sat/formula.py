# operators:
from grammar.parser import Parser

IFF = "<->"
IMPLIES = "->"
XOR = "+"
NOT = "!"
OR = "|"
AND = "&"


class FormulaFactory:
    @classmethod
    def __check_primitive(self, proposition):
        return isinstance(proposition, str) or isinstance(proposition, bool) or (
        isinstance(proposition, list) and len(proposition) == 1)

    @classmethod
    def create(cls, proposition):
        # type: (list) -> (Formula, None)
        if proposition is None:
            return None

        if FormulaFactory.__check_primitive(proposition):
            return Formula(proposition)

        elif proposition[0] == NOT:
            return UnaryFormula(proposition)

        else:
            return BinaryFormula(proposition)

    @classmethod
    def create_cnf(cls, proposition):
        # type: (list) -> (CNFFormula, None)
        if proposition is None:
            return None

        return CNFFormula(FormulaFactory.create(Parser().parse(proposition)))


class Formula:
    def __init__(self, proposition):
        self.expression = proposition
        self.operator = None
        self.first = None
        self.second = None

    def __str__(self):
        self.__string = ""
        self.__to_string(self.expression)
        return self.__string

    def __to_string(self, tree):
        if isinstance(tree, str):
            self.__string += tree
        elif isinstance(tree, list):
            if len(tree) == 3:
                self.__string += "("
                self.__to_string(tree[1])
                self.__string += " " + tree[0] + " "
                self.__to_string(tree[2])
                self.__string += ")"
            elif len(tree) == 2:
                self.__string += tree[0]
                self.__to_string(tree[1])


class UnaryFormula(Formula):
    def __init__(self, proposition):
        Formula.__init__(self, proposition)
        self.operator = proposition[0]
        self.first = FormulaFactory.create(proposition[1])
        self.second = None


class BinaryFormula(Formula):
    def __init__(self, proposition):
        Formula.__init__(self, proposition)
        self.operator = proposition[0]
        self.first = FormulaFactory.create(proposition[1])
        self.second = FormulaFactory.create(proposition[2])


class CNFFormula(Formula):
    def __init__(self, formula):
        # type: (Formula) -> None
        expression = self.__convert(
            self.__implication_elimination_law(self.__biconditional_elimination(self.__xor_elimination(formula))))
        Formula.__init__(self, expression)

    def __convert(self, formula):
        # type: (Formula) -> list
        if isinstance(formula, BinaryFormula):
            first = FormulaFactory.create(self.__convert(formula.first))
            second = FormulaFactory.create(self.__convert(formula.second))

            if formula.operator == AND:
                answer = [AND, first.expression, second.expression]
            else:
                answer = self.__distributive_law(first, second)
        elif isinstance(formula, UnaryFormula):
            answer = self.__not_elimination_law(FormulaFactory.create(self.__de_morgans_law(formula)))
        else:
            answer = formula.expression

        return answer

    def __xor_elimination(self, formula):
        # type: (Formula) -> (Formula, None)
        if formula is None:
            return None

        if isinstance(formula, BinaryFormula):
            first = self.__xor_elimination(formula.first).expression
            second = self.__xor_elimination(formula.second).expression

            if formula.operator == XOR:
                result = [NOT, [IFF, first, second]]
            else:
                result = [formula.operator, first, second]

        elif isinstance(formula, UnaryFormula):
            first = self.__xor_elimination(formula.first).expression
            result = [NOT, first]

        else:
            result = formula.expression

        return FormulaFactory.create(result)

    def __biconditional_elimination(self, formula):
        # type: (Formula) -> (Formula, None)
        if formula is None:
            return None

        if isinstance(formula, BinaryFormula):
            first = self.__biconditional_elimination(formula.first).expression
            second = self.__biconditional_elimination(formula.second).expression

            if formula.operator == IFF:
                result = [AND, [IMPLIES, first, second], [IMPLIES, second, first]]
            else:
                result = [formula.operator, first, second]

        elif isinstance(formula, UnaryFormula):
            first = self.__biconditional_elimination(formula.first).expression
            result = [NOT, first]

        else:
            result = formula.expression

        return FormulaFactory.create(result)

    def __implication_elimination_law(self, formula):
        # type: (Formula) -> (Formula, None)
        if formula is None:
            return None

        if isinstance(formula, BinaryFormula):
            first = self.__implication_elimination_law(formula.first).expression
            second = self.__implication_elimination_law(formula.second).expression

            if formula.operator == IMPLIES:
                result = [OR, [NOT, first], second]
            else:
                result = [formula.operator, first, second]

        elif isinstance(formula, UnaryFormula):
            first = self.__implication_elimination_law(formula.first).expression
            result = [NOT, first]

        else:
            result = formula.expression

        return FormulaFactory.create(result)

    def __distributive_law(self, f1, f2):
        # type: (Formula, Formula) -> list
        if f1.operator == AND:
            answer = [AND, self.__distributive_law(f1.first, f2), self.__distributive_law(f1.second, f2)]
        elif f2.operator == AND:
            answer = [AND, self.__distributive_law(f1, f2.first), self.__distributive_law(f1, f2.second)]
        else:
            answer = [OR, f1.expression, f2.expression]
        return answer

    def __de_morgans_law(self, f1):
        # type: (Formula) -> list
        if isinstance(f1, UnaryFormula) and isinstance(f1.first, BinaryFormula):
            if f1.first.operator == AND:
                answer = [OR,
                          [NOT, self.__de_morgans_law(f1.first.first) if isinstance(f1.first.first,
                                                                                    UnaryFormula) else f1.first.first.expression],
                          [NOT, self.__de_morgans_law(f1.first.second) if isinstance(f1.first.second,
                                                                                     UnaryFormula) else f1.first.second.expression]]
            else:
                answer = [AND,
                          [NOT, self.__de_morgans_law(f1.first.first) if isinstance(f1.first.first,
                                                                                    UnaryFormula) else f1.first.first.expression],
                          [NOT, self.__de_morgans_law(f1.first.second) if isinstance(f1.first.second,
                                                                                     UnaryFormula) else f1.first.second.expression]]

        else:
            answer = f1.expression

        return answer

    def __not_elimination_law(self, f1):
        # type: (Formula) -> list
        if isinstance(f1, UnaryFormula) and isinstance(f1.first, UnaryFormula):
            answer = f1.first.expression[-1]

        elif isinstance(f1, BinaryFormula):
            answer = [f1.operator, self.__not_elimination_law(f1.first), self.__not_elimination_law(f1.second)]

        else:
            answer = f1.expression

        return answer
