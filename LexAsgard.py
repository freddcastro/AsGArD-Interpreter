import ply.lex as lex
import re

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
    "if": "TkIf",
    "then": "TkThen",
    "otherwise": "TkOtherwise",
    "done": "TkDone",
    "print": "TkPrint",
    "while": "TkWhile",
    "read": "TkRead",
    "with": "TkWith",
}

tokens = (
    # Separadores , ; ( )
    "TkComa", "TkPuntoYComa", "TkParAbre", "TkParCierra",

    # Operadores Aritméticos + - * / %
    "TkMas",  "TkMenos", "TkMult", "TkDiv", "TkMod",

    # Operadores Booleanos /\ \/ ^
    "TkConjuncion", "TkDisjuncion", "TkNegacion",

    # Operadores relacionales < <= > >= = !=
    "TkMenor", "TkMenorIgual", "TkMayor", "TkMayorIgual", "TkIgual", "TkDesigual",

    # Operadores de Lienzo : | $ '
    "TkConcatHorizontal",  "TkConcatVertical",  "TkRotacion",  "TkTransposicion",

    # Operador de asignación :=
    "TkAsignacion",
    
    # Identificadores
    "TkIdent", "TkNumLit", "TkTrue", "TkFalse", "TkCanvasLit", "Comentario",
    
)

tokens += tuple(reserved.values())

# Lista de tokens para imprimir al final
tokens_salida = []

# Lista para almacenar los tokens y valores de cada error
errores = []


def t_TkIdent(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'TkIdent')   # Buscamos las palabras reservadas
    return t

def t_TkCanvasLit(t):
    r'<empty>|<[\\\|\/\.\_]>'
    return t

t_TkNumLit = r'[0-9]+'

def t_Comentario(t):
    r'\{\-(.|\n)*?\-\}'
    # Debemos buscar los saltos de línea en la expresión
    saltos_de_linea = len([m.start() for m in re.finditer('\n', t.value)])
    # Los añadimos al lexer
    t.lexer.lineno += saltos_de_linea
    pass

# Definimos las demás reglas para los tokens sencillos

# Separadores
t_TkComa = r','

t_TkPuntoYComa = r'\;'

t_TkParAbre = r'\('

t_TkParCierra = r'\)'

# Operadores Aritméticos
t_TkMas = r'\+'

t_TkMenos = r'\-'

t_TkMult = r'\*'

t_TkDiv = r'\/'

t_TkMod = r'\%'

# Operadores Lógicos
t_TkConjuncion = r'\/\\'

t_TkDisjuncion = r'\\\/'

t_TkNegacion = r'\^'

# Operadores Relacionales
t_TkMenor = r'\<'

t_TkMenorIgual = r'\<='

t_TkMayor = r'\>'

t_TkMayorIgual = r'\>='

t_TkIgual = r'\='

t_TkDesigual = r'\!='

# Operadores de Canvas
t_TkConcatHorizontal = r'\:'

t_TkConcatVertical = r'\|'

t_TkRotacion = r'\$'

t_TkTransposicion = r'\''

# Operador Asignación
t_TkAsignacion = r'\:='


# Ignoramos los espacios, los tabuladores y los saltos de línea
t_ignore  = ' \t'

# Calculamos cada línea
def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar los errores, almacenandolos en una lista
def t_error(t):
    errores.append(t)
    t.lexer.skip(1)

# Creamos el lexer, silenciando los warnings
lexer = lex.lex(errorlog=lex.NullLogger())

# Funcion para generar tokens
def token_gen(lexer, tokens_salida, errores):
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

# Función para calcular el número de columna
# input es el texto ingresado
# token es la instancia del token a buscar

def find_column(input, token):
    comienzo = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - comienzo) + 1
