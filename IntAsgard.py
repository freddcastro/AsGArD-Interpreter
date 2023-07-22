import numpy as np
from SintAsgard import  *


class DivisionPorCero(Exception):
    pass
class ErrorDeTamañoLienzo(Exception):
    pass
class ErrorInicializacion(Exception):
    pass
class ErrorSintaxis(Exception):
    pass
class ErrorEstatico(Exception):
    pass
class ErrorDeEntrada(Exception):
    pass

def interp(ast):
    try:
        if ast is None:
            raise ErrorSintaxis
    
        # Creamos una tabla de símbolos que almacena nada más las variables
        primera_tabla = {}
        for var in ast.declars.vars:
            primera_tabla[var] = None
        tabla = TablaDeSimbolos(primera_tabla, None)
        buscar_instr(ast.instr, tabla)
    except ErrorSintaxis:
        pass

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
        if nodo.cont is None:
            cantidad = evaluar_exp(nodo.arit2) - evaluar_exp(nodo.arit1) + 1
            print(cantidad, 'asdasd')

    if isinstance(nodo, IteracionInd):
        while True:
            if evaluar_exp(nodo.guardia):
                buscar_instr(nodo.instr, tablaS)
            else:
                break
    
    if isinstance(nodo, Condicional):
        print(111111)
        resultado_guardia = evaluar_exp(nodo.guardia, tablaS)
        if resultado_guardia is True:
            print(2222222)
            buscar_instr(nodo.exito, tablaS)
        else:
            print(33333333)
            if nodo.fracaso is not None:
                print(4444444444)
                buscar_instr(nodo.exito, tablaS)

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
        try:

            if nodo.val == 'error':
                raise ErrorEstatico
            else:
                # Primeramente, evaluamos la expresion

                resultado = evaluar_exp(nodo.val, tablaS)

                # Ahora, asignamos el resultado a la variable en la tabla correspondiente
                tablaS.actualizarValor(nodo.var, resultado)
        except ErrorEstatico:
            pass

    if isinstance(nodo, Entrada):
            # recibimos la entrada
            try:
                entrada =input()
                entrada = int(entrada)
                tablaS.actualizarValor(nodo.var, entrada)
            except:
                # No es un entero, así que verificamos que sea un booleano
                if entrada == "true" or entrada == "false":
                    tablaS.actualizarValor(nodo.var, entrada)
                else:
                    try:
                        raise ErrorDeEntrada
                    except:
                        print("Error al ingresar valor de entrada, tipo incorrecto")

    
    if isinstance(nodo, Salida):
        salida = evaluar_exp(nodo.expr, tablaS)
        if salida is None:
            pass
        else:
            # verificamos si es un canvas para formatear la salida
            if isinstance(salida, np.ndarray):
                # Es una casilla sola
                if salida.size == 1:
                    print(salida[0])
                # Es un vector horizontal
                if len(salida.shape) == 1:
                    columna = ''
                    for x in salida:
                        if x == '':
                            pass
                        else:
                            columna += x
                    print(columna)
                # Es un vector vertical
                if len(salida.shape) == 2 and salida.shape[1] == 1:
                    for x in np.nditer(salida):
                        if x == '':
                            pass
                        else:
                            print(x)
                # Es una matriz
                if len(salida.shape) == 2 and (salida.shape[0] > 1 and salida.shape[1] > 1):
                    for i in range(salida.shape[0]):
                        fila = ''
                        for j in range(salida.shape[1]):
                            fila += salida[i][j]
                        print(fila)
            else:
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
        try:
            
            if resultado1 is None or resultado2 is None:
                raise ErrorInicializacion

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
                    elif resultado2 in [True, False]:
                        raise TypeError
                    elif resultado1 in [True, False]:
                        raise TypeError
                    else:
                        return resultado1 / resultado2
                except DivisionPorCero:
                    print(f"Error: División por Cero")
                except TypeError:
                    print("Error: División errónea de tipos")

            if expr.operador == "%":
                return resultado1 % resultado2
        except ErrorInicializacion:
            if resultado1 is None and isinstance(expr.izq, Variable):
                print(f"Error: La variable {expr.izq.ident} no está inicializada")
            if resultado2 is None and isinstance(expr.der, Variable):
                print(f"Error: La variable {expr.der.ident} no está inicializada")

    
    # Expresiones relacionadas a BOOLEANOS
    if isinstance(expr, Booleano):
        if expr.valor == "true":
            return True
        if expr.valor == "false":
            return False
        
    if isinstance(expr, OpBinLogica):
        resultado1 = evaluar_exp(expr.izq, tablaS)
        resultado2 = evaluar_exp(expr.der, tablaS)
        try:
            
            if resultado1 is None or resultado2 is None:
                raise ErrorInicializacion
            
            if expr.operador == "/\\":
                return resultado1 and resultado2
            
            if expr.operador == "\\/":
                return resultado1 or resultado2
        except ErrorInicializacion:
            if resultado1 is None and isinstance(expr.izq, Variable):
                print(f"Error: La variable {expr.izq.ident} no está inicializada")
            if resultado2 is None and isinstance(expr.der, Variable):
                print(f"Error: La variable {expr.der.ident} no está inicializada")

    # Expresiones RELACIONALES
    if isinstance(expr, OpBinRelacional):
        resultado1 = evaluar_exp(expr.izq, tablaS)
        resultado2 = evaluar_exp(expr.der, tablaS)
        
        try:
            if resultado1 is None or resultado2 is None:
                raise ErrorInicializacion
            
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
        except ErrorInicializacion:
            if resultado1 is None and isinstance(expr.izq, Variable):
                print(f"Error: La variable {expr.izq.ident} no está inicializada")
            if resultado2 is None and isinstance(expr.der, Variable):
                print(f"Error: La variable {expr.der.ident} no está inicializada")

    # Expresiones relacionadas a CANVAS
    if isinstance(expr, Canvas):
        if expr.valor[1] == ".":
            return np.array([" "])
        return np.array([expr.valor[1]])
    
    if isinstance(expr, OpBinLienzo):
        resultado1 = evaluar_exp(expr.izq, tablaS)
        resultado2 = evaluar_exp(expr.der, tablaS)

        try:
            if resultado1 is None or resultado2 is None:
                raise ErrorInicializacion
            
            if expr.operador == ":":
                try:
                    if resultado1[0] == "e" and resultado2[0] == "e":
                        return np.array(['e'])                       

                    if resultado1[0] == "e":
                        # Creamos la matriz vacía a partir del tamaño de la no vacía
                        vacia = np.empty(resultado2.shape, str)
                        
                        # devolvemos la concatenación horizontal
                        return np.hstack((vacia, resultado2))
                    
                    elif resultado2[0] == "e":
                        # Creamos la matriz vacía a partir del tamaño de la no vacía
                        vacia = np.empty(resultado1.shape, str)

                        # devolvemos la concatenación horizontal
                        return np.hstack((vacia, resultado1))

                    elif resultado1.shape != resultado2.shape:
                        raise ErrorDeTamañoLienzo
                    
                    # eliminamos los posibles vacios generados:
                    salida = np.hstack((resultado1, resultado2))
                    
                    return salida
                except ErrorDeTamañoLienzo: 
                    print("Error: los lienzos combinados no tienen la misma dimensión")
            
            if expr.operador == "|":
                try:
                    if resultado1[0] == "e" and resultado2[0] == "e":
                        return np.array(['e'])                       

                    if resultado1[0] == "e":

                        # Creamos la matriz vacía a partir del tamaño de la no vacía
                        vacia = np.empty(resultado2.shape, str)
                        
                        # devolvemos la concatenación vertical
                        return np.vstack((vacia, resultado2))
                    
                    elif resultado2[0] == "e":

                        # Creamos la matriz vacía a partir del tamaño de la no vacía
                        vacia = np.empty(resultado1.shape, str)

                        # devolvemos la concatenación vertical
                        return np.vstack((vacia, resultado1))

                    elif resultado1.shape != resultado2.shape:
                        raise ErrorDeTamañoLienzo
                    return np.vstack((resultado1, resultado2))
                except ErrorDeTamañoLienzo: 
                    print("Error: los lienzos combinados no tienen la misma dimensión")

            
        except ErrorInicializacion:
            if resultado1 is None and isinstance(expr.izq, Variable):
                print(f"Error: La variable {expr.izq.ident} no está inicializada")
            if resultado2 is None and isinstance(expr.der, Variable):
                print(f"Error: La variable {expr.der.ident} no está inicializada")

    # Expresiones Unarias de todos los tipos
    if isinstance(expr, ExpUnaria):
        resultado = evaluar_exp(expr.val, tablaS)
        try:
            if resultado is None:
                raise ErrorInicializacion
            if expr.tipo == "aritmética":
                return -resultado
            if expr.tipo == "booleana":
                return not resultado
            if expr.tipo == "lienzo":
                if expr.operador == "$":
                    resultado = np.rot90(resultado, k=-1)
                    for i in range(resultado.shape[0]):
                        for j in range(resultado.shape[1]):
                            if resultado[i][j] == "/":
                                resultado[i][j] = "\\"

                            elif resultado[i][j] == "\\":
                                resultado[i][j] = "/"
                            
                            elif resultado[i][j] == "_":
                                resultado[i][j] = "|"
                            
                            elif resultado[i][j] == "|":
                                resultado[i][j] = "_"
                            
                            elif resultado[i][j] == " ":
                                pass
                    return resultado
                
                if expr.operador == "'":
                    return resultado.transpose()

        except ErrorInicializacion:
            print(f"Error: La variable {expr.val.ident} no está inicializada")













