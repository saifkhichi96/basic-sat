import getopt
import sys

from sat.instance import SATInstance


def solve(expression):
    try:
        # Find solutions of the wff
        sat = SATInstance(expression)
        solutions = sat.find_solutions()

        # If no solutions, input is unsatisfiable
        if sat.is_contradiction:
            print("\n[{}] =".format(expression), "[{}] is UNSATISFIABLE.".format(str(sat.formula)))

        # If solutions exists, print them
        else:
            print("\n[{}] =".format(expression), "[{}] is SATISFIED by following assignments:".format(str(sat.formula)))
            i = 1
            for solution in solutions:
                print("\t{})".format(i), solution)
                i += 1

    # Catch syntax errors
    except SyntaxError as se:
        print("//---------------------------------------------------//\n" \
              "// Input expression not well-formed and/or invalid   //\n" \
              "// operators used. For instructions, please see      //\n" \
              "// Readme. Exit with CTRL+C.                         //\n" \
              "//---------------------------------------------------//\n" \
              "Error message: {}".format(se))
    except SystemError as se:
        print("//---------------------------------------------------//\n" \
              "// Input expression contains invalid names. Literals //\n" \
              "// can only contain alphabets. For instructions, see //\n" \
              "// Readme. Exit with CTRL+C.                         //\n" \
              "//---------------------------------------------------//\n" \
              "Error message: {}".format(se))


def main():
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
            wff = input("\n\n(CTRL+C to exit) Enter a wff: ")
            solve(wff)
        except KeyboardInterrupt:
            print()
            break


def exec_file(file):
    try:
        f = open(file, "r")

        for wff in f.readlines():
            solve(wff.strip())
    except IOError as ie:
        print("File \"{}\" not found ... skipping".format(file))

if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "-hi:", ["ifile="])

        if len(opts) > 0:
            for opt, arg in opts:
                if opt == '-h':
                    print('USAGE:\n' \
                          '\tinteractive-mode: python main.py\n' \
                          '\trun-from-file: python main.py -i "<comma-separated inputfiles in quotes>"')
                    sys.exit(0)
                elif opt in ("-i", "--ifile"):
                    for file in arg.split(","):
                        exec_file(file.strip())
        else:
            main()
    except getopt.GetoptError:
        main()
