import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Height ratios
h0 = np.array([22.43, 38.15, 33.16, 3.46, 6.05])
h1 = np.array([44.31, 18.3, 44.98, 32.5])
h2 = np.array([44.81, 54.55, 43.27, 44.88])
h3 = np.array([60.27, 39.53, 60.32, 58.23, 60.68, 109.46, 74.77, 51.64, 62.94, 67.57, 76.66])

height_dists = [h0, h1, h2, h3]

for dist in height_dists:
    print("Q1", np.quantile(dist, 0.25))
    print("Q3", np.quantile(dist, 0.75))
    print()


scores = [0, 1, 2, 3]
fig1 = sns.violinplot(data=height_dists)
fig1.set(xlabel="Height score", ylabel="Percent decrease in body height")
#plt.show()






# Speed

# FLAG 13_003, 15_113, 21_000
# Arm extension ratios
a0 = [0.31, -1.0, 0.03]
a1 = [0.29, -0.09, 0.16, -0.01, 0.13, 0.34]
a2 = [0.61, 0.99, 0.38, 0.45, 0.76, 0.54]
a3 = [0.28, 0.66, 0.67, 0.09, -0.22, 0.13, -0.08, -0.01, 0.7]