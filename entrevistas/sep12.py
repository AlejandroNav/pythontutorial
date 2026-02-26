def identidad(n):
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            if i == j:
                fila.append(1)
            else:
                fila.append(0)
        matriz.append(fila)
    return matriz

# Ejemplo
for fila in identidad(4):
    print(fila)
