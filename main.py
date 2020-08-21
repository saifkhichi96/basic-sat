import argparse

from bsat.solvers import SATSolver, DPLLSolver

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Solves SATisfiability problems in propositional logic.')
parser.add_argument('-w', type=str, help='a PL formula to be solved')
parser.add_argument('-f', type=str, help='file with a list of PL formulas')

args = parser.parse_args()


def solve(proposition: str, solver: SATSolver):
    try:
        # Determine satisfiability
        problem = solver.solve(proposition)
        cnf, solution = problem.formula, problem.solution

        # Print satisfiability results
        print(f'{proposition} <=> {cnf}\n{solution}')

    except SyntaxError as err:
        print(f'Expression not well-formed: {err}')

    except RuntimeError as err:
        print(err)


def solve_file(file: str, solver: SATSolver):
    print(f'Solving Boolean expressions in file: {file}...')
    with open(file, "r") as f:
        for proposition in f.readlines():
            solve(proposition, solver)


def main():
    # Problems would be solved with the DPLLSolver
    solver = DPLLSolver()

    # case: solving all propositions in a file
    if args.f is not None:
        file = args.f.strip()
        solve_file(file, solver)

    # case: solving a single proposition
    elif args.w is not None:
        proposition = args.w.strip()
        solve(proposition, solver)

    # case: interactive SAT solver
    else:
        print("//---------------------------------------------------//\n"
              "//  BasicSAT - A 'very' basic SAT solver             //\n"
              "//                                                   //\n"
              "//                                                   //\n"
              "// For documentation and instructions on how to use  //\n"
              "// BasicSAT, please see Readme. Exit with CTRL+C.    //\n"
              "//---------------------------------------------------//")

        while True:
            try:
                # Get a propositional formula from user
                proposition = input("\n\n(CTRL+C to exit) Enter a proposition: ").strip()
                solve(proposition, solver)
            except KeyboardInterrupt:
                print()
                break


if __name__ == '__main__':
    main()
