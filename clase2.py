import numpy as np

# Crear matriz original de 10x10 con valores del 0 al 99
matriz = np.arange(100).reshape(10, 10)
print("Matriz original:")
print(matriz)

# Extraer una submatriz (filas 1, 5, 9; columnas 0 y 5) como copia
submatriz2 = matriz[1:10:4, ::5].copy()

# Modificar el valor en la posición [0, 0] de la submatriz
submatriz2[0, 0] = -1

# Mostrar submatriz modificada
print("\nSubmatriz modificada (con [0, 0] = -1):")
print(submatriz2)

# Verificar que la matriz original no cambió
print("\nMatriz original después de modificar la submatriz:")
print(matriz)