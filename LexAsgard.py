import ply.lex as lex


reserved = (
    "using",
    "begin",
    "end",
    "of",
    "type",
    "from"
    "to"
    "repeat",
    "then",
    "otherwise",
    "done",
    "print",
    "while",
    "read",
    "with",
)

tokens = (
    "TkComa",
    "TkPuntoYComa"
    "TkParAbre",
    "TkParCierra",
    "TkMas",
    "TkMenos",
    "TkMult",
    "TkDiv",
    "TkMod",
    "TkConjuncion",
    "TkDisjuncion"
    "TkNegacion",
    "TkMenor",
    "TkMenorIgual",
    "TkMayor"
    "TkMayorIgual",
    "TkIgual",
    "TkDesigual",
    "TkConcatHorizontal",
    "TkConcatVertical",
    "TkRotacion",
    "TkTransposicion"
    "TkAsignacion",
    "TkIdent",
    "TkNumLit",
    "TkTrue",
    "TkFalse",
    "TkCanvasLit",
    "ID",
    "Comentario"
)

tokens += reserved

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = "Tk" + reserved[reserved.index(t.value)].capitalize()   # Check for reserved words
    return t

def t_Comentario(t):
    r'\{\-(.|\n)*?\-\}'
    pass

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n+'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

data = '''
end
begin
of type
{- Asignar al 35
el valor contador? -}

'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)