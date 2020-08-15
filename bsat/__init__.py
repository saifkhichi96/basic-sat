from .instance import *
from .solver import *


def solve(expression, verbose=False):
    # Find solutions of the wff
    sat = SATInstance(expression)
    solutions = sat.find_solutions()

    return not sat.is_contradiction, sat.formula, solutions


def solve_file(file):
    results = {}
    with open(file, "r") as f:
        for wff in f.readlines():
            wff = wff.strip()
            results[wff] = solve(wff)

    return results


def solve_i(expression):
    try:
        # Find solutions of the wff
        solvable, cnf, solutions = solve(expression)

        # If solutions exists, print them
        if solvable:
            print("\n{}".format(expression), "<=> {} is SAT with following assignments:".format(cnf))
            for i, solution in enumerate(solutions):
                print("\t{})".format(i+1), solution)

        # If no solutions, input is unsatisfiable
        else:
            print("\n[{}] =".format(expression), "[{}] is UNSAT.".format(cnf))

    # Catch syntax errors
    except SyntaxError as se:
        print("SyntaxError: Expression not well-formed. See README for allowed operators. {}".format(se))

    except SystemError as se:
        print("SystemError: Literal names can only contain alphabets. {}".format(se))


def bsat_interactive():
    welcome = "//---------------------------------------------------//\n" \
              "//  BasicSAT - A \"very\" basic SAT solver             //\n" \
              "//                                                   //\n" \
              "//                                                   //\n" \
              "// For documentation and instructions on how to use  //\n" \
              "// BasicSAT, please see Readme. Exit with CTRL+C.    //\n" \
              "//---------------------------------------------------//"

    print(welcome)
    while True:
        try:
            # Get a wff formula from user
            wff = input("\n\n(CTRL+C to exit) Enter a wff: ").strip()
            solve_i(wff)
        except KeyboardInterrupt:
            print()
            break
