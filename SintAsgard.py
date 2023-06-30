import re
import ply.yacc as yacc
from LexAsgard import tokens, find_column

'''
La gramática a Utilizar es la siguiente:

expresion ->  expresion TkMas expresion
            | expresion TkMenos expresion
            | expresion TkDiv expresion
            | expresion TkMod expresion
            | TkMenos expresion
            | TkNumLit
            | expresion TkMayor expresion
            | expresion TkMenor expresion
            | expresion TkMayorIgual expresion
            | expresion TkMenorIgual expresion
            | expresion TkIgual expresion
            | expresion TkDesigual expresion
            | TkTrue
            | TkFalse
            | expresion TkConjuncion expresion
            | expresion TkDisjuncion expresion
            | TkNegacion expresion
            | expresion TkConcatHorizontal expresion
            | expresion TkConcatVertical expresion
            | TkRotacion expresion
            | expresion TkTransposicion
            | TkCanvasLit
            | TkIdent
            | TkParAbre expresion TkParCierra

instruccion -> TkUsing declaracion TkBegin instruccion TkEnd
             | TkIdent TkAsignacion expresion
             | instruccion TkPuntoYComa instruccion
             | TkIf expresion TkThen instruccion TkDone
             | TkIf expresion TkThen instruccion TkOtherwise instruccion TkDone
             | TkWhile expresion TkRepeat instruccion TkDone
             | TkWith TkIdent TkFrom expresion TkTo expresion TkRepeat instruccion TkDone
             | TkFrom expresion TkTo expresion TkRepeat instruccion TkDone
             | TkPrint expresion
             | TkRead TkIdent

identificadores -> TkIdent
                 | TkIdent TkComa identificadores

declaracion -> identificadores TkOf TkType TkInteger
             | identificadores TkOf TkType TkBoolean
             | identificadores TkOf TkType TkCanvas
             | declaracion TkPuntoYComa declaracion
'''

# Establecemos la precedencia de las operaciones
precedence = (
    ('nonassoc', 'TkMayor', 'TkMenor', 'TkMayorIgual',
     'TkMenorIgual', 'TkIgual', 'TkDesigual', 'TkAsignacion'), # Operadores No Asociativos
    
    ('left', 'TkMas', 'TkMenos', 'TkDisjuncion', 'TkConcatHorizontal','TkConcatVertical',) ,
    
    ('left', 'TkMult', 'TkDiv', 'TkMod', 'TkConjuncion', 'TkRotacion', 'TkPuntoYComa'), 

    ('right', 'MenosUnit', 'TkTransposicion',), # Token temporal MenosUnit
    
    ('left', 'TkParAbre', 'TkParCierra', 'TkNegacion') # Token Temporal Negacion
)

### Analisis de Contexto ###
# Definimos la clase correspondiente a la tabla de símbolos
class TablaDeSimbolos():
    def __init__(self, tabla, padre):
        self.tabla = tabla
        self.padre = padre
    
    # Agrega elementos a la tabla actual
    def insertar(self, identificador, tipo, valor=None):
        # Primero, debemos chequear que al insertar, no exista un identificador con el mismo nombre
        unique = True
        for key in self.tabla.keys():
            if key == identificador:
                unique = False
        if unique:
            self.tabla.update({f"{identificador}": [identificador, tipo, valor]})
        else:
            print(f'Error Estático: La variable {identificador} ya está definida')

    # Verifica la existencia de la variable en cada incorporación de alcance correspondiente
    def verificarExistencia(self, identificador, existe=False):

        for key in self.tabla.keys():
            if key == identificador:
                existe = True
                return existe
        if not existe:
            if self.padre is None:
                existe = False
                return existe
            else:
                existe = self.padre.verificarExistencia(identificador, existe)
                return existe

        return existe            

    def verificarTipo(self, tipo_esperado, valor):

        # Verificamos si el error está en la expresión
        if valor.var_tipo == "error":
            return "error"

        if tipo_esperado != valor.var_tipo:
            return False
        return True
