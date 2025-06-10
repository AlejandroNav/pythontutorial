import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
file_path = "tacos_CDMX.csv"  # Asegúrate de que esté en el mismo folder o usa la ruta absoluta
df = pd.read_csv(file_path)

# Análisis 1: Cuántos tienen rating y cuántos no
con_rating = df[df["rating"].notna()]
sin_rating = df[df["rating"].isna()]

print(f"Con rating: {len(con_rating)}")
print(f"Sin rating: {len(sin_rating)}")

# Análisis 2: Estadísticas generales de rating
print("\n=== Estadísticas de todos los lugares con rating ===")
print(con_rating["rating"].describe(percentiles=[0.25, 0.5, 0.75, 0.9]))

# Histograma de rating
plt.figure(figsize=(8, 4))
plt.hist(con_rating["rating"], bins=10, edgecolor='black')
plt.title("Distribución de Ratings")
plt.xlabel("Rating")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.tight_layout()
plt.show()

# Análisis 3: Top 25% por número de reseñas
threshold = con_rating["userRatingCount"].quantile(0.75)
top25 = con_rating[con_rating["userRatingCount"] >= threshold]

print(f"\nTop 25% por número de reseñas (más de {threshold} reseñas): {len(top25)} lugares")

# Estadísticas de rating en ese subconjunto
print("\n=== Estadísticas de rating en el top 25% ===")
print(top25["rating"].describe())

# Histograma para top 25%
plt.figure(figsize=(8, 4))
plt.hist(top25["rating"], bins=10, edgecolor='black', color='orange')
plt.title("Distribución de Ratings (Top 25% más reseñado)")
plt.xlabel("Rating")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.tight_layout()
plt.show()
