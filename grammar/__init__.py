from ply import lex

from .lexer import Lexer


def t_FALSE(t):
    r'0'
    t.value = False
    return t


def t_TRUE(t):
    r'1'
    t.value = True
    return t

def t_error(p):
    raise SystemError(p)


def p_error(p):
    raise SyntaxError(p)


def p_expr_paren(p):
    '''expr : LPAR expr RPAR'''
    p[0] = p[2]


def p_expr_unary(p):
    '''expr : NOT expr          %prec NOT'''
    p[0] = [p[1], p[2]]


def p_expr_binop(p):
    '''expr : expr IF expr      %prec IF
            | expr BI expr      %prec BI
            | expr XOR expr     %prec XOR
            | expr OR expr      %prec OR
            | expr AND expr     %prec AND
            '''
    p[0] = [p[2], p[1], p[3]]


def p_expr_literal(p):
    '''expr : literal'''
    p[0] = p[1]


def p_literal(p):
    '''literal : FALSE
               | TRUE
               | LITERAL'''
    p[0] = p[1]


tokens = Lexer.tokens
precedence = Lexer.precedence

t_AND = Lexer.t_AND
t_OR = Lexer.t_OR
t_NOT = Lexer.t_NOT
t_IF = Lexer.t_IF
t_XOR = Lexer.t_XOR
t_BI = Lexer.t_BI

t_LPAR = Lexer.t_LPAR
t_RPAR = Lexer.t_RPAR
t_LITERAL = Lexer.t_LITERAL

t_ignore = Lexer.t_ignore


def create():
    lex.lex()
