# analisis_csv_basico.py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Leer CSV y extraer columna numérica
def leer_columna_numerica(ruta_csv, columna=None):
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    if os.path.getsize(ruta_csv) == 0:
        raise ValueError(f"El archivo está vacío (0 bytes): {ruta_csv}")

    # Intenta detectar separador automáticamente (coma, punto y coma, etc.)
    try:
        df = pd.read_csv(ruta_csv, sep=None, engine="python", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(ruta_csv, sep=None, engine="python", encoding="latin1")
    except pd.errors.EmptyDataError:
        raise ValueError("El CSV no contiene datos legibles.")
    except Exception as e:
        raise ValueError(f"No se pudo leer el CSV: {e}")

    if df.empty:
        raise ValueError("El CSV se leyó, pero no tiene filas.")

    # Si el usuario especifica columna
    if columna is not None:
        if columna not in df.columns:
            raise ValueError(
                f"La columna '{columna}' no existe.\n"
                f"Columnas disponibles: {list(df.columns)}"
            )
        serie = pd.to_numeric(df[columna], errors="coerce").dropna()
        nombre_columna = columna
    else:
        # Buscar primera columna numérica útil
        serie = None
        nombre_columna = None
        for col in df.columns:
            s_temp = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(s_temp) > 0:
                serie = s_temp
                nombre_columna = col
                break

        if serie is None:
            raise ValueError("No se encontró ninguna columna numérica útil.")

    if len(serie) == 0:
        raise ValueError("La columna seleccionada no tiene datos numéricos válidos.")

    return df, pd.Series(serie, dtype="float64"), nombre_columna

# 2) ESTADÍSTICOS + ATÍPICOS 
def calcular_estadisticos(serie):
    s = pd.Series(serie, dtype="float64").dropna().sort_values().reset_index(drop=True)

    q1 = s.quantile(0.25)
    q2 = s.quantile(0.50)
    q3 = s.quantile(0.75)
    q4 = s.quantile(1.00)

    ric = q3 - q1
    lim_inf = q1 - 1.5 * ric
    lim_sup = q3 + 1.5 * ric

    mask = (s >= lim_inf) & (s <= lim_sup)
    s_sin = s[mask].reset_index(drop=True)
    s_ati = s[~mask].reset_index(drop=True)

    resultados = {
        "n": int(s.count()),
        "minimo": float(s.min()),
        "Q1": float(q1),
        "Q2": float(q2),
        "Q3": float(q3),
        "Q4": float(q4),
        "maximo": float(s.max()),
        "rango": float(s.max() - s.min()),
        "RIC": float(ric),
        "media": float(s.mean()),
        "mediana": float(s.median()),
        "varianza_muestral": float(s.var(ddof=1)) if len(s) > 1 else np.nan,
        "varianza_poblacional": float(s.var(ddof=0)),
        "limite_inferior_atipicos": float(lim_inf),
        "limite_superior_atipicos": float(lim_sup),
        "bigote_inferior_real": float(s_sin.min()) if len(s_sin) else np.nan,
        "bigote_superior_real": float(s_sin.max()) if len(s_sin) else np.nan,
        "num_sin_atipicos": int(mask.sum()),
        "num_atipicos": int((~mask).sum()),
    }

    return resultados, s, s_sin, s_ati

# 3) STURGES + TABLAS DE FRECUENCIAS
def calcular_sturges(serie):
    s = pd.Series(serie, dtype="float64").dropna()
    n = len(s)

    if n == 0:
        return {"n": 0, "k_sturges": 0, "k_sturges_real": np.nan, "amplitud_aprox": np.nan}

    if n == 1:
        k_real = 1.0
        k = 1
    else:
        k_real = 1 + 3.322 * np.log10(n)
        k = int(np.ceil(k_real))

    rango = s.max() - s.min()
    amplitud = (rango / k) if k > 0 else np.nan

    return {
        "n": int(n),
        "k_sturges_real": float(k_real),
        "k_sturges": int(k),
        "minimo": float(s.min()),
        "maximo": float(s.max()),
        "rango": float(rango),
        "amplitud_aprox": float(amplitud),
    }


def tabla_frecuencias_simple(serie):
    s = pd.Series(serie).dropna()
    freq = s.value_counts().sort_index()

    df = pd.DataFrame({
        "valor": freq.index,
        "fi": freq.values
    })
    total = df["fi"].sum()
    df["hi"] = df["fi"] / total
    df["porcentaje"] = df["hi"] * 100
    df["Fi"] = df["fi"].cumsum()
    df["porcentaje_acumulado"] = df["porcentaje"].cumsum()
    return df


def tabla_frecuencias_sturges(serie):
    s = pd.Series(serie, dtype="float64").dropna()
    info = calcular_sturges(s)

    if len(s) == 0:
        cols = ["intervalo", "fi", "hi", "porcentaje", "Fi", "porcentaje_acumulado"]
        return pd.DataFrame(columns=cols), info

    if s.min() == s.max():
        df = pd.DataFrame({"intervalo": [f"[{s.min()}, {s.max()}]"], "fi": [len(s)]})
    else:
        k = max(1, info["k_sturges"])
        cats = pd.cut(s, bins=k, include_lowest=True, duplicates="drop")
        freq = cats.value_counts().sort_index()
        df = pd.DataFrame({
            "intervalo": freq.index.astype(str),
            "fi": freq.values
        })

    total = df["fi"].sum()
    df["hi"] = df["fi"] / total
    df["porcentaje"] = df["hi"] * 100
    df["Fi"] = df["fi"].cumsum()
    df["porcentaje_acumulado"] = df["porcentaje"].cumsum()

    return df, info

# 4) GRÁFICAS
def guardar_histograma(serie, ruta_png, bins="auto", titulo="Histograma"):
    s = pd.Series(serie, dtype="float64").dropna()
    if len(s) == 0:
        return

    if bins == "sturges":
        bins = max(1, calcular_sturges(s)["k_sturges"])

    plt.figure(figsize=(8, 5))
    plt.hist(s, bins=bins, edgecolor="black")
    plt.title(titulo)
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(ruta_png, dpi=150)
    plt.close()


def guardar_boxplot(serie, ruta_png, titulo="Boxplot", mostrar_atipicos=True):
    s = pd.Series(serie, dtype="float64").dropna()
    if len(s) == 0:
        return

    plt.figure(figsize=(8, 4))
    plt.boxplot(s, vert=False, showfliers=mostrar_atipicos)
    plt.title(titulo)
    plt.xlabel("Valor")
    plt.tight_layout()
    plt.savefig(ruta_png, dpi=150)
    plt.close()


# ============================================================
# 5) FUNCIÓN PRINCIPAL
# ============================================================
def analizar_csv_estadistico(ruta_csv, columna=None, carpeta_salida="salida_proyecto"):
    os.makedirs(carpeta_salida, exist_ok=True)

    # Leer
    df, serie, nombre_columna = leer_columna_numerica(ruta_csv, columna)

    # Calcular
    resultados, s, s_sin, s_ati = calcular_estadisticos(serie)
        # Mostrar en consola (estricto) los estadísticos clave
    print("\n=== ESTADÍSTICOS CLAVE ===")
    claves_mostrar = [
        "n", "minimo", "Q1", "Q2", "Q3", "Q4",
        "maximo", "rango", "RIC"
    ]
    for k in claves_mostrar:
        v = resultados[k]
        if isinstance(v, float):
            print(f'"{k}": {v}')
        else:
            print(f'"{k}": {v}')
    df_freq_simple = tabla_frecuencias_simple(s)
    df_freq_sturges, info_sturges = tabla_frecuencias_sturges(s)

    # Guardar CSVs
    pd.DataFrame([resultados]).to_csv(os.path.join(carpeta_salida, "estadisticos_resumen.csv"), index=False)
    pd.DataFrame([info_sturges]).to_csv(os.path.join(carpeta_salida, "sturges_resumen.csv"), index=False)
    df_freq_simple.to_csv(os.path.join(carpeta_salida, "tabla_frecuencias_simple.csv"), index=False)
    df_freq_sturges.to_csv(os.path.join(carpeta_salida, "tabla_frecuencias_sturges.csv"), index=False)
    pd.DataFrame({nombre_columna: s}).to_csv(os.path.join(carpeta_salida, "datos_ordenados.csv"), index=False)
    pd.DataFrame({nombre_columna: s_sin}).to_csv(os.path.join(carpeta_salida, "datos_sin_atipicos.csv"), index=False)
    pd.DataFrame({nombre_columna: s_ati}).to_csv(os.path.join(carpeta_salida, "datos_atipicos.csv"), index=False)

    # Gráficas con atípicos
    guardar_histograma(s, os.path.join(carpeta_salida, "histograma_con_atipicos_auto.png"),
                       bins="auto", titulo=f"Histograma con atípicos (auto) - {nombre_columna}")
    guardar_histograma(s, os.path.join(carpeta_salida, "histograma_con_atipicos_sturges.png"),
                       bins="sturges", titulo=f"Histograma con atípicos (Sturges) - {nombre_columna}")
    guardar_boxplot(s, os.path.join(carpeta_salida, "boxplot_con_atipicos.png"),
                    titulo=f"Boxplot con atípicos - {nombre_columna}", mostrar_atipicos=True)

    # Gráficas sin atípicos
    if len(s_sin) > 0:
        guardar_histograma(s_sin, os.path.join(carpeta_salida, "histograma_sin_atipicos_auto.png"),
                           bins="auto", titulo=f"Histograma sin atípicos (auto) - {nombre_columna}")
        guardar_histograma(s_sin, os.path.join(carpeta_salida, "histograma_sin_atipicos_sturges.png"),
                           bins="sturges", titulo=f"Histograma sin atípicos (Sturges) - {nombre_columna}")
        guardar_boxplot(s_sin, os.path.join(carpeta_salida, "boxplot_sin_atipicos.png"),
                        titulo=f"Boxplot sin atípicos - {nombre_columna}", mostrar_atipicos=False)

    # Resumen corto
    print(f"\n✅ Archivo analizado: {ruta_csv}")
    print(f"✅ Columna usada: {nombre_columna}")
    print(f"✅ Datos válidos: {len(serie)}")
    print(f"✅ Atípicos detectados: {resultados['num_atipicos']}")
    print(f"✅ Carpeta de salida: {os.path.abspath(carpeta_salida)}")

    return {
        "df_original": df,
        "columna": nombre_columna,
        "estadisticos": resultados,
        "sturges": info_sturges,
        "frecuencia_simple": df_freq_simple,
        "frecuencia_sturges": df_freq_sturges,
    }

if __name__ == "__main__":
    RUTA_CSV = "ejemplo.csv"      # <- cambiar por el nombre del archivo final
    COLUMNA = None                
    SALIDA = "salida_proyecto"

    analizar_csv_estadistico(
        ruta_csv=RUTA_CSV,
        columna=COLUMNA,
        carpeta_salida=SALIDA
    )