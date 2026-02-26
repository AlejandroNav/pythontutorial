import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 0) PORTADA (3 líneas)
# ============================================================
def portada():
    print("=" * 55)
    print("PROYECTO DE ESTADÍSTICA — AMALIA SOTO")
    print("=" * 55)
    print()

# ============================================================
# 1) CARGA Y LIMPIEZA
# ============================================================
def leer_csv(ruta_csv: str) -> pd.DataFrame:
    return pd.read_csv(ruta_csv)

def convertir_a_numerico(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(lambda col: pd.to_numeric(col, errors="coerce"))

def columnas_numericas(df_num: pd.DataFrame) -> list[str]:
    return [c for c in df_num.columns if df_num[c].count() > 0]

def preparar_datos_columna(df_num: pd.DataFrame, col: str) -> np.ndarray:
    return df_num[col].dropna().sort_values().to_numpy()

# ============================================================
# 2) ESTADÍSTICA (Tukey)
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
# 3) REPORTE
# ============================================================
def imprimir_resultados(col: str, n: int, q1: float, q2: float, q3: float,
                        ric: float, lim_inf: float, lim_sup: float, atipicos: np.ndarray):
    print("-" * 55)
    print("Columna:", col)
    print("n:", n)
    print("Q1:", q1, "Q2:", q2, "Q3:", q3)
    print("RIC:", ric)
    print("Límites:", lim_inf, lim_sup)
    print("Atípicos:", atipicos.tolist() if len(atipicos) else "No hay")

# ============================================================
# 4) BOXPLOT (guardar en carpeta)
# ============================================================
def boxplot_columna(datos: np.ndarray, col: str, carpeta_salida: str):
    plt.figure()
    plt.boxplot(datos)  # muestra atípicos
    plt.title(f"Boxplot - {col}")
    plt.ylabel(col)
    plt.tight_layout()

    ruta = os.path.join(carpeta_salida, f"boxplot_{col}.png")
    plt.savefig(ruta, dpi=150)
    plt.close()

# ============================================================
# 5) MAIN
# ============================================================
def main():
    portada()

    carpeta_salida = "resultados"
    os.makedirs(carpeta_salida, exist_ok=True)

    df = leer_csv("edades.csv")  # <-- cambia el nombre si quieres
    df_num = convertir_a_numerico(df)

    cols = columnas_numericas(df_num)
    if not cols:
        raise ValueError("No encontré ninguna columna numérica en el CSV.")

    for col in cols:
        datos = preparar_datos_columna(df_num, col)
        n = len(datos)

        q1, q2, q3 = cuartiles_tukey(datos)
        ric, lim_inf, lim_sup = limites_tukey(q1, q3)

        atipicos = atipicos_por_limites(datos, lim_inf, lim_sup)
        imprimir_resultados(col, n, q1, q2, q3, ric, lim_inf, lim_sup, atipicos)

        boxplot_columna(datos, col, carpeta_salida)

    print("-" * 55)
    print(f"Gráficas guardadas en: ./{carpeta_salida}/")

if __name__ == "__main__":
    main()