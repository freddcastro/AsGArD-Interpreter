# AsGArD-Interpreter
Para el proyecto del lenguaje AsGard y el interpretador a realizar, se utilizará como lenguaje principal Python.

### Requisitos
Es necesario tener insalado el paquete `ply` el cual podemos instalar de la siguiente manera: `pip3 install ply`

También puede ser necesario darle permisos de ejecución al archivo LexAsgard.sh del proyecto para correrlo de manera correcta.

## Lexer
El Analizador Lexicográfico, o Lexer, correspondiente a la primera entrega del proyecto, está especificado dentro del archivo `LexAsgard.py`, el cual contiene al lexer y todas las especificaciones (o reglas, como se denominan en el caso específico del paquete PLY) que se necesitan para cada símbolo perteneciente al lenguaje AsGArD. Además, contiene un par de funciones de utilidad como lo son la función generadora de tokens y una función que cuenta el número de columnas, para el manejo de errores. 
En el archivo encontramos un diccionario de palabras reservadas, cuyos valores de cada tupla (llave, valor) son agregados luego a la lista de tokens presentes en el archivo. Esto con la finalidad de que exista una única regla para los Identificadores de Variables y los de Palabras Reservadas. A modo de que, al recibir la palabra que entra en la regla especificada en la expresión regular de la función (t_TkIdent), si ésta es una palabra reservada, entonces se busca el token para dicha palabra en la lista de tokens, y de no ser así simplemente se devuelve el tipo de token "TkIdent", que luego se utiliza en el pre-procesamiento del archivo main.py. También, silenciamos las advertencias del lexer pues nos indicaba que se estaba definiendo varias veces, pero puede ser por la recursividad del tipo de token (es decir, varios valores correspondientes al mismo tipo de token).


## Parser
El Analizador Sintáctico, o Parser, correspondiente a la segunda entrega dle proyecto, está definido en el archivo `SintAsgard.py`.

Primeramente, al comienzo del archivo se encuentra un docstring que especifica la gramática regular ambigua recursiva izquierda que genera al lenguaje AsGArD. Seguidamente, apoyándonos en la herramienta usada para la creación del parser, se establecen las normas de precedencia, de manera tal que se puedan lidiar con los conflictos que genera la ambigüedad de la gramática.

De la misma manera, para el tratamiento de las expresiones e instrucciones, se utilizó el enfoque de POO, donde se generaron superclases para las expresiones y las instrucciones, y luego se añadieron subclases correspondientes a cada una de las posibles variantes, definidas en la gramática antes mencionada. A su vez, cada clase va acompañada de una función que cuenta con un prefijo en el nombre, indicando si es una expresión o una instrucción, que lleva el mismo nombre de la clase. De esta manera, la función captura la parte de la gramática especificada en ella y luego de eso se instancia en su subclase correspondiente.

Es importante destacar que para la instrucción de Incorporación de Alcance, debido a su estructura, se generó una subclase denominada `ListaDeclaraciones`. Esta subclase no corresponde precisamente una instrucción, pero a fines del código se consideró como tal. Así, gracias a esta subclase y la gramática adicional proporcionada, se puede generar un fragmento de la gramática que es eficiente a la hora de capturar la instrucción de Incorporación de Alcance.

Finalmente, luego de todas las especificaciones, se genera el parser.

También, se creó un archivo adicional llamado `outAST` que contiene una función de mismo nombre. Dicha función, se encarga de imprimir en la salida estándar la información del AST generado por el parser antes nombrado. La función, a través de un enfoque recursivo, inspecciona cada nodo (lidiando con los posibles anidamientos) verificando la clase de cada uno y se encarga de extraer, formatear e imprimir a salida estándar una estructura que representa el AST generado.

## Parser
Para la tercera entrega del proyecto, se extendieron las funcionalidades del parser, en el archivo SintAsgrd.py añadiendo control sobre el contexto generado por el código proporcionado. Primeramente, se añadió el manejo de tablas de símbolos, aplicando herencias y utilizando una variable global que hace referencia a la tabla de símbolos actual al momento de ejecutar el programa. Algunas instrucciones como la incorporación de alcance fueron modificadas para el manejo de esta tabla, añadiendo acciones a través del símbolo vacío (lambda) Y permitiendo ejecutar cierta lógica en momentos específicos. Para dicho manejo de tablas de símbolos, se creó una clase llamada `TablaDeSimbolos` que permite crear instancias de tablas de símbolos, con funciones que permiten su manejo, como verificar la existencia de una variable en dicha tabla y sus tablas padres, por ejemplo. Es importante destacar que el analizador de contexto (que no funciona aparte, sino que es una extensión del código implementado para el analizador sintáctico permitiendo así que ambas "partes" del interpretador se ejecuten simultáneamente construyendo los datos necesarios) imprime en la salida estándar todos los errores de contexto encontrados, evaluando los casos pertinentes e informando sobre los conflictos de tipos de datos en las expresiones/instrucciones del código AsGArD proporcionado al mismo.

## Uso y Ejecución
- `main.py` : Se trata del archivo central del proyecto, donde se llama tanto al lexer como al parser. Se encarga de recibir la información por la entrada estándar del sistema, a través de la terminal, en un archivo de texto correspondiente al lenguaje AsGArD. Luego, se encargará de enviarla al lexer y finalmente, generará los tokens y luego de un poco de pre-procesamiento, los imprimirá con el formato indicado en las especificaciones. Así mismo, luego de eso, envía los datos al parser generado en `SintAsgard.py`, los cuales van a la función `outAST` la cual se encarga de imprimir la información del AST en la salida estándar.
- `ContAsgard`: Es el script en Bash que se encarga de invocar al script main.py, recibiendo el archivo proporcionado, pasándolo al script de Python y luego imprimiendo la salida del script a salida estándar.
Así, para utilizar el Lexer y el Parser, debemos ejecutar el Script de la siguiente manera:
`./ContAsgard < archivo.asg`