# Creamos la variable t_actual que indica cuál es la tabla de símbolos actual
t_actual = TablaDeSimbolos({}, None)

# Con esta función, manejamos las variables para cada expresión e instrucción, donde verificamos
# si existen y, de ser así, les añadimos el valor especificado en la tabla de símbolos
def existencia_variables(inst, linea):
    if isinstance(inst, Variable):
        if t_actual.verificarExistencia(inst.ident):
            inst.var_tipo = t_actual.tabla[f"{inst.ident}"][1]
            return  True
        else:
            print(f"Error Estático en la línea {linea}: La variable '{inst.ident}' no está definida")
            return False


### INSTRUCCIONES ###
class Instruccion():
    def __init__(self, tipo):
        self.tipo = tipo


# Instrucción de Incorporación de Alcance
class Incorporacion(Instruccion):
    def __init__(self, declars, instr, tipo="incorporación de alcance"):
        self.declars = declars
        self.instr = instr
        self.tipo = tipo

def p_instruccion_incorporacion(p):
    'instruccion : abrir_alcance TkUsing declaracion TkBegin instruccion TkEnd cerrar_alcance'
    p[0] = Incorporacion(p[3], p[5])
    
def p_abrir_alcance(p):
    "abrir_alcance :"
    global t_actual
    p[0] = TablaDeSimbolos({}, t_actual)
    # le asignamos este valor a la variable global t_actual
    t_actual = p[0]


def p_cerrar_alcance(p):
    "cerrar_alcance :"
    global t_actual
    t_actual = t_actual.padre
    
# Lista de Declaraciones (no es precisamente una instrucción pero se considerará como tal a fines del código)

class ListaDeclaraciones(Instruccion):
    def __init__(self, vars, tipo_declar, tipo="listadeclaraciones"):
        self.vars = vars
        self.tipo_declar = tipo_declar
        self.tipo = tipo
        self.tabla = None

# Definimos una lista que almacenará los identificadores encontrados
l_identificadores = []

def p_instruccion_declaraciones(p):
    '''declaracion : identificadores TkOf TkType TkInteger
                    | identificadores TkOf TkType TkBoolean
                    | identificadores TkOf TkType TkCanvas
                    | declaracion TkPuntoYComa declaracion'''
    if len(p) == 5:
        # Copiamos la lista de identificadores actual
        identificadores2 = l_identificadores.copy()

        # Creamos la clase
        p[0] = ListaDeclaraciones(identificadores2, p[4])

        # Reiniciamos la global para recibir los nuevos identificadores
        l_identificadores.clear()
    if len(p) == 4:
        p[0] = ListaDeclaraciones([p[1], p[3]], "compuesto")
    
    
    p[0].tabla = t_actual

    if p[0].tipo_declar != "compuesto":
            
        # Ahora, insertamos elementos en la tabla
        for var in p[0].vars:
            p[0].tabla.insertar(var, p[0].tipo_declar)

def p_instruccion_identificadores(p):
    '''identificadores : TkIdent
                        | TkIdent TkComa identificadores'''
    if len(p) >= 2:
        l_identificadores.append(p[1])

# Instrucción de Asignación
class Asignacion(Instruccion):
    def __init__(self, var, val):
        self.var = var
        self.val = val
        self.tipo = "asignacion"

def p_instruccion_asignacion(p):
    'instruccion : TkIdent TkAsignacion expresion'

    # Al momento de revisar la instrucción de asignación, debemos verificar que
    # la variable a utilizar exista y de no ser así, debe imprimir error
    existe = t_actual.verificarExistencia(p[1])
    if not existe:
        print(f"Error Estático en la línea {p.lineno(1)}: La variable '{p[1]}' no está definida")
    else:
        
        # Ahora, basta verificar el tipo de variable esperado
        tipo_correcto = t_actual.verificarTipo(t_actual.tabla[f"{p[1]}"][1], p[3])

        # Si la función de verificación devuelve error, entonces el error está en la expresión generada
        if tipo_correcto == "error":
            print(f"Error Estático en la línea {p.lineno(1)}, columna {col_num(p.lexer.lexdata, p.lexpos(2)+2)}: Conflicto de tipos en la expresión")

        elif tipo_correcto is False:
            print(f"Error Estático en la línea {p.lineno(1)}: La variable '{p[1]}' no tiene el tipo de variable correcto")

    p[0] = Asignacion(p[1], p[3])

