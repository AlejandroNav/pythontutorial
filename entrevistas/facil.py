
#¿Para qué sirve un bucle for y cómo imprimirías los números del 1 al 5?
# para iterar de forma secuancial
# formado de dos cosas 1 variable de control, 2 codigo a ejecutar

for i in range(1,6):
    print(i)

# imprime los numeros del 20 al 60 de 5 en 5
print("================= /n" )
for i in range(20,61,5):
    print(i)

#¿En qué se diferencian una lista y un diccionario en Python?

#Colección ordenada de elementos acceso por indices, Permite valores duplicados
listaFrutas = ["manzano","mango","fresa","mango"]
print(listaFrutas[3])

# colecciones de pares CLAVE+VALOR , los valores se pueden repetir las claves no
dictionarioAmalia = {
    "nombre": "amalia",
    "apellido": "soto",
    "edad": 23 
}
print("hola tengo " + str(dictionarioAmalia["edad"]))
#str convierte de cualqueir tipo de dato a string para imprimir de 23 a "23"



#¿Cómo cargarías un archivo CSV en un DataFrame llamado df con pandas?

# con Pandas usando read_csv

import pandas as pd
# ventas.csv es el nombre del archivo

df = pd.read_csv("ventas.csv")
print(df)


#¿Cómo contarías los valores faltantes en la columna edad de un DataFrame?

print(df["edad"])
#isNA, preguntas si es un numero regresa false si si es un numero
valoresInexistentes=df["edad"].isna()

cuenta = valoresInexistentes.sum()
print(cuenta)



#Explica con tus palabras qué hace df.groupby('ciudad')['ventas'].mean().

dfCiudades = pd.DataFrame({
    "ciudad": ["CDMX", "CDMX", "Monterrey", "Guadalajara", "Monterrey"],
    "ventas": [100, 200, 150, 300, 250]
    
})

# Agrupa las ventas por ciudad y calcula el promedio en cada agrupacion
print(dfCiudades.groupby('ciudad')  ['ventas'].mean())



# ¿Qué es un JOIN en SQL y para qué se utiliza?

# Un join combina datos de dos o mas tablas, usnado columans comunes

# Une las tablas clientes y pedidos usando la columna en común id_cliente

# SELECT clientes.nombre, pedidos.fecha
# FROM clientes
# JOIN pedidos
#  ON clientes.id = pedidos.id_cliente;

# CLIENTES
# ID    nombre
# 1     ana
# 2     juan
# 3     raul
#
# PEDIDOS
# id    producto  cliente fechach
# 0023  cooche     3        lunes
# 0024  moto       2       martes
# 0034  jamon      1       domingo
#
#    raul   lunes
#    juan   martes
#    ana    domingo
