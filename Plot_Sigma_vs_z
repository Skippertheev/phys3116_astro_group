import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

base_path = os.path.dirname(__file__)

data_path = os.path.join(base_path, "Data_Repo")

cat = pd.read_csv(os.path.join(data_path, "InputCatGAMADR3.csv"))
clusters = pd.read_csv(os.path.join(data_path, "samiDR3InputCatClusters.csv"))
kinematics = pd.read_csv(os.path.join(data_path, "samiDR3StelKin.csv"))
morph = pd.read_csv(os.path.join(data_path, "samiDR3VisualMorphology.csv"))

clusters = clusters.drop_duplicates(subset='catid')
kinematics = kinematics.drop_duplicates(subset='catid')
morph = morph.drop_duplicates(subset='catid')

merged_galaxy = (
    cat.merge(kinematics, on = 'catid', how = 'inner', validate = 'many_to_one', suffixes=('_cat','_kin'))
        .merge(clusters, on = 'catid', how = 'left', validate = 'many_to_one', suffixes=('_kin','_clust'))
        .merge(morph, on = 'catid', how = 'left', validate = 'many_to_one', suffixes=('_clust','_morph'))
)

print("\nTable summary:")
print(merged_galaxy.info())

df = pd.DataFrame(merged_galaxy)
arr_mg = np.array(merged_galaxy)
arr1 = arr_mg[:,8]

size = np.size(arr1)

print(size)

print(arr1)

col_needed = ["sigma_re", "m_r_kin", "z_spec_kin", "ellip_kin"]
df_3 = df.dropna(subset=col_needed)

df_3 = df_3.dropna(subset=col_needed)

c = 299792.45
H0 = 70.0
z = df_3["z_spec_kin"].astype(float).values
d = (c/H0) * z 

# plotting the axis data correctly
y_pts = df_3["sigma_re"]
x_pts = z

# removal of further NaNs and infinity numbers which came through
mask = np.isfinite(x_pts) & np.isfinite(y_pts)
x_pts = x_pts[mask]
y_pts = y_pts[mask]

plt.figure(figsize=(8,6))
plt.scatter(x_pts, y_pts, s=32, color="royalblue", marker="*")
plt.title("How Dispersion Changes with Respect to a Galaxies Distance from the Milky Way")
plt.xlabel("Redshift")
plt.ylabel("Velocity Dispersion / km/s")

## polyfit to find out actual slope
x_plane = np.linspace(x_pts.min(), x_pts.max(), 100)
b_bit, a_bit = np.polyfit(x_pts, y_pts, 1)   # y = a + bx
y_fit = a_bit + b_bit * x_plane
plt.plot(x_plane, y_fit, color="purple", label="line of best fit; slope = " + str(b_bit) + ")")

correlation_matrix = np.corrcoef(x_pts, y_pts)
correlation_coefficient = correlation_matrix[0, 1]

print(f"Correlation coefficient (NumPy): {correlation_coefficient}")
print("Gradient", b_bit)

plt.legend()
plt.show()

num_points = len(df)
print(f"Number of points plotted: {num_points}")
