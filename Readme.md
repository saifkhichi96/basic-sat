# BasicSAT: A _very_ basic SAT Solver in Python

BasicSAT is a simple SAT solver written in Python. It uses a very naive implementation of [DPLL algorithm](https://en.wikipedia.org/wiki/DPLL_algorithm) to find satisfiability of a given [propositional formula](https://en.wikipedia.org/wiki/Propositional_formula).

BasicSAT has two independent modules: a CNF maker and a SAT solver. All input PL statements are first converted to conjunctive normal form (CNF) before being given to the SAT solver to determine its satisfiability.

## Releases
| Version | Description |
| :-----: | :---------- |
| [v1.0.0](https://github.com/saifkhichi96/basic-sat/releases/tag/v1.0.0) | Initial version of the project, written in Python2.7. |
| [v2.0.0](https://github.com/saifkhichi96/basic-sat/releases/tag/v2.0.0) | Project upgraded to Python3. |

## Prerequisites
This project requires Python3 and uses the [ply.yacc](http://www.dabeaz.com/ply/) package for parsing input formulas and generating their parse trees. Before you proceed, make sure that you have the required package installed on your machine.

You should be able to install it by running `pip install ply`. For details, visit its [website](http://www.dabeaz.com/ply/).

## How to Run
The project can be run in a number of different modes.

To run the project:
1) Clone the repository to your local filesystem using `git clone https://github.com/saifkhichi96/basic-sat.git`.
2) Change current directory using `cd basic-sat`.

### Interactive Mode
SAT solver can also be started in interactive mode. In this mode, user can write a propositional formula interactively and get its assignments (if any).

To run the program in interactive mode, use the command:
````
$  python main.py
````
Interactive mode enters the program into an infinte loop which can be exited by pressing `CTRL+C` buttons.

### From a File
To execute formulas listed in a file, use the following command:
````
$  python main.py -i "<comma-separted-list-of-files>"
````

For example, executing `python main.py -i "file1, file2"` would test all the formulas defined in `file1` and `file2`. Input files must have only one formula written on each line, and nothing else in the file.

Formulas must use valid syntax and semantics as defined below. Formulas which are not well-formed or use invalid symbols raise SyntaxError exceptions.

### Examples
The project contains sample PL formulas in `examples/` directory which can be run using the following command from terminal:
````
$  chmod u+w run-examples.sh
$  ./run-examples.sh
````
This would solve all the formulas from the `examples/` directory and print their results: `Unsatisfiable` or `Satisfiable`.

For satisfiable formulas, assignments that satisfy the formula are also listed.


## Semantics
BasicSAT expects input formulas to follow a certain syntax. The following sections describe allowed and forbidden symbols.

### Connectors
BasicSAT can solve formulas with unary and binary operators listed below. Symbol to be used for each operation is written opposite to its name.

#### Unary Operators
1) Negation (!)

#### Binary Operators
1) Conjunction (&)
2) Disjunction (|)
3) Implication (->)
4) Biconditional (<->)
5) XOR (+)

### Symbols
#### Variables
Symbols used to represent propositions must be subsets of regex `\[a-zA-Z]+`. That is, they can only be alphabetic. No numbers or special characters are supported.

#### Brackets
Parentheses `()` are supported in expressions, but brackets `[]` and braces `{}` are not.

#### Constants
Use `1` to represent `True` and `0` to represent `False` in a propositional formula.

### Help
To access help from command-line, use the command:
````
$  python main.py -h
````
To view complete documentation from command-line, on Linux use the command:
````
$  cat Readme.md | less
````

### Efficiency
SAT is a NP-complete problem. This project converts an input formula into a CNF in linear time, `O(n)`. However, solving the CNF is not very efficient.
