import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Height ratios
h0 = np.array([22.43, 38.15, 33.16, 3.46, 6.05])
h1 = np.array([44.31, 18.3, 44.98, 32.5])
h2 = np.array([44.81, 54.55, 43.27, 44.88])
h3 = np.array([60.27, 39.53, 60.32, 58.23, 60.68, 109.46, 74.77, 51.64, 62.94, 67.57, 76.66])

height_dists = [h0, h1, h2, h3]
'''
print("-------------------------------------")
print("Height")
for dist in height_dists:
    print("Q1", np.quantile(dist, 0.25))
    print("Median", np.quantile(dist, 0.5))
    print("Q3", np.quantile(dist, 0.75))
    print()
print("-------------------------------------")
'''
#fig1 = sns.violinplot(data=height_dists)
#fig1.set(xlabel="Height score", ylabel="Percent decrease in body height")


# Acceleration
s0 = np.array([-50.22, -57.5, -114.75, -190.82 -52.94, -103.78, -6.24])
s1 = np.array([-135.98, -47.70, -59.313, 3.43, -113.84, -4.69, 14.45])
s2 = np.array([-48.44, -66.64, 7.96, -2.97])
s3 = np.array([-52.7, -45.08, -58.20, 52.99, 4.97, -21.62])

speed_dists = [s0, s1, s2, s3]
'''
print("-------------------------------------")
print("Acceleration")
print(len(speed_dists))
for dist in speed_dists:
    print("Q1", np.quantile(dist, 0.25))
    print("Median", np.quantile(dist, 0.5))
    print("Q3", np.quantile(dist, 0.75))
    print()
print("-------------------------------------")
'''
#fig2 = sns.violinplot(data=speed_dists, cut=1)
#fig2.set(xlabel="Acceleration score", ylabel="Percent change in velocity")


# Arm angles [-pi/2, pi/2]
a0 = np.array([-0.09, -0.63, 0.96, -0.67, -0.86])
a1 = np.array([-1.42, 0.04, -1.43, -0.23, -0.61])
a2 = np.array([-0.38, -0.35, -0.12, 0.48,])
a3 = np.array([-0.29, -0.83, -0.73, 0.35, -0.80, 0.75, -0.08, -0.03, 0.33, 0.54])

arm_dists = [a0, a1, a2, a3]
'''
print("-------------------------------------")
print("Arm Extension")
for dist in arm_dists:
    print("Q1", np.quantile(dist, 0.25))
    print("Median", np.quantile(dist, 0.5))
    print("Q3", np.quantile(dist, 0.75))
    print()
print("-------------------------------------")
'''

#fig3 = sns.violinplot(data=arm_dists, cut=0)
#fig3.set(xlabel="Arm extension score", ylabel="Angle of arm extension (radians)")
#plt.show()