# Instrucción de Secuenciación
class Secuenciacion(Instruccion):
    def __init__(self, ins1, ins2,anidada, primer_print, tipo="secuenciacion"):
        self.ins1 = ins1
        self.ins2 = ins2
        self.anidada = anidada
        self.primer_print = primer_print
        self.tipo = tipo

def p_instruccion_secuenciacion(p):
    '''instruccion : instruccion TkPuntoYComa instruccion'''
    if isinstance(p[1], Secuenciacion):
        p[0] = Secuenciacion(p[1], p[3], True, False)
    else:
        p[0] = Secuenciacion(p[1], p[3], False, True)

# Instrucción Condicional
class Condicional(Instruccion):
    def __init__(self, guardia, exito, fracaso=None, tipo="condicional"):
        self.guardia = guardia
        self.exito = exito
        self.fracaso = fracaso
        self.tipo = tipo
    
def p_instruccion_condicional(p):
    '''instruccion : TkIf expresion TkThen instruccion TkDone
                    | TkIf expresion TkThen instruccion TkOtherwise instruccion TkDone'''
    # Verificamos si la expresión dada es una variable existente
    existencia_variables(p[2], p.lineno(1))
    if p[2].var_tipo != "boolean":
        print(f"Error Estático en la línea {p.lineno(1)}: La expresión en la guardia del condicional no tiene el tipo de dato booleano")
    if len(p) == 6:
        p[0] = Condicional(p[2], p[4])
    else:
        p[0] = Condicional(p[2], p[4], p[6])

  
# Instrucción de Iteración Indeterminada
class IteracionInd(Instruccion):
    def __init__(self, guardia, instr, tipo="iteracion indeterminada"):
        self.guardia = guardia
        self.instr = instr
        self.tipo = tipo
    
def p_instruccion_iteracionind(p):
    '''instruccion : TkWhile expresion TkRepeat instruccion TkDone'''

    # Verificamos si la expresión dada es una variable existente
    existencia_variables(p[2], p.lineno(1))
    if p[2].var_tipo != "boolean":
        print(f"Error Estático en la línea {p.lineno(1)}: La expresión en la guardia de la iteración indeterminada no tiene el tipo de dato booleano")

    p[0] = IteracionInd(p[2], p[4])


# Instrucción de Iteración Determinada
class IteracionDet(Instruccion):
    def __init__(self, arit1, arit2, instr, cont=None,tipo="iteracion determinada"):
        self.arit1 = arit1
        self.arit2 = arit2
        self.instr = instr
        self.cont = cont
        self.tipo = tipo
    
def p_instruccion_iteraciondet(p):
    '''instruccion :  TkWith TkIdent TkFrom expresion TkTo expresion TkRepeat instruccion TkDone
                    | TkFrom expresion TkTo expresion TkRepeat instruccion TkDone'''
    if len(p) == 10:
        p[0] = IteracionDet(p[4], p[6], p[8], p[2])
    else:
        p[0] = IteracionDet(p[2], p[4], p[6])

# Instrucción de Entrada
class Entrada(Instruccion):
    def __init__(self, var, tipo="entrada"):
        self.var = var
        self.tipo = tipo

def p_instruccion_entrada(p):
    '''instruccion : TkRead TkIdent'''
    p[0] = Entrada(p[2])


# Instrucción de Salida
class Salida(Instruccion):
    def __init__(self, expr, tipo="salida"):
        self.expr = expr
        self.tipo = tipo

