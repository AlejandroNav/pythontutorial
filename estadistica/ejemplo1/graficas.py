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

def quitar_atipicos(datos: np.ndarray, lim_inf: float, lim_sup: float) -> np.ndarray:
    """Quita atípicos (filtra) y regresa solo los que están dentro de los límites."""
    return datos[(datos >= lim_inf) & (datos <= lim_sup)]

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

    ancho = int(np.ceil(rango / k)) if k > 0 else 1
    if ancho == 0:
        ancho = 1

    edges = [minimo + i * ancho for i in range(k + 1)]
    if edges[-1] <= maximo:
        edges[-1] = maximo + 1e-9

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
def boxplot_columna(datos: np.ndarray, col: str, carpeta_salida: str, sufijo: str, showfliers: bool = True):
    plt.figure(figsize=(3, 10))
    plt.boxplot(datos, vert=True, widths=0.35, showfliers=showfliers)
    plt.title(f"Boxplot ({sufijo}) - {col}")
    plt.ylabel(col)
    plt.xticks([1], [col])
    plt.tight_layout()

    ruta = os.path.join(carpeta_salida, f"boxplot_{col}_{sufijo}.png")
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"✓ boxplot_{col}_{sufijo}.png")

def histograma_sturges(tabla: pd.DataFrame, col: str, carpeta_salida: str, sufijo: str):
    etiquetas = tabla["Intervalo"].astype(str).tolist()
    frecuencias = tabla["Frecuencia"].to_numpy()

    plt.figure(figsize=(10, 4))
    plt.bar(range(len(frecuencias)), frecuencias)
    plt.title(f"Histograma (Sturges) ({sufijo}) - {col}")
    plt.xlabel("Intervalos")
    plt.ylabel("Frecuencia")
    plt.xticks(range(len(etiquetas)), etiquetas, rotation=45, ha="right")
    plt.tight_layout()

    ruta = os.path.join(carpeta_salida, f"hist_sturges_{col}_{sufijo}.png")
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"✓ hist_sturges_{col}_{sufijo}.png")

# ============================================================
# 5) MAIN
# ============================================================
def main():
    portada()

    carpeta_salida = "resultados"
    os.makedirs(carpeta_salida, exist_ok=True)

    df = leer_csv_o_ejemplo("Prub1.csv")
    df_num = convertir_a_numerico(df)

    cols = columnas_numericas(df_num)
    if not cols:
        raise ValueError("No encontré ninguna columna numérica en el CSV.")

    for col in cols:
        datos = preparar_datos_columna(df_num, col)

        # --- Tukey + atípicos (con TODOS los datos) ---
        q1, q2, q3 = cuartiles_tukey(datos)
        ric, lim_inf, lim_sup = limites_tukey(q1, q3)
        atipicos = atipicos_por_limites(datos, lim_inf, lim_sup)

        print("-" * 55)
        print("Columna:", col)
        print("n:", len(datos))
        print("Q1:", q1, "Q2:", q2, "Q3:", q3)
        print("RIC:", ric)
        print("Límites:", lim_inf, lim_sup)
        print("Atípicos:", atipicos.tolist() if len(atipicos) else "No hay")

        # --- DATOS SIN ATÍPICOS (FILTRADO REAL) ---
        datos_sin = quitar_atipicos(datos, lim_inf, lim_sup)

        # Debug útil: qué se quitó y qué quedó
        quitados = datos[(datos < lim_inf) | (datos > lim_sup)]
        print("\nQuitando atípicos (lista que queda):")
        print(datos_sin.tolist())
        print("Valores quitados:", quitados.tolist() if len(quitados) else "Ninguno")
        print("n_sin_atipicos:", len(datos_sin))

        # --- Sturges (con datos completos) ---
        k_real, k, ancho, minimo, maximo, rango, edges, tabla = tabla_sturges(datos)
        print("\nSturges (con atípicos):")
        print("Min:", minimo, "Max:", maximo, "Rango:", rango)
        print("k_real:", k_real, "=> k:", k)
        print("Amplitud:", ancho)
        print(tabla.to_string(index=False))

        # --- Sturges (sin atípicos) ---
        tabla2 = None
        if len(datos_sin) >= 2:
            k_real2, k2, ancho2, min2, max2, rango2, edges2, tabla2 = tabla_sturges(datos_sin)
            print("\nSturges (sin atípicos):")
            print("Min:", min2, "Max:", max2, "Rango:", rango2)
            print("k_real:", k_real2, "=> k:", k2)
            print("Amplitud:", ancho2)
            print(tabla2.to_string(index=False))

        # --- Gráficas ---
        # 1) Boxplot CON atípicos
        boxplot_columna(datos, col, carpeta_salida, "con_atipicos", showfliers=True)
        histograma_sturges(tabla, col, carpeta_salida, "con_atipicos")

        # 2) Boxplot SIN atípicos (ya filtrados)
        if len(datos_sin) > 0:
            boxplot_columna(datos_sin, col, carpeta_salida, "sin_atipicos", showfliers=False)
            if tabla2 is not None:
                histograma_sturges(tabla2, col, carpeta_salida, "sin_atipicos")

    print("-" * 55)
    print(f"Gráficas guardadas en: ./{carpeta_salida}/")

if __name__ == "__main__":
    main()