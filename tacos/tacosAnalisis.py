import pandas as pd
import matplotlib.pyplot as plt

# Cambia esta ruta por la del archivo real que quieres analizar
file_path = "tacos_CDMX.csv"

# Leer el archivo CSV
df = pd.read_csv(file_path)

# Separar los que tienen priceLevel y los que no
with_price = df[df['priceLevel'].notna()]
without_price = df[df['priceLevel'].isna()]

# Conteo de cada nivel de precio
price_counts = with_price['priceLevel'].value_counts()

# Mostrar resumen
print("Resumen:")
print(f"Total de lugares: {len(df)}")
print(f"Con priceLevel: {len(with_price)}")
print(f"Sin priceLevel: {len(without_price)}")
print("\nDistribución de niveles de precio:")
print(price_counts)

# Graficar
plt.figure(figsize=(8, 4))
price_counts.plot(kind='bar', color='green')
plt.title("Distribución de 'priceLevel'")
plt.xlabel("Nivel de precio")
plt.ylabel("Número de lugares")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("grafica_priceLevel.png")
plt.show()
