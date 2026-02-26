# ============================================================
# PROYECTO FINAL: Análisis estadístico desde CSV
# ------------------------------------------------------------
# Lee un CSV (que dará el profesor), selecciona una columna numérica
# y calcula:
#   - Q1, Q2, Q3, Q4
#   - RIC (rango intercuartílico)
#   - media, mediana, varianza
#   - límites inferior/superior para atípicos (fences)
#   - bigotes reales del boxplot
#   - tabla de frecuencias simple
#   - tabla de frecuencias agrupada por intervalos (Regla de Sturges)
# Genera:
#   - histogramas con y sin atípicos (auto y Sturges)
#   - boxplot con y sin atípicos
# Guarda resultados en CSV e imágenes.
# ============================================================

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1) GENERAR CSV DE EJEMPLO (OPCIONAL)
# ============================================================
def generar_csv_ejemplo(
    nombre_csv="edades_20_alumnos.csv",
    n=20,
    minimo=16,
    maximo=28,
    semilla=42
):
    """
    Genera un CSV de ejemplo con una columna 'edad'
    con n valores aleatorios enteros entre minimo y maximo.
    """
    np.random.seed(semilla)
    edades = np.random.randint(minimo, maximo + 1, size=n)
    df_ejemplo = pd.DataFrame({"edad": edades})
    df_ejemplo.to_csv(nombre_csv, index=False, encoding="utf-8")
    print(f"✅ CSV de ejemplo generado: {nombre_csv}")
    print(df_ejemplo)
    return df_ejemplo


