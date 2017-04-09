from ply import lex

from lexer import Lexer


def t_error(p):
    raise SystemError(p)


def p_error(p):
    raise SyntaxError(p)


def p_expr_unary(p):
    '''expr : NOT expr          %prec NOT'''
    p[0] = [p[1], p[2]]


def p_expr_binop(p):
    '''expr : expr OR expr      %prec OR
            | expr AND expr     %prec AND
            '''
    p[0] = [p[2], p[1], p[3]]


def p_expr_literal(p):
    '''expr : literal'''
    p[0] = p[1]


def p_literal(p):
    '''literal : LITERAL'''
    p[0] = p[1]


tokens = Lexer.tokens
precedence = Lexer.precedence

t_AND = Lexer.t_AND
t_OR = Lexer.t_OR
t_NOT = Lexer.t_NOT
t_LITERAL = Lexer.t_LITERAL

t_ignore = Lexer.t_ignore


def create():
    lex.lex()
