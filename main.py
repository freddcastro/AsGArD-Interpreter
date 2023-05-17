from LexAsgard import lexer, token_gen, errores, find_column, tokens_salida

# Acá recibimos los datos del script

#invocamos al lexer

data = '''
using contador begin
  contador := 35
end
'''

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