import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# ============================================================
# 0) PORTADA (3 líneas)
# ============================================================
def portada():
    print("=" * 55)
    print("PROYECTO DE ESTADÍSTICA — AMALIA SOTO")
    print("=" * 55)
    print()

# ============================================================
# 1) CARGA (si falla, usa ejemplo)
# ============================================================
def leer_csv_o_ejemplo(ruta_csv: str) -> pd.DataFrame:
    csv_ejemplo = """edades,peso
3,55
8,60
9,58
10,62
10,65
11,59
11,67
12,70
12,72
12,68
13,75
13,73
14,78
14,80
15,82
15,77
16,85
17,88
18,90
19,95
20,100
50,120
"""
    try:
        return pd.read_csv(ruta_csv)
    except Exception:
        print(f"⚠ No pude cargar '{ruta_csv}'. Usando datos de ejemplo.")
        return pd.read_csv(StringIO(csv_ejemplo))

def convertir_a_numerico(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(lambda col: pd.to_numeric(col, errors="coerce"))

def columnas_numericas(df_num: pd.DataFrame) -> list[str]:
    return [c for c in df_num.columns if df_num[c].count() > 0]

def preparar_datos_columna(df_num: pd.DataFrame, col: str) -> np.ndarray:
    return df_num[col].dropna().sort_values().to_numpy()

# ============================================================
# 2) CUARTILES (Tukey) + ATÍPICOS
# ============================================================
def cuartiles_tukey(datos: np.ndarray) -> tuple[float, float, float]:
    n = len(datos)
    q2 = float(np.median(datos))

    if n % 2 == 0:
        lower = datos[: n // 2]
        upper = datos[n // 2 :]
    else:
        lower = datos[: n // 2]
        upper = datos[n // 2 + 1 :]

    q1 = float(np.median(lower))
    q3 = float(np.median(upper))
    return q1, q2, q3

def limites_tukey(q1: float, q3: float) -> tuple[float, float, float]:
    ric = q3 - q1
    lim_inf = q1 - 1.5 * ric
    lim_sup = q3 + 1.5 * ric
    return ric, lim_inf, lim_sup

def atipicos_por_limites(datos: np.ndarray, lim_inf: float, lim_sup: float) -> np.ndarray:
    return datos[(datos < lim_inf) | (datos > lim_sup)]

# ============================================================
# 3) STURGES (k, amplitud, intervalos, frecuencias)
# ============================================================
def tabla_sturges(datos: np.ndarray):
    datos = np.asarray(datos)
    n = len(datos)
    minimo = float(np.min(datos))
    maximo = float(np.max(datos))
    rango = maximo - minimo

    k_real = 1 + np.log2(n)
    k = int(np.ceil(k_real))

    # amplitud usando k entero (como suele hacerse)
    ancho = int(np.ceil(rango / k))

    # ---- cortes estilo tu cuaderno ----
    # empezamos en minimo, y vamos sumando 'ancho',
    # pero ajustamos los bordes para que queden como 3,11,20,29...
    edges = [minimo]
    for _ in range(k - 1):
        edges.append(edges[-1] + ancho)
    edges.append(maximo)  # cerrar en el máximo exacto

    # Ajuste para que coincida con tu hoja (11, 20, 29, 38, 47)
    # Si el mínimo es 3 y ancho es 9, esto deja: 3,12,21...
    # Tu hoja usa: 3,11,20... => restamos 1 a los bordes internos.
    for i in range(1, len(edges) - 1):
        edges[i] -= 1

    # Asegura monotonicidad (por si acaso)
    edges = sorted(edges)

    # Intervalos: [a,b) excepto el último que incluye el máximo
    cats = pd.cut(datos, bins=edges, right=False, include_lowest=True)
    freq = pd.Series(cats).value_counts(sort=False)

    tabla = pd.DataFrame({
        "Intervalo": [str(i) for i in freq.index],
        "Frecuencia": freq.values
    })

    return k_real, k, ancho, minimo, maximo, rango, edges, tabla

# ============================================================
# 4) BOXPLOTS + HISTOGRAMA (guardar en carpeta resultados)
# ============================================================
def boxplot_columna(datos: np.ndarray, col: str, carpeta_salida: str):
    plt.figure(figsize=(3, 10))
    plt.boxplot(datos, vert=True, widths=0.35)
    plt.title(f"Boxplot - {col}")
    plt.ylabel(col)
    plt.xticks([1], [col])
    plt.tight_layout()

    ruta = os.path.join(carpeta_salida, f"boxplot_{col}.png")
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"✓ boxplot_{col}.png")

def boxplot_columna_con_puntos(datos: np.ndarray, col: str, carpeta_salida: str):
    plt.figure(figsize=(3, 10))
    plt.boxplot(datos, vert=True, widths=0.35)

    rng = np.random.default_rng(42)
    x = 1 + rng.normal(0, 0.03, size=len(datos))
    plt.scatter(x, datos, alpha=0.7, s=18, zorder=3)

    plt.title(f"Boxplot + puntos - {col}")
    plt.ylabel(col)
    plt.xticks([1], [col])
    plt.tight_layout()

    ruta = os.path.join(carpeta_salida, f"boxplot_puntos_{col}.png")
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"✓ boxplot_puntos_{col}.png")

def histograma_sturges(datos: np.ndarray, edges, col: str, carpeta_salida: str):
    plt.figure(figsize=(6, 4))
    plt.hist(datos, bins=edges)
    plt.title(f"Histograma (Sturges) - {col}")
    plt.xlabel(col)
    plt.ylabel("Frecuencia")
    plt.tight_layout()

    ruta = os.path.join(carpeta_salida, f"hist_sturges_{col}.png")
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"✓ hist_sturges_{col}.png")

# ============================================================
# 5) MAIN
# ============================================================
def main():
    portada()

    carpeta_salida = "resultados"
    os.makedirs(carpeta_salida, exist_ok=True)

    df = leer_csv_o_ejemplo("datos.csv")
    df_num = convertir_a_numerico(df)

    cols = columnas_numericas(df_num)
    if not cols:
        raise ValueError("No encontré ninguna columna numérica en el CSV.")

    for col in cols:
        datos = preparar_datos_columna(df_num, col)
        n = len(datos)

        # --- Tukey + atípicos ---
        q1, q2, q3 = cuartiles_tukey(datos)
        ric, lim_inf, lim_sup = limites_tukey(q1, q3)
        atipicos = atipicos_por_limites(datos, lim_inf, lim_sup)

        print("-" * 55)
        print("Columna:", col)
        print("n:", n)
        print("Q1:", q1, "Q2:", q2, "Q3:", q3)
        print("RIC:", ric)
        print("Límites:", lim_inf, lim_sup)
        print("Atípicos:", atipicos.tolist() if len(atipicos) else "No hay")

        # --- Sturges ---
        k_real, k, ancho, minimo, maximo, rango, edges, tabla = tabla_sturges(datos)
        print("\nSturges:")
        print("Min:", minimo, "Max:", maximo, "Rango:", rango)
        print("k_real:", k_real, "=> k:", k)
        print("Amplitud:", ancho)
        print(tabla.to_string(index=False))

        # --- Gráficas ---
        boxplot_columna(datos, col, carpeta_salida)
        boxplot_columna_con_puntos(datos, col, carpeta_salida)
        histograma_sturges(datos, edges, col, carpeta_salida)

    print("-" * 55)
    print(f"Gráficas guardadas en: ./{carpeta_salida}/")

if __name__ == "__main__":
    main()