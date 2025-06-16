import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# ---------- ALGORITMOS DE ORDENAMIENTO CON REGISTRO ---------- ###

def quicksort_classic_highlight(arr, frames, pivots, comparisons, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivots.append(high)
        comparisons.append(None)
        frames.append(arr.copy())

        p = partition_highlight(arr, frames, pivots, comparisons, low, high)
        quicksort_classic_highlight(arr, frames, pivots, comparisons, low, p - 1)
        quicksort_classic_highlight(arr, frames, pivots, comparisons, p + 1, high)


# EL quicksort clásico utiliza el último elemento como pivote
# El quicksort aleatorizado utiliza un pivote aleatorio
def quicksort_random_highlight(arr, frames, pivots, comparisons, low=0, high=None):
    if high is None: # si high es None, significa que es la primera llamada a la función
        high = len(arr) - 1 #  establece high al último índice del arreglo.
    if low < high: # si low es menor que high
        rand_index = random.randint(low, high) #  Aquí está la aleatorización:
        #se elige un índice aleatorio dentro del rango actual.

        arr[high], arr[rand_index] = arr[rand_index], arr[high] 
        #Y luego se intercambia el elemento en ese índice con el último elemento (pivote).

        # frames, pivots y comparisons son listas que guardan cada paso del algoritmo (para la animación).
        pivots.append(high)
        comparisons.append(None)
        frames.append(arr.copy())

        p = partition_highlight(arr, frames, pivots, comparisons, low, high)
        quicksort_random_highlight(arr, frames, pivots, comparisons, low, p - 1)
        quicksort_random_highlight(arr, frames, pivots, comparisons, p + 1, high)

def partition_highlight(arr, frames, pivots, comparisons, low, high):
    pivot = arr[high]
    i = low
    for j in range(low, high):
        comparisons.append(j)
        pivots.append(high)
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            frames.append(arr.copy())
            i += 1
        else:
            frames.append(arr.copy())
    arr[i], arr[high] = arr[high], arr[i]
    comparisons.append(i)
    pivots.append(high)
    frames.append(arr.copy())
    return i

# ---------- CONFIGURACIÓN Y ANIMACIÓN ----------

def preparar_animacion(arr, es_aleatorizado=False):
    arr_copy = arr.copy()
    frames, pivots, comparisons = [arr_copy.copy()], [None], [None]
    if es_aleatorizado:
        quicksort_random_highlight(arr_copy, frames, pivots, comparisons)
    else:
        quicksort_classic_highlight(arr_copy, frames, pivots, comparisons)
    return frames, pivots, comparisons

def crear_animacion_comparativa(frames_c, pivots_c, comps_c, frames_r, pivots_r, comps_r, n):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("QuickSort Clásico vs Aleatorizado\nRojo = Pivote, Amarillo = Comparación")

    bars1 = ax1.bar(range(n), frames_c[0], align="edge", color='lightblue')
    bars2 = ax2.bar(range(n), frames_r[0], align="edge", color='lightgreen')

    ax1.set_title("Clásico")
    ax2.set_title("Aleatorizado")

    for ax in (ax1, ax2):
        ax.set_xlim(0, n)
        ax.set_ylim(0, n + 1)
        ax.set_xticks([])
        ax.set_yticks([])

    max_frames = max(len(frames_c), len(frames_r))

    def update(frame):
        if frame < len(frames_c):
            for i, rect in enumerate(bars1):
                rect.set_height(frames_c[frame][i])
                rect.set_color('lightblue')
            pivot = pivots_c[frame]
            if pivot is not None:
                bars1[pivot].set_color('red')
            comp = comps_c[frame]
            if comp is not None and comp != pivot:
                bars1[comp].set_color('gold')

        if frame < len(frames_r):
            for i, rect in enumerate(bars2):
                rect.set_height(frames_r[frame][i])
                rect.set_color('lightgreen')
            pivot = pivots_r[frame]
            if pivot is not None:
                bars2[pivot].set_color('red')
            comp = comps_r[frame]
            if comp is not None and comp != pivot:
                bars2[comp].set_color('gold')

        return bars1 + bars2

    ani = animation.FuncAnimation(fig, update, frames=max_frames, interval=10, repeat=False)
    plt.tight_layout()
    plt.show()

# ---------- EJECUCIÓN PRINCIPAL ----------

if __name__ == "__main__":
    n = 40  # Número de elementos a ordenar

    # Opción 1: Lista en reversa (peor caso para QuickSort clásico)
    datosReversa = list(range(n, 0, -1))

    # Opción 2: Lista ordenada ascendente
    datosOrdenados = list(range(1, n + 1))

    # Opción 3: Lista aleatoria
    datosAleatorios = list(range(1, n + 1))
    random.shuffle(datosAleatorios)

    # ==> ESCOGE UNA DE ESTAS OPCIONES:
    datosEscogidos = datosReversa.copy()       # ← Prueba reversa EL PEOR CASO
    # datosEscogidos = datosOrdenados.copy()   # ← Prueba ordenada 
    # datosEscogidos = datosAleatorios.copy()  # ← Prueba aleatoria

    # Ejecutar animaciones con los mismos datos
    frames_clasico, pivots_clasico, comps_clasico = preparar_animacion(datosEscogidos, es_aleatorizado=False)
    frames_aleatorio, pivots_aleatorio, comps_aleatorio = preparar_animacion(datosEscogidos, es_aleatorizado=True)

    # Mostrar la animación comparativa
    crear_animacion_comparativa(frames_clasico, pivots_clasico, comps_clasico,
                                 frames_aleatorio, pivots_aleatorio, comps_aleatorio, n)