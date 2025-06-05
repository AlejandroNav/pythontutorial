import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Parámetros del proceso
n = 1_000          # piezas inspeccionadas
p = 0.008          # 0.8 % probabilidad de que una pieza sea defectuosa

# Soporte y PMF
x = np.arange(0, n + 1)
pmf = binom.pmf(x, n, p)

# Recortar para la gráfica (0–25 defectos capturan casi toda la masa)
x_plot = x[:26]
pmf_plot = pmf[:26]

plt.bar(x_plot, pmf_plot, color='steelblue')
plt.title('Número de piezas defectuosas en un lote de 1 000 (p = 0.8 %)')
plt.xlabel('Defectos en el lote')
plt.ylabel('Probabilidad')
plt.xticks(x_plot)          # muestra cada entero
plt.tight_layout()
plt.show()

# Métricas útiles
media = n * p
desv = np.sqrt(n * p * (1 - p))
print(f"Valor esperado (media): {media:.2f} defectos")
print(f"Desviación estándar  : {desv:.2f}")
