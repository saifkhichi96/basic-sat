from sat.instance import SATInstance


def main():
    welcome = "//---------------------------------------------------//\n" \
              "//  BasicSAT - A \"very\" basic SAT solver             //\n" \
              "//    (Assignment #2, SE320)                         //\n" \
              "//                                                   //\n" \
              "//                  Muhammad Saifullah Khan (111453) //\n" \
              "//                              Mansoor Ali (111290) //\n" \
              "//---------------------------------------------------//\n" \
              "// For documentation and instructions on how to use  //\n" \
              "// BasicSAT, please see Readme. Exit with CTRL+C.    //\n" \
              "//---------------------------------------------------//"

    print welcome
    while True:
        try:
            # Get a wff formula from user
            wff = raw_input("\n\n(CTRL+C to exit) Enter a wff: ")

            # Find solutions of the wff
            sat = SATInstance(wff)
            solutions = sat.find_solutions()

            # If no solutions, input is unsatisfiable
            if sat.is_contradiction:
                print "\n[{}] =".format(wff), "[{}] is UNSATISFIABLE.".format(str(sat.formula))

            # If solutions exists, print them
            else:
                print "\n[{}] =".format(wff), "[{}] is SATISFIED by following assignments:".format(str(sat.formula))
                i = 1
                for solution in solutions:
                    print "\t{})".format(i), solution
                    i += 1

        # Catch syntax errors
        except SyntaxError, se:
            print "//---------------------------------------------------//\n" \
                  "// Input expression not well-formed and/or invalid   //\n" \
                  "// operators used. For instructions, please see      //\n" \
                  "// Readme. Exit with CTRL+C.                         //\n" \
                  "//---------------------------------------------------//\n" \
                  "Error message: {}".format(se)
        except SystemError, se:
            print "//---------------------------------------------------//\n" \
                  "// Input expression contains invalid names. Literals //\n" \
                  "// can only contain alphabets. For instructions, see //\n" \
                  "// Readme. Exit with CTRL+C.                         //\n" \
                  "//---------------------------------------------------//\n" \
                  "Error message: {}".format(se)
        except KeyboardInterrupt:
            print
            break


if __name__ == '__main__':
    main()
