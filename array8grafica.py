import numpy as np
import math as m
import matplotlib.pyplot as plt

def explicar(mensaje):
    print(f"\n🔹 {mensaje}")
    input("Presiona Enter para continuar...\n")

explicar("Se creará un array de grados de 0 a 360 con paso de 1.")
grados = np.array([i for i in range(0, 361, 1)], dtype='float')
print("Array de grados:\n", grados)

explicar("Se mostrará el valor de pi usando la librería math.")
print("Valor de pi:", m.pi)

explicar("Convertiremos los grados a radianes usando la fórmula: radianes = grados * (pi / 180).")
np_radianes = grados * (m.pi / 180)
print("Radianes equivalentes:\n", np_radianes)

explicar("Calcularemos el seno de cada valor en radianes usando np.sin().")
fsin = np.sin(np_radianes)
print("Seno de cada radian:\n", fsin)

# 📈 Gráfico del seno
plt.figure(figsize=(10, 4))
plt.plot(grados, fsin, label='Seno', color='blue')
plt.title('Función Seno')
plt.xlabel('Grados')
plt.ylabel('Seno')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

explicar("Se creará una matriz 1D de radianes desde 0° a 180° con paso de 10°, y se usará np.radians().")
radianesA = np.radians(np.array([i for i in range(0, 181, 10)], dtype='float'))
print("Radianes convertidos desde grados (1D):\n", radianesA)

explicar("Se calculará el coseno de los radianes anteriores usando np.cos().")
fcos1 = np.cos(radianesA)
print("Coseno:\n", fcos1)

# 📈 Gráfico del coseno (1D)
plt.figure(figsize=(10, 4))
plt.plot(np.degrees(radianesA), fcos1, label='Coseno', color='red', marker='o')
plt.title('Función Coseno (0° a 180°)')
plt.xlabel('Grados')
plt.ylabel('Coseno')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

explicar("Ahora se creará una matriz 4x5 de radianes desde 0° a 190° usando reshape().")
radianes2 = np.radians(np.array([i for i in range(0, 191, 10)], dtype='float').reshape(4, 5))
print("Matriz de radianes 4x5:\n", radianes2)

explicar("Se calculará el coseno de la matriz 4x5 anterior.")
fcos2 = np.cos(radianes2)
print("Coseno matriz 4x5:\n", fcos2)

# 📈 Gráfico del coseno (matriz 4x5 a plano)
plt.figure(figsize=(10, 4))
plt.plot(np.degrees(radianes2).flatten(), fcos2.flatten(), label='Coseno 4x5', color='green', marker='x')
plt.title('Coseno de matriz 4x5 (Aplanada)')
plt.xlabel('Grados')
plt.ylabel('Coseno')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

explicar("Se generarán 11 valores equidistantes entre 0 y 1 usando np.linspace().")
valores_equidistantes = np.linspace(0, 1, 11)
print("Valores equidistantes:\n", valores_equidistantes)

explicar("Se creará una matriz de 100x100 con valores entre 0 y 1, y se calculará su tangente.")
ejercicio1_examen = np.tan(np.linspace(0, 1, 100 * 100).reshape(100, 100))
print("Tangente de matriz 100x100:\n", ejercicio1_examen)

# 📈 Mapa de calor de la tangente
plt.figure(figsize=(6, 5))
plt.imshow(ejercicio1_examen, cmap='viridis', aspect='auto')
plt.colorbar(label='Tangente')
plt.title('Tangente en matriz 100x100')
plt.xlabel('Columnas')
plt.ylabel('Filas')
plt.tight_layout()
plt.show()



