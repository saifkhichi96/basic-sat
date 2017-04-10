class Lexer:
    tokens = (
        'LITERAL',
        'AND',
        'OR',
        'NOT',
        'IF',
        'BI',
        'XOR',
        'LPAR',
        'RPAR',
        'FALSE',
        'TRUE'
    )

    precedence = (
        ('left', 'BI'),
        ('left', "XOR"),
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
    t_XOR = r'\+'
    t_BI = r'<->'
    t_LITERAL = '[a-zA-Z]+'
    t_LPAR = r'\('
    t_RPAR = r'\)'

    # Ignore white space
    t_ignore = ' \t\n'