def p_instruccion_salida(p):
    '''instruccion : TkPrint expresion'''
    p[0] = Salida(p[2])



### EXPRESIONES ###

# Primeramente, establecemos las Superclases para trabajar
class Expr: pass

class Variable(Expr):
    def __init__(self, ident):
        self.ident = ident
        self.var_tipo = None

def p_expresion_variable(p):
    'expresion : TkIdent'
    p[0] = Variable(p[1])

class Numero(Expr):
    def __init__(self,valor):
        self.valor = valor
        self.var_tipo = "integer"

def p_expresion_numero(p):
    'expresion : TkNumLit'
    p[0] = Numero(p[1])


class ExpUnaria(Expr):
    def __init__(self, operador, val, tipo):
        self.operador = operador
        self.val = val
        self.tipo = tipo
        self.var_tipo = self.val.var_tipo

class OperacionBinaria(Expr):
    def __init__(self, izq, operador, der, tipo):
        self.izq = izq
        self.der = der
        self.operador = operador
        self.tipo = tipo

# Vamos con las Operaciones Binarias de cada tipo

# Operaciones Binarias Aritméticas
class OpBinAritmetica(OperacionBinaria):
    def __init__(self, izq, operador, der, tipo="aritmética"):
        super().__init__(izq, operador, der, tipo)
        self.var_tipo = "integer" if self.izq.var_tipo == "integer" and self.der.var_tipo == "integer" else "error"

def p_expresion_OpBinAritmetica(p):
    '''expresion : expresion TkMas expresion
                  | expresion TkMenos expresion
                  | expresion TkMult expresion
                  | expresion TkDiv expresion
                  | expresion TkMod expresion'''

    # Verificamos si alguna expresión es una variable y aplicamos el manejo correspondiente
    existencia_variables(p[1], p.lineno(2))
    
    existencia_variables(p[3], p.lineno(2))

    p[0] = OpBinAritmetica(p[1],p[2],p[3])

# Operación Unaria Aritmética - Menos
def p_expresion_MenosUnit(p):
    'expresion : TkMenos expresion %prec MenosUnit'

    # Para una expresión unaria, si se trata de una variable, verificamos
    # existencia y luego le asociamos a la variable su tipo de la tabla
    existencia_variables(p[2], p.lineno(1))
    if p[2].var_tipo != "integer":
        p[0] = ExpUnaria(p[1], p[2], "aritmética")
        p[0].var_tipo = "error"
    else:
        p[0] = ExpUnaria(p[1], p[2], "aritmética")
        p[0].var_tipo = "integer"

# Operaciones Binarias Relacionales
class OpBinRelacional(OperacionBinaria):
    def __init__(self, izq, operador, der, tipo="relacional"):
        super().__init__(izq, operador, der, tipo)
        self.var_tipo = "boolean" if self.izq.var_tipo == self.der.var_tipo else "error"

def p_expresion_OpBinRelacional(p):
    '''expresion : expresion TkMenor expresion
                  | expresion TkMenorIgual expresion
                  | expresion TkMayor expresion
                  | expresion TkMayorIgual expresion
                  | expresion TkIgual expresion
                  | expresion TkDesigual expresion'''
    
    # Misma lógica que con expresiones binarias aritméticas
    existencia_variables(p[1], p.lineno(2))
    
    existencia_variables(p[3], p.lineno(2))

    p[0] = OpBinRelacional(p[1],p[2],p[3])


# Operaciones Binarias Lógicas
class OpBinLogica(OperacionBinaria):
    def __init__(self, izq, operador, der, tipo='lógica'):
        super().__init__(izq, operador, der, tipo)
        self.var_tipo = "boolean" if self.izq.var_tipo == "boolean" and self.der.var_tipo == "boolean" else "error"

def p_expresion_OpBinLogica(p):
    '''expresion : expresion TkConjuncion expresion
                  | expresion TkDisjuncion expresion'''
    
    existencia_variables(p[1], p.lineno(2))
    
    existencia_variables(p[3], p.lineno(2))

    p[0] = OpBinLogica(p[1],p[2],p[3])

