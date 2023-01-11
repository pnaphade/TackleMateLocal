import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Height ratios
h0 = np.array([22.43, 38.15, 33.16, 3.46, 6.05])
h1 = np.array([44.31, 18.3, 44.98, 32.5])
h2 = np.array([44.81, 54.55, 43.27, 44.88])
h3 = np.array([60.27, 39.53, 60.32, 58.23, 60.68, 109.46, 74.77, 51.64, 62.94, 67.57, 76.66])

height_dists = [h0, h1, h2, h3]

print("-------------------------------------")
print("Height distribution quartiles")
for dist in height_dists:
    print("Q1", np.quantile(dist, 0.25))
    print("Q3", np.quantile(dist, 0.75))
    print()
print("-------------------------------------")


#fig1 = sns.violinplot(data=height_dists)
#fig1.set(xlabel="Height score", ylabel="Percent decrease in body height")


# Speed
print("-------------------------------------")
print("Acceleration Distribution Quartiles")
s0 = np.array([-50.22, -57.5, -114.75, -190.82 -52.94, -103.78, -6.24])
s1 = np.array([-135.98, -47.70, -59.313, 3.43, -113.84, -4.69, 14.45])
s2 = np.array([-48.44, -66.64, 7.96, -2.97])
s3 = np.array([-52.7, -45.08, -58.20, 52.99, 4.97, -21.62])
print("-------------------------------------")


speed_dists = [s0, s1, s2, s3]
print(len(speed_dists))
for dist in speed_dists:
    print("Q1", np.quantile(dist, 0.25))
    print("Q3", np.quantile(dist, 0.75))
    print()

#fig2 = sns.violinplot(data=speed_dists)
#fig2.set(xlabel="Acceleration score", ylabel="Percent change in velocity")
#plt.show()


# FLAG 13_003, 15_113, 21_000
# Arm extension ratios
a0 = [0.31, -1.0, 0.03]
a1 = [0.29, -0.09, 0.16, -0.01, 0.13, 0.34]
a2 = [0.61, 0.99, 0.38, 0.45, 0.76, 0.54]
a3 = [0.28, 0.66, 0.67, 0.09, -0.22, 0.13, -0.08, -0.01, 0.7]