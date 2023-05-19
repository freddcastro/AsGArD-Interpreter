# AsGArD-Interpreter
Para el proyecto del lenguaje AsGard y el interpretador a realizar, se utilizará como lenguaje principal Python.

### Requisitos
Es necesario tener insalado el paquete `ply` el cual podemos instalar de la siguiente manera: `pip3 install ply`

También puede ser necesario darle permisos de ejecución al archivo LexAsgard.sh del proyecto para correrlo de manera correcta.

## Lexer
El Analizador Lexicográfico, o Lexer, correspondiente a la primera entrega del proyecto, está constituido por tres partes fundamentales
- **main.py** : Se trata de la función central de esta sección del proyecto. Se encarga de recibir la información por la entrada estándar del sistema, a través de la terminal, en un archivo de texto correspondiente al lenguaje AsGArD. Luego, se encargará de enviarla al lexer y finalmente, generará los tokens y luego de un poco de pre-procesamiento, los imprimirá con el formato indicado en las especificaciones.
- **LexAsgard.py**: Contiene al lexer y todas las especificaciones (o reglas, como se denominan en el caso específico del paquete PLY) que se necesitan para cada símbolo perteneciente al lenguaje AsGArD. Además, contiene un par de funciones de utilidad como lo son la función generadora de tokens y una función que cuenta el número de columnas, para el manejo de errores. En el archivo encontramos un diccionario de palabras reservadas, cuyos valores de cada tupla (llave, valor) son agregados luego a la lista de tokens presentes en el archivo. Esto con la finalidad de que exista una única regla para los Identificadores de Variables y los de Palabras Reservadas. A modo de que, al recibir la palabra que entra en la regla especificada en la expresión regular de la función (t_TkIdent), si ésta es una palabra reservada, entonces se busca el token para dicha palabra en la lista de tokens, y de no ser así simplemente se devuelve el tipo de token "TkIdent", que luego se utiliza en el pre-procesamiento del archivo main.py. También, silenciamos las advertencias del lexer pues nos indicaba que se estaba definiendo varias veces, pero puede ser por la recursividad del tipo de token (es decir, varios valores correspondientes al mismo tipo de token).
- **LexAsgard.sh**: Es el script en Bash que se encarga de invocar al script main.py, recibiendo el archivo proporcionado, pasándolo al script de Python y luego imprimiendo la salida del script a salida estándar.