# ============================================================
# 2) LEER Y LIMPIAR DATOS DESDE CSV
# ============================================================
def leer_columna_numerica_desde_csv(ruta_csv, columna=None):
    """
    Lee un CSV y devuelve:
    - df_original: DataFrame completo
    - serie_numerica: columna numérica limpia (sin NaN)
    - nombre_columna: nombre de la columna usada

    Si 'columna' es None, usa la primera columna que pueda convertirse
    a numérica con datos válidos.
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    df = pd.read_csv(ruta_csv)

    if df.empty:
        raise ValueError("El CSV está vacío.")

    if columna is not None:
        if columna not in df.columns:
            raise ValueError(
                f"La columna '{columna}' no existe.\n"
                f"Columnas disponibles: {list(df.columns)}"
            )
        serie = pd.to_numeric(df[columna], errors="coerce").dropna()
        nombre_columna = columna
    else:
        serie = None
        nombre_columna = None
        for col in df.columns:
            serie_temp = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(serie_temp) > 0:
                serie = serie_temp
                nombre_columna = col
                break

        if serie is None:
            raise ValueError("No se encontró ninguna columna numérica útil en el CSV.")

    if len(serie) == 0:
        raise ValueError("La columna seleccionada no tiene datos numéricos válidos.")

    return df, serie, nombre_columna


# ============================================================
# 3) ESTADÍSTICOS DESCRIPTIVOS + ATÍPICOS + BIGOTES
# ============================================================
def calcular_estadisticos(serie):
    """
    Calcula estadísticos principales de una serie numérica:
    - Cuartiles Q1, Q2, Q3, Q4
    - RIC
    - Media, mediana, varianzas
    - Límites teóricos para atípicos (fences)
    - Bigotes reales del boxplot
    - Separación de datos con y sin atípicos
    """
    s = pd.Series(serie, dtype="float64").dropna().sort_values().reset_index(drop=True)

    if len(s) == 0:
        raise ValueError("No hay datos numéricos para calcular estadísticas.")

    q1 = s.quantile(0.25)
    q2 = s.quantile(0.50)  # mediana
    q3 = s.quantile(0.75)
    q4 = s.quantile(1.00)  # máximo (percentil 100)

    ric = q3 - q1

    media = s.mean()
    mediana = s.median()

    # Si solo hay 1 dato, la varianza muestral (ddof=1) es indefinida
    if len(s) >= 2:
        varianza_muestral = s.var(ddof=1)
    else:
        varianza_muestral = np.nan

    varianza_poblacional = s.var(ddof=0)

    minimo = s.min()
    maximo = s.max()
    n = int(s.count())
    rango = maximo - minimo

    # Límites teóricos (fences) para atípicos
    limite_inferior = q1 - 1.5 * ric
    limite_superior = q3 + 1.5 * ric

    # Filtrado de atípicos
    mask_sin_atipicos = (s >= limite_inferior) & (s <= limite_superior)
    s_sin_atipicos = s[mask_sin_atipicos].copy().reset_index(drop=True)
    s_atipicos = s[~mask_sin_atipicos].copy().reset_index(drop=True)

    # Bigotes reales = extremos observados dentro de los límites teóricos
    if len(s_sin_atipicos) > 0:
        bigote_inferior_real = s_sin_atipicos.min()
        bigote_superior_real = s_sin_atipicos.max()
    else:
        bigote_inferior_real = np.nan
        bigote_superior_real = np.nan

    resultados = {
        "n": n,
        "minimo": minimo,
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
        "Q4": q4,
        "maximo": maximo,
        "rango": rango,
        "RIC": ric,
        "media": media,
        "mediana": mediana,
        "varianza_muestral": varianza_muestral,
        "varianza_poblacional": varianza_poblacional,
        "limite_inferior_atipicos": limite_inferior,
        "limite_superior_atipicos": limite_superior,
        "bigote_inferior_real": bigote_inferior_real,
        "bigote_superior_real": bigote_superior_real,
        "num_atipicos": int((~mask_sin_atipicos).sum()),
        "num_sin_atipicos": int(mask_sin_atipicos.sum()),
    }

    return resultados, s, s_sin_atipicos, s_atipicos


# ============================================================
# 4) REGLA DE STURGES
# ============================================================
def calcular_sturges(serie):
    """
    Calcula el número de intervalos k usando la regla de Sturges:
        k = 1 + 3.322 * log10(n)
    y la amplitud aproximada:
        A = (max - min) / k
    """
    s = pd.Series(serie, dtype="float64").dropna()

    n = len(s)
    if n == 0:
        return {
            "n": 0,
            "k_sturges_real": np.nan,
            "k_sturges": 0,
            "minimo": np.nan,
            "maximo": np.nan,
            "rango": np.nan,
            "amplitud_aprox": np.nan
        }

    minimo = s.min()
    maximo = s.max()
    rango = maximo - minimo

    if n == 1:
        k_real = 1.0
        k = 1
    else:
        k_real = 1 + 3.322 * np.log10(n)
        k = int(np.ceil(k_real))

    amplitud = (rango / k) if k > 0 else np.nan

    return {
        "n": int(n),
        "k_sturges_real": float(k_real),
        "k_sturges": int(k),
        "minimo": float(minimo),
        "maximo": float(maximo),
        "rango": float(rango),
        "amplitud_aprox": float(amplitud)
    }


# ============================================================
# 5) TABLA DE FRECUENCIAS (NO AGRUPADA)
# ============================================================
def tabla_frecuencias_no_agrupada(serie):
    """
    Tabla de frecuencias para datos discretos o repetidos:
    - valor
    - fi (frecuencia absoluta)
    - hi (frecuencia relativa)
    - porcentaje
    - Fi (frecuencia acumulada)
    - porcentaje_acumulado
    """
    s = pd.Series(serie).dropna()

    if len(s) == 0:
        return pd.DataFrame(columns=[
            "valor", "fi", "hi", "porcentaje", "Fi", "porcentaje_acumulado"
        ])

    freq_abs = s.value_counts().sort_index()

    df_freq = pd.DataFrame({
        "valor": freq_abs.index,
        "fi": freq_abs.values
    })

    total = df_freq["fi"].sum()
    df_freq["hi"] = df_freq["fi"] / total
    df_freq["porcentaje"] = df_freq["hi"] * 100
    df_freq["Fi"] = df_freq["fi"].cumsum()
    df_freq["porcentaje_acumulado"] = df_freq["porcentaje"].cumsum()

    return df_freq


# ============================================================
# 6) TABLA DE FRECUENCIAS AGRUPADA (STURGES)
# ============================================================
def tabla_frecuencias_agrupada_sturges(serie):
    """
    Crea una tabla de frecuencias agrupada por intervalos usando Sturges.
    """
    s = pd.Series(serie, dtype="float64").dropna()

    info_sturges = calcular_sturges(s)

    if len(s) == 0:
        columnas = ["intervalo", "fi", "hi", "porcentaje", "Fi", "porcentaje_acumulado"]
        return pd.DataFrame(columns=columnas), info_sturges

    k = info_sturges["k_sturges"]

    # Caso especial si todos los valores son iguales (rango=0)
    if s.min() == s.max():
        df_freq_int = pd.DataFrame({
            "intervalo": [f"[{s.min():.4f}, {s.max():.4f}]"],
            "fi": [len(s)]
        })
    else:
        categorias = pd.cut(s, bins=k, include_lowest=True, duplicates="drop")
        freq_abs = categorias.value_counts().sort_index()

        df_freq_int = pd.DataFrame({
            "intervalo": freq_abs.index.astype(str),
            "fi": freq_abs.values
        })

    total = df_freq_int["fi"].sum()
    df_freq_int["hi"] = df_freq_int["fi"] / total
    df_freq_int["porcentaje"] = df_freq_int["hi"] * 100
    df_freq_int["Fi"] = df_freq_int["fi"].cumsum()
    df_freq_int["porcentaje_acumulado"] = df_freq_int["porcentaje"].cumsum()

    return df_freq_int, info_sturges


# ============================================================
# 7) FUNCIONES DE GRÁFICAS
# ============================================================
def graficar_histograma(serie, titulo, nombre_archivo, bins="auto"):
    """
    Grafica histograma.
    bins puede ser:
      - "auto"
      - "sturges"
      - un entero (por ejemplo 6)
    """
    s = pd.Series(serie, dtype="float64").dropna()

    if len(s) == 0:
        print(f"⚠️ No se pudo graficar '{titulo}' porque no hay datos.")
        return

    bins_usar = bins
    if bins == "sturges":
        info = calcular_sturges(s)
        bins_usar = max(1, info["k_sturges"])

    plt.figure(figsize=(8, 5))
    plt.hist(s, bins=bins_usar, edgecolor="black")
    plt.title(titulo)
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(nombre_archivo, dpi=150)
    plt.close()
    print(f"📊 Histograma guardado: {nombre_archivo}")


def graficar_boxplot(serie, titulo, nombre_archivo, mostrar_fliers=True):
    """
    Grafica boxplot (diagrama de caja y bigotes).
    mostrar_fliers=True  -> muestra puntos atípicos
    mostrar_fliers=False -> oculta puntos atípicos en la gráfica
    """
    s = pd.Series(serie, dtype="float64").dropna()

    if len(s) == 0:
        print(f"⚠️ No se pudo graficar '{titulo}' porque no hay datos.")
        return

    plt.figure(figsize=(8, 4))
    plt.boxplot(s, vert=False, showfliers=mostrar_fliers)
    plt.title(titulo)
    plt.xlabel("Valor")
    plt.tight_layout()
    plt.savefig(nombre_archivo, dpi=150)
    plt.close()
    print(f"📦 Boxplot guardado: {nombre_archivo}")


# ============================================================
# 8) GUARDAR RESULTADOS
# ============================================================
def guardar_dict_como_csv(diccionario, ruta_csv):
    """
    Guarda un diccionario de resultados en una sola fila CSV.
    """
    df = pd.DataFrame([diccionario])
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"✅ Archivo guardado: {ruta_csv}")
    return df


def imprimir_bonito_estadisticos(resultados):
    """
    Imprime resultados de forma amigable.
    """
    print("\n" + "=" * 70)
    print("ESTADÍSTICOS DESCRIPTIVOS Y DETECCIÓN DE ATÍPICOS")
    print("=" * 70)

    orden = [
        "n", "minimo", "Q1", "Q2", "Q3", "Q4", "maximo",
        "rango", "RIC", "media", "mediana",
        "varianza_muestral", "varianza_poblacional",
        "limite_inferior_atipicos", "limite_superior_atipicos",
        "bigote_inferior_real", "bigote_superior_real",
        "num_sin_atipicos", "num_atipicos"
    ]

    for k in orden:
        v = resultados.get(k, None)
        if isinstance(v, (int, np.integer)):
            print(f"{k:30s}: {v}")
        elif isinstance(v, float) or isinstance(v, np.floating):
            if np.isnan(v):
                print(f"{k:30s}: NaN")
            else:
                print(f"{k:30s}: {v:.6f}")
        else:
            print(f"{k:30s}: {v}")


def imprimir_bonito_sturges(info_sturges):
    """
    Imprime datos de la regla de Sturges.
    """
    print("\n" + "=" * 70)
    print("REGLA DE STURGES (INTERVALOS PARA HISTOGRAMA)")
    print("=" * 70)
    print(f"{'n':30s}: {info_sturges['n']}")
    if not np.isnan(info_sturges["k_sturges_real"]):
        print(f"{'k_sturges_real':30s}: {info_sturges['k_sturges_real']:.6f}")
    else:
        print(f"{'k_sturges_real':30s}: NaN")
    print(f"{'k_sturges':30s}: {info_sturges['k_sturges']}")
    print(f"{'minimo':30s}: {info_sturges['minimo']:.6f}" if not np.isnan(info_sturges["minimo"]) else f"{'minimo':30s}: NaN")
    print(f"{'maximo':30s}: {info_sturges['maximo']:.6f}" if not np.isnan(info_sturges["maximo"]) else f"{'maximo':30s}: NaN")
    print(f"{'rango':30s}: {info_sturges['rango']:.6f}" if not np.isnan(info_sturges["rango"]) else f"{'rango':30s}: NaN")
    print(f"{'amplitud_aprox':30s}: {info_sturges['amplitud_aprox']:.6f}" if not np.isnan(info_sturges["amplitud_aprox"]) else f"{'amplitud_aprox':30s}: NaN")


# ============================================================
# 9) FUNCIÓN PRINCIPAL DE ANÁLISIS
# ============================================================
def analizar_csv_estadistico(ruta_csv, columna=None, carpeta_salida="salida_proyecto"):
    """
    Ejecuta todo el flujo:
    - Lee CSV
    - Calcula estadísticos
    - Detecta atípicos
    - Tabla de frecuencias no agrupada
    - Tabla de frecuencias agrupada con Sturges
    - Genera histogramas y boxplots con/sin atípicos
    - Guarda resultados en archivos
    """
    os.makedirs(carpeta_salida, exist_ok=True)

    # 1) Lectura
    df_original, serie, nombre_columna = leer_columna_numerica_desde_csv(ruta_csv, columna=columna)

    print("\n" + "=" * 70)
    print("DATAFRAME ORIGINAL (primeras 10 filas)")
    print("=" * 70)
    print(df_original.head(10))

    print(f"\n✅ Columna usada para análisis: '{nombre_columna}'")
    print(f"✅ Total de datos numéricos válidos: {len(serie)}")

    # 2) Estadísticos + atípicos + bigotes
    resultados, s_ordenada, s_sin_atipicos, s_atipicos = calcular_estadisticos(serie)
    imprimir_bonito_estadisticos(resultados)

    # 3) Sturges
    info_sturges = calcular_sturges(s_ordenada)
    imprimir_bonito_sturges(info_sturges)

    # 4) Tablas de frecuencias
    df_freq_no_agrupada = tabla_frecuencias_no_agrupada(s_ordenada)
    print("\n" + "=" * 70)
    print("TABLA DE FRECUENCIAS (NO AGRUPADA)")
    print("=" * 70)
    print(df_freq_no_agrupada)

    df_freq_agrupada_sturges, _ = tabla_frecuencias_agrupada_sturges(s_ordenada)
    print("\n" + "=" * 70)
    print("TABLA DE FRECUENCIAS AGRUPADA (STURGES)")
    print("=" * 70)
    print(df_freq_agrupada_sturges)

    # 5) Guardar CSV de resultados
    ruta_estadisticos = os.path.join(carpeta_salida, "estadisticos_resumen.csv")
    ruta_sturges = os.path.join(carpeta_salida, "sturges_resumen.csv")
    ruta_freq_no_agrupada = os.path.join(carpeta_salida, "tabla_frecuencias_no_agrupada.csv")
    ruta_freq_agrupada = os.path.join(carpeta_salida, "tabla_frecuencias_agrupada_sturges.csv")
    ruta_datos_ordenados = os.path.join(carpeta_salida, "datos_ordenados.csv")
    ruta_datos_sin_atipicos = os.path.join(carpeta_salida, "datos_sin_atipicos.csv")
    ruta_datos_atipicos = os.path.join(carpeta_salida, "datos_atipicos.csv")

    df_estadisticos = guardar_dict_como_csv(resultados, ruta_estadisticos)
    df_sturges = guardar_dict_como_csv(info_sturges, ruta_sturges)

    df_freq_no_agrupada.to_csv(ruta_freq_no_agrupada, index=False, encoding="utf-8")
    print(f"✅ Archivo guardado: {ruta_freq_no_agrupada}")

    df_freq_agrupada_sturges.to_csv(ruta_freq_agrupada, index=False, encoding="utf-8")
    print(f"✅ Archivo guardado: {ruta_freq_agrupada}")

    pd.DataFrame({nombre_columna: s_ordenada}).to_csv(ruta_datos_ordenados, index=False, encoding="utf-8")
    print(f"✅ Archivo guardado: {ruta_datos_ordenados}")

    pd.DataFrame({nombre_columna: s_sin_atipicos}).to_csv(ruta_datos_sin_atipicos, index=False, encoding="utf-8")
    print(f"✅ Archivo guardado: {ruta_datos_sin_atipicos}")

    pd.DataFrame({nombre_columna: s_atipicos}).to_csv(ruta_datos_atipicos, index=False, encoding="utf-8")
    print(f"✅ Archivo guardado: {ruta_datos_atipicos}")

    # 6) Gráficas con atípicos
    graficar_histograma(
        s_ordenada,
        titulo=f"Histograma con atípicos (bins=auto) - {nombre_columna}",
        nombre_archivo=os.path.join(carpeta_salida, "histograma_con_atipicos_auto.png"),
        bins="auto"
    )

    graficar_histograma(
        s_ordenada,
        titulo=f"Histograma con atípicos (Sturges) - {nombre_columna}",
        nombre_archivo=os.path.join(carpeta_salida, "histograma_con_atipicos_sturges.png"),
        bins="sturges"
    )

    graficar_boxplot(
        s_ordenada,
        titulo=f"Boxplot / Caja y bigotes CON atípicos - {nombre_columna}",
        nombre_archivo=os.path.join(carpeta_salida, "boxplot_con_atipicos.png"),
        mostrar_fliers=True
    )

    # 7) Gráficas sin atípicos (si hay datos)
    if len(s_sin_atipicos) > 0:
        graficar_histograma(
            s_sin_atipicos,
            titulo=f"Histograma sin atípicos (bins=auto) - {nombre_columna}",
            nombre_archivo=os.path.join(carpeta_salida, "histograma_sin_atipicos_auto.png"),
            bins="auto"
        )

        graficar_histograma(
            s_sin_atipicos,
            titulo=f"Histograma sin atípicos (Sturges) - {nombre_columna}",
            nombre_archivo=os.path.join(carpeta_salida, "histograma_sin_atipicos_sturges.png"),
            bins="sturges"
        )

        # Boxplot sin atípicos (ya quitamos atípicos del conjunto)
        graficar_boxplot(
            s_sin_atipicos,
            titulo=f"Boxplot / Caja y bigotes SIN atípicos - {nombre_columna}",
            nombre_archivo=os.path.join(carpeta_salida, "boxplot_sin_atipicos.png"),
            mostrar_fliers=False
        )
    else:
        print("⚠️ No hay datos sin atípicos para generar gráficas 'sin atípicos'.")

    # 8) Resumen de archivos generados
    print("\n" + "=" * 70)
    print("ARCHIVOS GENERADOS")
    print("=" * 70)
    for archivo in sorted(os.listdir(carpeta_salida)):
        print("-", os.path.join(carpeta_salida, archivo))

    # Retorno útil por si quieres usarlo en notebook
    return {
        "df_original": df_original,
        "nombre_columna_analizada": nombre_columna,
        "serie_ordenada": s_ordenada,
        "serie_sin_atipicos": s_sin_atipicos,
        "serie_atipicos": s_atipicos,
        "resultados_estadisticos": resultados,
        "info_sturges": info_sturges,
        "df_estadisticos": df_estadisticos,
        "df_sturges": df_sturges,
        "df_frecuencia_no_agrupada": df_freq_no_agrupada,
        "df_frecuencia_agrupada_sturges": df_freq_agrupada_sturges,
    }


# ============================================================
# 10) EJEMPLOS DE USO
# ============================================================
if __name__ == "__main__":
    # --------------------------------------------------------
    # OPCIÓN A: Generar CSV de ejemplo (20 edades entre 16 y 28)
    # --------------------------------------------------------
    generar_csv_ejemplo(
        nombre_csv="edades_20_alumnos.csv",
        n=20,
        minimo=16,
        maximo=28,
        semilla=10  # puedes cambiar semilla para otras edades
    )

    # --------------------------------------------------------
    # OPCIÓN B: Analizar el CSV de ejemplo
    # --------------------------------------------------------
    analizar_csv_estadistico(
        ruta_csv="edades_20_alumnos.csv",
        columna="edad",                  # si no sabes el nombre de la columna, usa None
        carpeta_salida="salida_proyecto"
    )

    # --------------------------------------------------------
    # OPCIÓN C: Cuando te den el CSV del profe
    # (descomenta y cambia el nombre del archivo)
    # --------------------------------------------------------
    # analizar_csv_estadistico(
    #     ruta_csv="archivo_del_profe.csv",
    #     columna=None,                 # o "nombre_columna" si lo conoces
    #     carpeta_salida="salida_proyecto_profe"
    # )