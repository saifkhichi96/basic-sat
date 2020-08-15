import argparse

from bsat import bsat_interactive, solve_file, solve_i


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Solves SATisfiability problems in propositional logic.')
parser.add_argument('-w', type=str, help='a PL formula to be solved')
parser.add_argument('-f', type=str, help='file with a list of PL formulas')

args = parser.parse_args()


def main():
    if args.f is not None:
        file = args.f
        print(file)
        results = solve_file(file.strip())
        for wff, (solvable, cnf, solutions) in results.items():
            print (wff, '=', cnf, end=' ')
            if solvable:
                print ('resolved with following assignments:')
                for i, solution in enumerate(solutions):
                    print("\t{})".format(i), solution)
            else:
                print ('is not solvable.')

    elif args.w is not None:
        wff = args.w
        solve_i(wff)

    else:
        bsat_interactive()


if __name__ == '__main__':
    main()
