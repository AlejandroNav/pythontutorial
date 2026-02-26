import random
import matplotlib.pyplot as plt

T = [
    (0.03,  0.00, 0.00, 0.10, 0.0, 0.00, 0.02),
    (0.85,  0.00, 0.00, 0.85, 0.0, 1.50, 0.60),
    (0.80,  0.00, 0.00, 0.80, 0.0, 1.50, 0.10),
    (0.20, -0.08, 0.15, 0.22, 0.0, 0.85, 0.07),
    (-0.20, 0.08, 0.15, 0.22, 0.0, 0.85, 0.07),
    (0.25, -0.10, 0.12, 0.25, 0.0, 0.30, 0.07),
    (-0.20, 0.10, 0.12, 0.20, 0.0, 0.40, 0.07),
]

# CDF para elegir por probabilidad
cdf = []
s = 0.0
for *coef, p in T:
    s += p
    cdf.append(s)

def step(x, y):
    r = random.random()
    i = next(k for k, v in enumerate(cdf) if r <= v)
    a,b,c,d,e,f,_p = T[i]
    return a*x + b*y + e, c*x + d*y + f

N = 200_000
x, y = 0.0, 2.0
xs, ys = [], []

# burn-in
for _ in range(50):
    x, y = step(x, y)

for _ in range(N):
    x, y = step(x, y)
    xs.append(x); ys.append(y)

plt.figure(figsize=(4, 8))
plt.scatter(xs, ys, s=0.1, marker=".", linewidths=0)
plt.axis("off")
plt.show()
