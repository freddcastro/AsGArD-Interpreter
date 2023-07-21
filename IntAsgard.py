from SintAsgard import  *

class DivisionPorCero(Exception):
    pass

def interp(ast):
    
    # Creamos una tabla de símbolos que almacena nada más las variables
    primera_tabla = {}
    for var in ast.declars.vars:
        primera_tabla[var] = None
    tabla = TablaDeSimbolos(primera_tabla, None)
    buscar_instr(ast.instr, tabla)

def buscar_instr(nodo, tablaS):
    '''
    Función que divide el nodo actual del AST en 3 partes:

    - Si es una instrucción de secuenciación vuelve a llamar a esta función
    - Si es una instrucción que contiene a otra instrucción, vuelve a llamar a esta función
    - Si es una instrucción "terminal", procede a ejecutarla, pasando a la etapa
    de evaluación de la misma.
    '''

    # Secuenciación
    if isinstance(nodo, Secuenciacion):
        buscar_instr(nodo.ins1, tablaS)
        buscar_instr(nodo.ins2, tablaS)
    
    # Instrucciones que contienen a otras instrucciones
    if isinstance(nodo, Incorporacion):
        # En este caso, debemos crear una nueva tabla y hacerla una tabla hija de la tabla actual
        tabla_hija = {}
        for var in nodo.declars.vars:
            tabla_hija[var] = None
        tabla = TablaDeSimbolos(tabla_hija, tablaS)
        buscar_instr(nodo.instr, tabla)

    if isinstance(nodo, IteracionDet):
        buscar_instr(nodo.instr,tablaS)

    if isinstance(nodo, IteracionInd):
        buscar_instr(nodo.instr, tablaS)
    
    if isinstance(nodo, Condicional):
        buscar_instr(nodo.exito, tablaS)
        if nodo.fracaso is not None:
            buscar_instr(nodo.exito, tablaS)
    
    if isinstance(nodo, IteracionInd):
        buscar_instr(nodo.instr, tablaS)

    # Instrucciones Terminales
    if isinstance(nodo, Asignacion):
        evaluar_ins_terminal(nodo, tablaS)
    
    if isinstance(nodo, Entrada):
        evaluar_ins_terminal(nodo, tablaS)
    
    if isinstance(nodo, Salida):
        evaluar_ins_terminal(nodo, tablaS)

# Ahora, dependiendo de la instrucción terminal, de
def evaluar_ins_terminal(nodo, tablaS):
    '''
    Función que evalúa las 3 instrucciones terminales:

    - Si es una Asignación, debemos evaluar la expresión de la misma y luego
    actualizar el valor de la variable en la tabla de símbolos

    - Si es una Entrada, debemos aplicar input(), verificando el tipo y luego
    actualizar el valor de la variable en la tabla de símbolos

    - Si es una Salida, debemos hacer print()
    '''
    
    if isinstance(nodo, Asignacion):
        # Primeramente, evaluamos la expresion

        resultado = evaluar_exp(nodo.val, tablaS)

        # Ahora, asignamos el resultado a la variable en la tabla correspondiente
        tablaS.actualizarValor(nodo.var, resultado)

        print(tablaS.buscarValor(nodo.var))

    if isinstance(nodo, Entrada):
        print("entrada")
    
    if isinstance(nodo, Salida):
        salida = evaluar_exp(nodo.expr, tablaS)
        print(salida)

def evaluar_exp(expr, tablaS):
    '''
    Función que evalúa las expresiones de manera recursiva y en las "terminales" devuelve el resultado
    Si existen variables debe buscar su valor en la tabla de símbolos y de no tener valor se trata
    de un error dinámico que debe ser reportado.
    '''
    
    if isinstance(expr, Parentizada):
        resultado = evaluar_exp(expr.interna, tablaS)
        return resultado

    if isinstance(expr, Variable):
        # Buscamos el valor de la variable en la tabla de símbolos y si no tiene reportamos un error
        resultado = tablaS.buscarValor(expr.ident)
        return resultado
        
    # Expresiones relacionadas a ENTEROS
    if isinstance(expr, Numero):
        return int(expr.valor)

    if isinstance(expr, OpBinAritmetica):
        resultado1 = evaluar_exp(expr.izq, tablaS)
        resultado2 = evaluar_exp(expr.der, tablaS)

        if expr.operador == "+":
            return resultado1 + resultado2
        
        if expr.operador == "-":
            return resultado1 - resultado2

        if expr.operador == "*":
            return resultado1 * resultado2
        
        if expr.operador == "/":
            try:
                if resultado2 == 0:
                    raise DivisionPorCero
                else:
                    return resultado1 / resultado2
            except DivisionPorCero:
                print(f"Error, División por Cero")

        if expr.operador == "%":
            return resultado1 % resultado2


    
    # Expresiones relacionadas a BOOLEANOS
    if isinstance(expr, Booleano):
        if expr.valor == "true":
            return True
        if expr.valor == "false":
            return False
        
    if isinstance(expr, OpBinLogica):
        resultado1 = evaluar_exp(expr.izq, tablaS)
        resultado2 = evaluar_exp(expr.der, tablaS)

        if expr.operador == "/\\":
            return resultado1 and resultado2
        
        if expr.operador == "\\/":
            return resultado1 or resultado2
    
    # Expresiones RELACIONALES
    if isinstance(expr, OpBinRelacional):
        resultado1 = evaluar_exp(expr.izq, tablaS)
        resultado2 = evaluar_exp(expr.der, tablaS)

        if expr.operador == "=":
            return resultado1 == resultado2
        
        if expr.operador == "/=":
            return resultado1 != resultado2
        
        if expr.operador == "<":
            return resultado1 < resultado2
        
        if expr.operador == "<=":
            return resultado1 <= resultado2
        
        if expr.operador == ">":
            return resultado1 > resultado2
        
        if expr.operador == ">=":
            return resultado1 >= resultado2

    # Expresiones Unarias de todos los tipos
    if isinstance(expr, ExpUnaria):
        if expr.tipo == "aritmética":
            resultado = evaluar_exp(expr.val, tablaS)
            return -resultado
        if expr.tipo == "booleana":
            resultado = evaluar_exp(expr.val, tablaS)
            return not resultado















