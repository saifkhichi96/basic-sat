"""Implements a solver for SAT problems based the DPLL algorithm.
"""
from ..norm import CNF
from ._solvers import SATSolver, SATSolution


class DPLLSolver(SATSolver):
    """Implements a CNF-SAT solver using the DPLL algorithm.

    The Davis–Putnam–Logemann–Loveland (DPLL) algorithm is a complete, backtracking-based search algorithm for deciding
    the satisfiability of propositional logic formulae in conjunctive normal form. This algorithm is implemented here
    to solve the CNF-SAT problems.
    """

    def _solve(self, problem: CNF) -> SATSolution:
        """See base class."""
        parse_tree = problem.parse_tree
        assignments = list(self._find_solutions(parse_tree, dict()))
        solution = SATSolution(problem, assignments)
        return solution

    def _find_solutions(self, F, bindings):
        F = self.__minimize(F, bindings)

        if F is True:
            yield bindings or F
            return
        elif F is False:
            return

        L = self.__next_unbound(F)

        bindings1 = bindings.copy()
        bindings1[L] = True
        for sat in self._find_solutions(F, bindings1):
            yield sat

        bindings2 = bindings.copy()
        bindings2[L] = False
        for sat in self._find_solutions(F, bindings2):
            yield sat

    def __minimize(self, F, bindings, infer=True):
        if isinstance(F, list):
            fn = F[0]
            args = [self.__minimize(a, bindings, infer) for a in F[1:]]
            r = fn(*args)
            if r is not None and infer:
                return r
            else:
                return [fn] + args
        elif isinstance(F, str) and F in bindings:
            return bindings[F]
        else:
            return F

    def __yield_unbounds(self, F):
        all_unbounds = []
        if isinstance(F, list):
            for arg in F[1:]:
                for unbound in self.__yield_unbounds(arg):
                    if unbound not in all_unbounds:
                        all_unbounds.append(unbound)
                        yield unbound
        elif isinstance(F, str):
            all_unbounds.append(F)
            yield F

    def __next_unbound(self, F):
        for unbound in self.__yield_unbounds(F):
            return unbound
        raise StopIteration
