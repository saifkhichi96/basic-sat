from .NF import NF
from .logic.laws import de_morgans_law


class NNF(NF):
    def __init__(self, expr, from_proposition=False):
        NF.__init__(self, expr, from_proposition)

    def _build(self, expr):
        return de_morgans_law(expr)
