# operators:
from grammar.parser import Parser

IMPLIES = "->"
NOT = "!"
OR = "|"
AND = "&"


class FormulaFactory:
    @classmethod
    def __check_primitive(self, proposition):
        return isinstance(proposition, str) or (isinstance(proposition, list) and len(proposition) == 1)

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
        elif isinstance(tree, list) and len(tree) == 3:
            self.__string += "("
            self.__to_string(tree[1])
            self.__string += " " + tree[0] + " "
            self.__to_string(tree[2])
            self.__string += ")"
        else:
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
        expression = self.__convert(self.__replace_implication(formula))
        Formula.__init__(self, expression)

    def __replace_implication(self, formula):
        # type: (Formula) -> (Formula, None)

        """
        Removes implications by using the equivalence:
            p -> q  -||-  !p v q
        """
        if formula is None:
            return None

        if isinstance(formula, BinaryFormula):
            first = self.__replace_implication(formula.first).expression
            second = self.__replace_implication(formula.second).expression

            if formula.operator == IMPLIES:
                result = [OR, [NOT, first], second]
            else:
                result = [formula.operator, first, second]

        else:
            result = formula.expression

        return FormulaFactory.create(result)

    def __convert(self, formula):
        # type: (Formula) -> list
        if isinstance(formula, BinaryFormula):
            first = FormulaFactory.create(self.__convert(formula.first))
            second = FormulaFactory.create(self.__convert(formula.second))

            if formula.operator == AND:
                return [AND, first.expression, second.expression]
            else:
                return self.__distribute_or(first, second)
        else:
            return formula.expression

    def __distribute_or(self, f1, f2):
        # type: (Formula, Formula) -> list
        if f1.operator == AND:
            answer = [AND, self.__distribute_or(f1.first, f2), self.__distribute_or(f1.second, f2)]
        elif f2.operator == AND:
            answer = [AND, self.__distribute_or(f1, f2.first), self.__distribute_or(f1, f2.second)]
        else:
            answer = [OR, f1.expression, f2.expression]
        return answer
