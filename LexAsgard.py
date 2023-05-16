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
    "TkPuntoYComa",
    "TkParAbre",
    "TkParCierra",
    "TkMas",
    "TkMenos",
    "TkMult",
    "TkDiv",
    "TkMod",
    "TkConjuncion",
    "TkDisjuncion",
    "TkNegacion",
    "TkMenor",
    "TkMenorIgual",
    "TkMayor",
    "TkMayorIgual",
    "TkIgual",
    "TkDesigual",
    "TkConcatHorizontal",
    "TkConcatVertical",
    "TkRotacion",
    "TkTransposicion",
    "TkAsignacion",
    "TkIdent",
    "TkNumLit",
    "TkTrue",
    "TkFalse",
    "TkCanvasLit",
    "TkIdent",
    "ID",
    "Comentario",
    
)

tokens += tuple(reserved.values())

def t_TkIdent(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')   # Buscamos las palabras reservadas
    return t

def t_TkCanvasLit(t):
    r'<empty>|<[\\\|\/\.\_]>'
    return t

t_TkNumLit = r'[0-9]+'

def t_Comentario(t):
    r'\{\-(.|\n)*?\-\}'
    pass

# Definimos las demás reglas para los tokens sencillos
t_TkComa = r','

#t_TkPuntoYComa = r'\;'

t_TkParAbre = r'\('

t_TkParCierra = r'\)'

t_TkMas = r'\+'

t_TkMenos = r'\-'

t_TkMult = r'\*'

t_TkDiv = r'\/'

t_TkMod = r'\%'

t_TkConjuncion = r'\/\\'

t_TkDisjuncion = r'\\\/'

t_TkNegacion = r'\^'

t_TkMenor = r'\<'

t_TkMenorIgual = r'\<='

t_TkMayor = r'\>'

t_TkMayorIgual = r'\>='

t_TkIgual = r'\='

t_TkDesigual = r'\!='

t_TkConcatHorizontal = r'\:'

t_TkConcatVertical = r'\|'

t_TkRotacion = r'\$'

t_TkTransposicion = r'\''

t_TkAsignacion = r'\:='


# Ignoramos los espacios, los tabuladores y los saltos de línea
t_ignore  = ' \t\n+'

# Regla para manejar los errores (provisional)
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


# De acá para abajo es el testing
data = '''
using contador begin <o>
{- Asignar al contador
el valor 35. -}
contador := 35
end
'''

lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)