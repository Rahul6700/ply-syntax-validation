import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'IDENTIFIER', 'ASSIGN', 'NUMBER', 'FLOATNUM', 'PLUS', 'MINUS', 'PRODUCT','DIVIDE', 'LPAREN', 'RPAREN', 'LESS', 
    'NEWLINE', 'DEF', 'RETURN', 'WHILE', 'IF', 'ELSE', 'FOR', 'COLON', 'COMMA', 'STRING',
    'IN', 'RANGE', 'MORE', 'TRUE', 'FALSE', 'BREAK'
)

reserved = {
    'def': 'DEF',
    'return': 'RETURN',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'in': 'IN',
    'range': 'RANGE',
    'True' : 'TRUE',
    'False': 'False',
    'break': 'BREAK'

}

t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_PRODUCT = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LESS = r'<'
t_MORE = r'>'
t_COLON = r':'
t_COMMA = r','

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER') 
    return t

def t_FLOATNUM(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_assignment(p):
    'statement : IDENTIFIER ASSIGN expression'
    print(f"Valid assignment: {p[1]} = {p[3]}")

# Expression
def p_expression(p):
    '''expression : NUMBER
                  | FLOATNUM
                  | STRING
                  | IDENTIFIER
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression PRODUCT expression
                  | expression DIVIDE expression
                  | expression LESS NUMBER
                  | expression MORE NUMBER'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]} {p[2]} {p[3]}"
def p_return_statement(p):
    '''statement : RETURN expression
                 | RETURN TRUE
                 | RETURN FALSE'''
    print(f"Valid return statement: {p[2]}")
def p_break_statement(p):
    'statement : BREAK'
    print(f"Valid return statement: {p[2]}")

def p_function_definition(p):
    'statement : DEF IDENTIFIER LPAREN param_list RPAREN COLON NEWLINE statement_list'
    print(f"Valid function declaration: {p[2]} with parameters {p[4]}")

def p_param_list(p):
    '''param_list : IDENTIFIER COMMA param_list
                  | IDENTIFIER
                  what does return in python give| empty'''
    p[0] = [p[1]] + p[3] if len(p) == 4 else [p[1]] if p else []

def p_statement_list(p):
    '''statement_list : statement NEWLINE statement_list
                      | statement
                      | empty'''
    pass

def p_if_statement(p):
    '''statement : IF LPAREN expression RPAREN COLON NEWLINE statement_list
                 | IF LPAREN expression RPAREN COLON NEWLINE statement_list ELSE COLON NEWLINE statement_list'''
    if len(p) == 8:
        print("Valid if statement")
    else:
        print("Valid if-else statement")

def p_while_loop(p):
    '''statement : WHILE expression COLON NEWLINE statement_list
                 | WHILE TRUE'''
    print("Valid while loop")

def p_for_loop(p):
    '''statement : FOR IDENTIFIER IN RANGE LPAREN NUMBER COMMA NUMBER RPAREN COLON NEWLINE statement_list
                 | FOR IDENTIFIER IN IDENTIFIER COLON NEWLINE statement_list'''
    print(f"Valid for loop with iterator {p[2]} ")

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()
test_cases = [
    "x = -10",                  
    "y = 3.14",                
    'name = "Alice"',          
    "def add(a, b):\n\treturn a + b",  
    "if (x < 5):\n\tx = x + 1\nelse:\n\tx = x - 2",         
    "while x < 5 :\n\tx = x + 1",     
    "for i in range(0, 10):\n\tx = x + i",  
]
def test_parser():
    for test in test_cases:
        print(f"Testing: {test}")
        parser.parse(test)
        print("\n")
test_parser()
