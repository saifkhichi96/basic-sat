#!/bin/bash
pydoc -w bsat
mv bsat.html docs/index.html

pydoc -w bsat.logic
mv bsat.logic.html docs/

pydoc -w bsat.logic.grammar
mv bsat.logic.grammar.html docs/

pydoc -w bsat.logic.grammar._lexer
mv bsat.logic.grammar._lexer.html docs/

pydoc -w bsat.logic.grammar._parser
mv bsat.logic.grammar._parser.html docs/

pydoc -w bsat.logic._logic
mv bsat.logic._logic.html docs/

pydoc -w bsat.logic.identities
mv bsat.logic.identities.html docs/

pydoc -w bsat.logic.laws
mv bsat.logic.laws.html docs/

pydoc -w bsat.norm
mv bsat.norm.html docs/

pydoc -w bsat.norm._norm
mv bsat.norm._norm.html docs/

pydoc -w bsat.solvers
mv bsat.solvers.html docs/

pydoc -w bsat.solvers._solvers
mv bsat.solvers._solvers.html docs/

pydoc -w bsat.solvers.dpll
mv bsat.solvers.dpll.html docs/

pydoc -w bsat.utils
mv bsat.utils.html docs/
