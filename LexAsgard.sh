#!/bin/bash

# Leemos el archivo de entrada desde la entrada estándar y guardarlo en una variable
archivo=$(cat)

# Invocamos al script main de Python pasándole el contenido del archivo como argumento
salida=$(python3 main.py "$archivo")

# Imprimir la salida del script de Python en la salida estándar del script de Bash
echo "$salida"