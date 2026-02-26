import pandas as pd

#portada
print("=" * 55)
print("        PROYECTO DE ESTADÍSTICA DE AMALIA SOTO")
print("=" * 55)
print("Este proyecto tomará un archivo CSV con números")
print("y calculará varias cosas, como:")
print("- número de datos (n)")
print("- cuartiles")
print("- RIC (rango intercuartílico)")
print("- media, mediana, etc.")
print("- Sturges graficas, etc")
print("=" * 55)
print()

df = pd.read_csv("edades.csv")

df["edades"] = pd.to_numeric(df["edades"], errors="coerce")
# Contar valores válidos (no nulos)
n = df["edades"].count()

print(f"El número de valores (n) del documento es: {n}")