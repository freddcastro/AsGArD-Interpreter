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
'''

# Establecemos la precedencia de las operaciones
precedence = (
    ('nonassoc', 'TkMayor', 'TkMenor', 'TkMayorIgual',
     'TkMenorIgual', 'TkIgual', 'TkDesigual', 'TkAsignacion'), # Operadores No Asociativos
    ('left', 'TkMas', 'TkMenos', 'TkDisjuncion', 'TkConcatHorizontal',
     'TkConcatVertical'),
    ('left', 'TkMult', 'TkDiv', 'TkMod', 'TkConjuncion', 'TkRotacion', 'Negacion'), # Token Temporal Negacion
    ('right', 'MenosUnit', 'TkTransposicion'), # Token temporal MenosUnit
    ('left', 'TkParAbre', 'TkParCierra')
)

### INSTRUCCIONES ###


class Instruccion():
    def __init__(self, tipo):
        self.tipo = tipo

# Instrucción de Asignación
class Asignacion(Instruccion):
    def __init__(self, var, val):
        self.var = var
        self.val = val
        self.tipo = "asignacion"

def p_instruccion_asignacion(p):
    'instruccion : TkIdent TkAsignacion expresion'
    p[0] = Asignacion(p[1], p[3])


# Instrucción de Secuenciación
class Secuenciacion(Instruccion):
    def __init__(self, ins1, ins2, tipo="secuenciacion"):
        self.ins1 = ins1
        self.ins2 = ins2

def p_instruccion_secuenciacion(p):
    '''instruccion : instruccion TkPuntoYComa instruccion'''
    p[0] = Secuenciacion(p[1], p[3])


# Instrucción Condicional
class Condicional(Instruccion):
    def __init__(self, guardia, exito, fracaso=None, tipo="condicional"):
        self.guardia = guardia
        self.exito = exito
        self.fracaso = fracaso
    
def p_instruccion_condicional(p):
    '''instruccion : TkIf expresion TkThen instruccion TkDone
                    | TkIf expresion TkThen instruccion TkOtherwise instruccion TkDone'''
    if len(p) == 6:
        p[0] = Condicional(p[2], p[4])
    else:
        p[0] = Condicional(p[2], p[4], p[6])

  
# Instrucción de Iteración Indeterminada
class IteracionInd(Instruccion):
    def __init__(self, guardia, instr, tipo="iteracion indeterminada"):
        self.guardia = guardia
        self.instr = instr
    
def p_instruccion_iteracionind(p):
    '''instruccion : TkWhile expresion TkRepeat instruccion TkDone'''
    p[0] = IteracionInd(p[2], p[4])


# Instrucción de Iteración Determinada
class IteracionDet(Instruccion):
    def __init__(self, guardia, instr, tipo="iteracion determinada"):
        self.guardia = guardia
        self.instr = instr
    
def p_instruccion_iteraciondet(p):
    '''instruccion :  TkWith TkIdent TkFrom expresion TkTo expresion TkRepeat instruccion TkDone
                    | TkFrom expresion TkTo expresion TkRepeat instruccion TkDone'''
    p[0] = IteracionInd(p[2], p[4])


# Instrucción de Incorporación de Alcance TODO

# Instrucción de Entrada
class Entrada(Instruccion):
    def __init__(self, var, tipo="entrada"):
        self.var = var

def p_instruccion_entrada(p):
    '''instruccion : TkRead TkIdent'''
    p[0] = Entrada(p[2])


# Instrucción de Salida
class Salida(Instruccion):
    def __init__(self, expr, tipo="salida"):
        self.expr = expr

def p_instruccion_salida(p):
    '''instruccion : TkPrint expresion'''
    p[0] = Salida(p[2])



### EXPRESIONES ###

# Primeramente, establecemos las Superclases para trabajar
class Expr: pass

class Variable(Expr):
    def __init__(self, ident):
        self.ident = ident

def p_expresion_variable(p):
    'expresion : TkIdent'
    p[0] = Variable(p[1])

class Numero(Expr):
    def __init__(self,valor):
        self.valor = valor

def p_expresion_numero(p):
    'expresion : TkNumLit'
    p[0] = Numero(p[1])

class ExpUnaria(Expr):
    def __init__(self, operador, val, tipo):
        self.operador = operador
        self.val = val
        self.tipo = tipo

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

def p_expresion_OpBinAritmética(p):
    '''expresion : expresion TkMas expresion
                  | expresion TkMenos expresion
                  | expresion TkMult expresion
                  | expresion TkDiv expresion
                  | expresion TkMod expresion'''

    p[0] = OpBinAritmetica(p[1],p[2],p[3])

# Operación Unaria Aritmética - Menos
def p_expresion_MenosUnit(p):
    'expresion : TkMenos expresion %prec MenosUnit'
    p[0] = ExpUnaria(p[1], p[2], "aritmética")

def p_expresion_truefalse(p):
    '''expresion : TkTrue 
                | TkFalse'''
    p[0] = ExpUnaria(None, p[1], "booleana")

# Operaciones Binarias Relacionales
class OpBinRelacional(OperacionBinaria):
    def __init__(self, izq, operador, der, tipo="relacional"):
        super().__init__(izq, operador, der, tipo)

def p_expresion_OpBinRelacional(p):
    '''expresion : expresion TkMenor expresion
                  | expresion TkMenorIgual expresion
                  | expresion TkMayor expresion
                  | expresion TkMayorIgual expresion
                  | expresion TkIgual expresion
                  | expresion TkDesigual expresion'''

    p[0] = OpBinRelacional(p[1],p[2],p[3])


# Operaciones Binarias Lógicas
class OpBinLogica(OperacionBinaria):
    def __init__(self, izq, operador, der, tipo='lógica'):
        super().__init__(izq, operador, der, tipo)

def p_expresion_OpBinLogica(p):
    '''expresion : expresion TkConjuncion expresion
                  | expresion TkDisjuncion expresion'''
    p[0] = OpBinLogica(p[1],p[2],p[3])

# Operación Unaria Lógica - Negación
def p_expresion_Negación(p):
    'expresion : expresion TkNegacion %prec Negacion'
    p[0] = ExpUnaria(p[2], p[1], "lógica")


# Operaciones Binarias de Lienzo
class OpBinLienzo(OperacionBinaria):
    def __init__(self, izq, operador, der, tipo="lienzo"):
        super().__init__(izq, operador, der, tipo)

def p_expresion_OpBinLienzo(p):
    ''' expresion : expresion TkConcatHorizontal expresion
                  | expresion TkConcatVertical expresion
                  '''
    p[0] = OpBinLienzo(p[1], p[2], p[3])

def p_expresion_lienzo_unaria(p):
    '''expresion : TkRotacion expresion
                  | expresion TkTransposicion'''
    if p[1] == "TkRotacion":
        p[0] = ExpUnaria(p[1], p[2], 'lienzo')
    else:
        p[0] = ExpUnaria(p[2], p[1], 'lienzo')

def p_expresion_canvaslit(p):
    'expresion : TkCanvasLit'
    p[0] = ExpUnaria(None, p[1], 'lienzo')



# Manejamos los errores para cada regla TODO mejorar para cada caso, que sea más descriptivo, el num de columna esta mal
def p_instruccion_asignacion_error(p):
    'instruccion : TkIdent TkAsignacion error'
    print(f"Asignación Errónea en línea {p.lineno(3)}, columna {p.lexpos(3)}")

# Build the parser
parser = yacc.yacc()
