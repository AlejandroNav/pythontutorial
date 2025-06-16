import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Función de QuickSort con registro de frames, pivotes y comparaciones
def quicksort_with_highlight(arr, frames, pivots, comparisons, low=0, high=None, randomized=False):
    if high is None:
        high = len(arr) - 1
    if low < high:
        if randomized:
            rand_index = random.randint(low, high)
            arr[high], arr[rand_index] = arr[rand_index], arr[high]
        pivots.append(high)
        comparisons.append(None)
        frames.append(arr.copy())

        p = partition_highlight(arr, frames, pivots, comparisons, low, high)
        quicksort_with_highlight(arr, frames, pivots, comparisons, low, p - 1, randomized)
        quicksort_with_highlight(arr, frames, pivots, comparisons, p + 1, high, randomized)

# Particionado que guarda comparaciones y pivotes
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

# Número de elementos (puedes cambiarlo)
n = 60

# Lista aleatoria
original = list(range(1, n + 1))
random.shuffle(original)

# Preparar arreglos para ambos métodos
arr_classic = original.copy()
arr_random = original.copy()

# Almacenar estados
frames_c, pivots_c, comps_c = [arr_classic.copy()], [None], [None]
frames_r, pivots_r, comps_r = [arr_random.copy()], [None], [None]

# Ejecutar ambos algoritmos
quicksort_with_highlight(arr_classic, frames_c, pivots_c, comps_c, randomized=False)
quicksort_with_highlight(arr_random, frames_r, pivots_r, comps_r, randomized=True)

# Crear visualización
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("QuickSort Clásico vs Aleatorizado\nRojo = Pivote, Amarillo = Comparación (Lista Aleatoria)")

bars1 = ax1.bar(range(n), frames_c[0], align="edge", color='lightblue')
bars2 = ax2.bar(range(n), frames_r[0], align="edge", color='lightgreen')

ax1.set_title("Clásico")
ax2.set_title("Aleatorizado")

for ax in (ax1, ax2):
    ax.set_xlim(0, n)
    ax.set_ylim(0, n + 1)
    ax.set_xticks([])
    ax.set_yticks([])

# Determinar número máximo de frames
max_frames = max(len(frames_c), len(frames_r))

# Función de actualización de animación
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

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=max_frames, interval=10, repeat=False)
plt.tight_layout()
plt.show()
