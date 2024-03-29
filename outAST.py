from SintAsgard import  *

def outAST(ast, espacios):

    ### INSTRUCCIONES ###
    # chequeamos para cada instrucción
    if isinstance(ast, Asignacion):
        print((" "* espacios) + "ASIGNACION")
        print((" "* espacios) + f"  - var : {ast.var}")
        if isinstance(ast.val, Numero) or isinstance(ast.val, Booleano) or isinstance(ast.val, Canvas):
            print((" "* espacios) + f"  - val : {ast.val.valor}")
        else:
            print((" "* espacios ) + f"  - val: ")
            outAST(ast.val, espacios+4)
    
    if isinstance(ast, Secuenciacion):
        # Imprimimos el nombre de la instrucción solo la primera vez
        if ast.primer_print:
            print((" "* espacios) + "SECUENCIACION")
            ast.primer_print = False
        # Si no está anidado, quiere decir que sus ambas instrucciones
        # son distintas de una secuenciación, por lo que las pasamos
        # normalmente de manera recursiva
        if not ast.anidada:
            outAST(ast.ins1, espacios + 4)
            outAST(ast.ins2, espacios + 4)
        # Si son anidadas, al tener precedencia izquierda, debemos 
        # iterar sobre la primera instrucción.
        # Si es una secuenciación, la pasamos de manera normal sin los
        # espacios extra para el orden de la salida
        # Si no es una secuenciación, la pasamos de manera normal con
        # los espacios correspondientes
        # La segunda instrucción nunca puede ser una secuenciación así
        # que la imprimimos normalmente
        else:
            for subnodo, valor in vars(ast.ins1).items():
                if isinstance(valor, Secuenciacion):
                    outAST(valor, espacios)
                else:
                    outAST(valor, espacios+4)
            outAST(ast.ins2, espacios + 4)

    if isinstance(ast, Condicional):
        print((" "* espacios) + ast.tipo.upper())

        # guardia del condicional
        print((" "* espacios) + "  - guardia:")
        outAST(ast.guardia, espacios + 6)
        
        # exito del condicional
        print((" "* espacios) + "  - exito:")
        outAST(ast.exito, espacios + 6)

        if ast.fracaso is not None:
            # exito del condicional
            print((" "* espacios) + "  - fracaso:")
            outAST(ast.fracaso, espacios + 6)

    if isinstance(ast, IteracionInd):
        print((" "* espacios) + ast.tipo.upper())

        # guardia de la iteracion
        print((" "* espacios) + "  - guardia:")

        outAST(ast.guardia, espacios + 6)

        # instrucción de la iteracion
        print((" "* espacios) + "  - exito:")

        outAST(ast.instr, espacios + 6)

    if isinstance(ast, IteracionDet):
        print((" "* espacios) + ast.tipo.upper())

        # Valor inicial del rango
        print((" "* espacios) + "  - Valor Inicial del Rango:")
        outAST(ast.arit1, espacios + 6)

        # Valor inicial del rango
        print((" "* espacios) + "  - Valor Final del Rango:")
        outAST(ast.arit2, espacios + 6)

        # Instrucción de Repetición
        print((" "* espacios) + "  - Instruccion A Repetir:")
        outAST(ast.instr, espacios + 6)

    if isinstance(ast, Entrada):
        print((" "* espacios) + ast.tipo.upper())

        # Nombre del Identificador usado en la entrada
        print((" "* espacios) + f"  - var: {ast.var}")

    if isinstance(ast, Salida):
        print((" "* espacios) + ast.tipo.upper())

        # Nombre de la expresión impresa en salida
        print((" "* espacios) + "  - Expresion:")
        outAST(ast.expr, espacios + 4)

    if isinstance(ast, Incorporacion):
        print((" "* espacios) + ast.tipo.upper())

        # Instrucciones del Sub programa
        print((" "* espacios) + "  - Instruccion:")
        outAST(ast.instr, espacios + 6)


    ### EXPRESIONES ###
    # Chequeamos para cada expresión
    if isinstance(ast, OperacionBinaria):

        print((" "* espacios) + "OP BINARIA " + ast.tipo.upper())
        
        # Operacion
        print((" "* espacios) + f"  - Operación: {ast.operador}")

        # Izquierdo
        print((" "* espacios) + "  - Operador izquierdo:")
        outAST(ast.izq, espacios + 6)
        
        # Derecho
        print((" "* espacios) + "  - Operador derecho:")
        outAST(ast.der, espacios + 6)
        
    if isinstance(ast, Numero) or isinstance(ast, Canvas) or isinstance(ast, Booleano):
        print((" "* espacios) + f"- val: {ast.valor}")
    
    if isinstance(ast, Variable):
        print((" "* espacios) + f"- var: {ast.ident}")

    if isinstance(ast, Parentizada):
        outAST(ast.interna, espacios)

    if isinstance(ast, ExpUnaria):

        print((" "* espacios) + f"OP UNARIA " + ast.tipo.upper())
        print((" "* espacios) + f"  - Operador: '{ast.operador}'")
        
        if isinstance(ast.val, Variable):
            print((" "* espacios) + f"  - val: {ast.val.ident}")

        else:
            if not isinstance(ast.val, Parentizada):
                if not isinstance(ast.val, ExpUnaria):
                    print((" "* espacios) + f"  - val: {ast.val.valor}")
                else:
                    print((" "* espacios) + "  - val:")
                    outAST(ast.val, espacios + 4)
            else:
                print((" "* espacios) + "  - val:")
                outAST(ast.val, espacios + 4)
