import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 10, 2)
plt.plot(x, x**2)


for i in range(5):
    plt.plot(i, i**2, c="red", marker="o")

plt.show()

