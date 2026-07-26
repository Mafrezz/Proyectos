import numpy as np
import matplotlib.pyplot as plt
x = np.arange(0, 2 * np.pi, 0.01)
y = np.sin(x)
plt.plot(x, y)
plt.title("Gráfica de y = sin(x)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()