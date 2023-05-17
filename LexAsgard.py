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

t_TkPuntoYComa = r'\;'

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

# Calculamos cada línea
def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Calculamos las columnas
#     input es el texto ingresado
#     token es la instancia del token a buscar

def find_column(input, token):
    comienzo = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - comienzo) + 1

# Lista para almacenar los tokens y valores de cada error
errores = []

# Regla para manejar los errores, almacenandolos en una lista
def t_error(t):
    errores.append(t)
    t.lexer.skip(1)

# Creamos el lexer, silenciando los warnings
lexer = lex.lex(errorlog=lex.NullLogger())


# De acá para abajo es el testing
data = '''
using contador! begin
  contador ?:= 35
end
'''

lexer.input(data)

# Lista de tokens para imprimir al final
tokens_salida = []

# Primeramente, creamos los tokens
while True:
    # Creamos el token
    tok = lexer.token()

    if not tok: 
        break   # No hay más input para crear tokens    

    # Dependiendo de su tipo, lo almacenamos en errores o en la salida normal
    if tok.type == "error":
        errores.append(tok)
    else:
        tokens_salida.append(tok)


# Ahora, realizamos la verificación y el printing correspondiente

# Las listas vacias en python evaluan a false
if bool(errores) is False:
    # La lista de errores está vacía, es decir, no hay errores.
    # Asi, imprimimos los tokens encontrados
    for token in tokens_salida:
        if token.type == "TkNumLit":
            print(token.type + f"({token.value})", end=" ")
            continue
        if token.type == "ID":
            print(f'TkIdent("{token.value}")', end=" ")
            continue
        else:
            print(token.type, end=" ")
            continue

    print("")
else:
    # La lista de errores NO está vacía
    # Así, imprimimos los errores encontrados
    for error in errores:
        print(f'Error: Caracter inesperado "{error.value[0]}" en la fila {error.lineno}, columna {find_column(data, error)}')

