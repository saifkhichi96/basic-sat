class Lexer:
    tokens = (
        'LITERAL',
        'AND',
        'OR',
        'NOT',
        'IF',
        'LPAR',
        'RPAR',
    )

    precedence = (
        ('left', 'IF'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
    )

    # Lexer rules
    t_AND = r'&'
    t_OR = r'\|'
    t_NOT = r'!'
    t_IF = r'->'
    t_LITERAL = '[a-zA-Z]+'
    t_LPAR = r'\('
    t_RPAR = r'\)'

    # Ignore white space
    t_ignore = ' \t\n'
