from LexAsgard import lexer, token_gen, errores, find_column, tokens_salida
from SintAsgard import  parser
from outAST import outAST

import sys

# Acá recibimos la información por entrada estándar
data = sys.argv[1]

# Invocamos al lexer, pasándole la información
lexer.input(data)

# Generamos los tokens luego de pasarle los datos al lexer
token_gen(lexer, tokens_salida, errores)

# Ahora, realizamos la verificación y el printing correspondiente

# Las listas vacias en python evaluan a false
if bool(errores) is False:
    # La lista de errores está vacía, es decir, no hay errores.
    # Asi, imprimimos los tokens encontrados
    for token in tokens_salida:
        if token.type == "TkNumLit":
            print(token.type + f"({token.value})", end=" ")
            continue
        if token.type == "TkIdent" or token.type == "TkCanvasLit":
            print(token.type + f'("{token.value}")', end=" ")
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

# reiniciamos la cuenta de líneas
lexer.lineno = 1

# Generamos el árbol sintáctico abstracto con los datos de la entrada estándar
ast = parser.parse(data)

#variable para formato
espacios = 0

# Comenzamos con este atributo porque la primera instruccion obtenida siempre es una incorporación de alcance
if ast is not None:
        if "instr" not in vars(ast):
            print("Error Sintáctico en linea 1, columna 1")
        else:
            outAST(ast.instr, espacios)
