"""Provides classes to define Boolean formulas in different normal forms.

In classical logic, a normal form represents a Boolean expression in a simplified
form by replacing all complex logical operations with AND, OR and NOT operations.
Different normal forms exist. This module allows definition of the propositional
logic formulas in negation normal form (NNF) and conjunctive normal form (CNF).

    Typical usage example:

    foo = 'some Boolean expression'
    cnf = CNF(foo)
"""

from ._norm import CNF
from ._norm import NNF