class Booleano(Expr):
    def __init__(self, valor, negada):
        self.valor = valor
        self.negada = negada
        self.var_tipo = "boolean"

# Operación Unaria Lógica - Negación
def p_expresion_Negacion(p):
    'expresion : expresion TkNegacion'

    # Misma lógica que con las unarias aritméticas
    existencia_variables(p[1], p.lineno(2))
    if p[1].var_tipo != "boolean":
        p[0] = ExpUnaria(p[2], p[1], 'booleana')
        p[0].var_tipo = "error"
    else:
        p[0] = ExpUnaria(p[2], p[1], 'booleana')
        p[0].var_tipo = "boolean"
        
def p_expresion_truefalse(p):
    '''expresion : TkTrue 
                | TkFalse'''
    p[0] = Booleano(p[1], False)    

# Operaciones Binarias de Lienzo
class OpBinLienzo(OperacionBinaria):
    def __init__(self, izq, operador, der, tipo="lienzo"):
        super().__init__(izq, operador, der, tipo)
        self.var_tipo = "canvas" if self.izq.var_tipo == "canvas" and self.der.var_tipo == "canvas" else "error"

def p_expresion_OpBinLienzo(p):
    ''' expresion : expresion TkConcatHorizontal expresion
                  | expresion TkConcatVertical expresion
                  '''
    
    # Misma lógica que en expresiones binarias aritméticas
    existencia_variables(p[1], p.lineno(2))
    
    existencia_variables(p[3], p.lineno(2))

    p[0] = OpBinLienzo(p[1], p[2], p[3])
    

def p_expresion_lienzo_unaria(p):
    '''expresion : TkRotacion expresion
                  | expresion TkTransposicion'''
    
    # Misma lógica que con las unarias aritméticas
    if p[1] == "$":
        existencia_variables(p[2], p.lineno(1))
        if p[2].var_tipo != "canvas":
            p[0] = ExpUnaria(p[1], p[2], 'lienzo')
            p[0].var_tipo = "error"
        else:
            p[0] = ExpUnaria(p[1], p[2], 'lienzo')
            p[0].var_tipo = "canvas"
    else:
        existencia_variables(p[1], p.lineno(2))
        if p[1].var_tipo != "canvas":
            p[0] = ExpUnaria(p[2], p[1], 'lienzo')
            p[0].var_tipo = "error"
        else:
            p[0] = ExpUnaria(p[2], p[1], 'lienzo')
            p[0].var_tipo = "canvas"
        

class Canvas(Expr):
    def __init__(self, valor):
        self.valor = valor
        self.var_tipo = "canvas"

def p_expresion_canvaslit(p):
    'expresion : TkCanvasLit'
    p[0] = Canvas(p[1])

class Parentizada(Expr):
    def __init__(self, interna, tipo):
        self.interna = interna
        self.tipo = tipo
        self.var_tipo = interna.var_tipo

def p_expresion_parentizada(p):
    'expresion : TkParAbre expresion TkParCierra'

    # verificamos si es una variable y realizamos el proceso correspondiente
    existencia_variables(p[2], p.lineno(1))
    p[0] = Parentizada(p[2], "parentizada")

# Funcion local para el número de columnas
def col_num(input, lexpos):
    comienzo = input.rfind('\n', 0, lexpos) + 1
    return (lexpos - comienzo) + 1

# Manejamos los errores de forma general, permitiendo que la ejecución
# sea solamente una vez
def p_error(p):
    if not hasattr(p_error, "ejecutada"):
        if not p:
            print("Error de Sintaxis al final de Archivo")
            return
        print(f"Error sintáctico en línea {p.lineno}, columna {col_num(p.lexer.lexdata, p.lexpos)}")
        setattr(p_error, "ejecutada", True)
    

# Construimos el parser
parser = yacc.yacc()

