"""Defines all the classes in the 'norm' package.

This is the internal definition of the package, with all the public and private classes defined here. \
Only the public classes are exported for external use.
"""
from abc import ABC, abstractmethod
from typing import List

from ..logic import Expression, ExpressionBuilder, Operators
from ..logic.grammar import PropositionParser
from ..logic.identities import simplify_operators
from ..logic.laws import de_morgans_law, distribute_ands


class _NF(ABC):
    """Abstract class representing a Boolean formula in a normal form (NF).

    Attributes:
        _expr: Internal representation of the formula in normal form.
    """
    _expr: Expression

    def __init__(self, formula: str):
        """Inits the NF formula.

        Args:
            formula: The Boolean formula to represent in normal form.
        """
        expr = ExpressionBuilder.from_proposition(formula)
        self._expr = self._build(expr)

    def __str__(self):
        """Returns a printable representation of the formula in normal form."""
        return str(self._expr)

    @property
    def max_solutions(self):
        """Maximum possible solutions for this formula.

        Number of possible solutions depends on the number of literals in the formula, N
        and is given by 2^N."""
        return 2 ** len(self._expr.literals)

    @property
    def parse_tree(self) -> List:
        """Parse tree of the NF formula as a preorder, nested list."""
        return self._get_tree(self._expr.parse_tree)

    def _get_tree(self, tree: List) -> List:
        """Internal accessor to calculate the 'parse_tree' property."""
        if isinstance(tree, list) and len(tree) >= 2:
            operator = PropositionParser.operations()[tree[0]]
            return [operator] + list(map(self._get_tree, tree[1:]))
        elif isinstance(tree, list) and len(tree) == 1:
            return self._get_tree(tree[0])
        else:
            return tree

    @abstractmethod
    def _build(self, expr: Expression) -> Expression:
        """Converts the Boolean formula into normal form.

        Args:
            expr: The formula to convert to the normal form.

        Returns:
            An equivalent formula represented in the normal form.
        """
        pass


class NNF(_NF):
    """Defines a Boolean formula in the negation normal form.

    In Boolean logic, a formula is in negation normal form if the negation operator (NOT) is
    only applied to variables and the only other allowed Boolean operators are conjunction
    (AND) and disjunction (OR)."""

    def __init__(self, formula: str):
        """Inits the NNF formula.

        Args:
            formula: The Boolean formula to represent in NNF.
        """
        _NF.__init__(self, formula)

    def _build(self, expr):
        """Converts the input formula to negation normal form.

        Every formula can be brought into this form by replacing implications and equivalences
        by their definitions, using De Morgan's laws to push negation inwards, and eliminating
        double negations.

        Args:
            expr: The formula to convert to NNF.

        Returns:
            An equivalent formula in negation normal form.
        """
        expr = simplify_operators(expr)
        return de_morgans_law(expr)


class CNF(_NF):
    """Defines a Boolean formula in the conjunctive normal form.

    In Boolean logic, a formula is in conjunctive normal form (CNF) or clausal normal form if
    it is a conjunction of one or more clauses, where a clause is a disjunction of literals;
    otherwise put, it is an AND of ORs."""

    def __init__(self, formula: str):
        """Inits the CNF formula.

        Args:
            formula: The Boolean formula to represent in CNF.
        """
        _NF.__init__(self, formula)

    def _build(self, expr):
        """Converts the input formula to conjunctive normal form.

        Every propositional formula can be converted into an equivalent formula that is in CNF
        based on rules about logical equivalences: double negation elimination, De Morgan's laws,
        and the distributive law.

        Args:
            expr: The formula to convert to CNF.

        Returns:
            An equivalent formula in conjunctive normal form.
        """
        for i in range(3):
            expr = distribute_ands(NNF(str(expr))._expr)

        return expr

    @property
    def clauses(self):
        """List of clauses in the CNF."""
        clauses = []
        for c in self._get_clauses(self._expr.parse_tree).split('\n'):
            c = c.strip()
            if c != '':
                clauses.append(c)

        return clauses

    def _get_clauses(self, tree: List, eof: bool = False) -> str:
        """Internal accessor to calculate the 'clauses' property.

        Args:
            tree: Parse tree of the formula to find clauses in.
            eof: Optional; Line break is added after the clause if True.

        Returns:
            List of all the clauses in the formula, represented as a single string.
        """
        clause = []
        if isinstance(tree, list):
            if len(tree) == 3:
                op, t1, t2 = tuple(tree)
                clause.append(self._get_clauses(t1, op == Operators.AND))
                clause.append(self._get_clauses(t2, op == Operators.AND))

            elif len(tree) == 2:
                op, val = tuple(tree)
                clause.append(f'{op}{self._get_clauses(val)}')

        else:
            clause.append('{}  '.format(str(tree)))

        clause = ''.join(clause).replace('\n\n', '\n').strip()
        if eof and len(clause.strip()) != 0:
            clause += '\n'

        return clause

    @property
    def dimacs(self) -> str:
        """The DIMACS CNF representation of the CNF formula."""
        clauses = self.clauses

        raw = ''
        for clause in clauses:
            raw += clause.replace(str(Operators.NOT), '-') + '  0\n'

        literals = self._expr.literals
        for lt in literals:
            raw = raw.replace(lt, f'{literals.index(lt) + 1}')

        return "c the CNF formula '{}'\n" \
               'c in DIMACS format' \
               'c' \
               'p cnf {} {}\n' \
               '{}'.format(str(self),
                           len(literals),
                           len(clauses),
                           raw)

    def __str__(self):
        """See base class."""
        string = ''

        clauses = self.clauses
        for i, clause in enumerate(clauses):
            string += '('
            for j, item in enumerate(clause.split(' ')):
                item = item.strip()
                if item != '' and item != Operators.NOT:
                    string += item
                    string += f' {Operators.OR} '
            string = string[:-3]
            string += ')'
            if i + 1 != len(clauses):
                string += f' {Operators.AND} '

        return string
