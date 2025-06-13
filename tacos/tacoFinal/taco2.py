import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Leer el archivo limpio y ya ordenado
df = pd.read_csv("tacos_CDMX_sorted.csv")

# Seleccionar y ordenar todas las columnas que se van a usar
dfCompleto = df[['name','address', 'userRatingCount','rating', 'priceLevel', 'website', 'lat', 'lng']]  
print("Columnas disponibles:")# Mostrar las columnas en orden
print(dfCompleto.columns.tolist())
print(dfCompleto)# Mostrar el DataFrame completo

dfUserRatingCount = dfCompleto[['name', 'userRatingCount', 'rating','address']].copy()
# Ordenar por número de calificaciones (userRatingCount)    
dfUserRatingCount = dfUserRatingCount.sort_values(by='userRatingCount', ascending=False)

# Mostrar las primeras filas del DataFrame ordenado
print(dfUserRatingCount)

mediaRating = dfUserRatingCount['rating'].mean()
print("Media de rating:", mediaRating)

# limpiar solo las taquerías con ratings válidos y al menos 10 calificaciones, además de excluir las que tienen rating perfecto (5.0) o muy bajo (1.0).

# 1. Eliminar filas donde falta el rating (NaN)
dfFiltrado = dfUserRatingCount.dropna(subset=['rating'])

# 2. Filtrar lugares con al menos 10 calificaciones
dfFiltrado = dfFiltrado[dfFiltrado['userRatingCount'] >= 10]
# Mostrar el DataFrame filtrado
print("Taquerías con al menos 10 calificaciones:")#contar las filas filtradas
print(dfFiltrado.shape[0], "taquerías encontradas.")

# 3. Excluir calificaciones perfectas de 5.0 y calificaciones muy bajas de 1.0
dfFiltrado = dfFiltrado[(dfFiltrado['rating'] != 5.0) & (dfFiltrado['rating'] != 1.0)]

# Mostrar el DataFrame final filtrado
print("Taquerías con calificaciones realistas (sin 5.0 ni 1.0 y al menos 10 opiniones):")
print(dfFiltrado.shape[0], "taquerías encontradas.")

# Volver a calcular la media de ratings ya filtrados
mediaRealista = dfFiltrado['rating'].mean()
print("Media de rating filtrada:", mediaRealista)

# Preparar las variables para la regresión
X = dfFiltrado[['userRatingCount']]  # variable independiente (X)
y = dfFiltrado['rating']             # variable dependiente (y)

# Crear el modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Hacer predicciones
y_pred = modelo.predict(X)

# Mostrar coeficientes
print("Coeficiente (pendiente):", modelo.coef_[0])
print("Intercepto:", modelo.intercept_)

# Graficar datos y línea de regresión
plt.scatter(X, y, alpha=0.4, label='Datos reales')
plt.plot(X, y_pred, color='red', label='Regresión lineal')
plt.xlabel('Número de calificaciones')
plt.ylabel('Rating')
plt.title('Regresión lineal: Rating vs. Número de calificaciones')
plt.legend()
plt.grid(True)
plt.show()