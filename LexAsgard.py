import ply.lex as lex

# Diccionario para las palabras reservadas, donde tenemos como llaves las que están en el código y como valores las resultantes de la especificación

reserved = {
    "using": "TkUsing",
    "begin": "TkBegin",
    "end": "TkEnd",
    "of": "TkOf",
    "type": "TkType",
    "from": "TkFrom",
    "to": "TkTo",
    "repeat": "TkRepeat",
    "then": "TkThen",
    "otherwise": "TkOtherwise",
    "done": "TkDone",
    "print": "TkPrint",
    "while": "TkWhile",
    "read": "TkRead",
    "with": "TkWith",
}

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
    "Reservada",
    "Comentario"
)

tokens += tuple(reserved.values())

def t_Reservada(t):
    r'[a-zA-Z_]+'
    t.type = reserved.get(t.value)   # Buscamos las palabras reservadas
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