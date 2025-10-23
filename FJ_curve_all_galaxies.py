# Main file for Computational assignment 2 PHYS 3116

# Lets the script interact with computer's files and folder
import os

# Setup for numpy as well as path
import pandas as pd
import numpy as np

# import plots
import matplotlib.pyplot as plt

# Location of main.py, ensures that the code can always find files relative to the script's location
base_path = os.path.dirname(__file__)

# Combines paths, so Data_Repo can be referred to from different devices
data_path = os.path.join(base_path, "Data_Repo")

# Retrieves each file from Data_Repo # Fixed Data_Repo to data_path to make sure that Python always looks in the Data_Repo folder next to the main.py, no matter where the script is run from
cat = pd.read_csv(os.path.join(data_path, "InputCatGAMADR3.csv"))
clusters = pd.read_csv(os.path.join(data_path, "samiDR3InputCatClusters.csv"))
kinematics = pd.read_csv(os.path.join(data_path, "samiDR3StelKin.csv"))
morph = pd.read_csv(os.path.join(data_path, "samiDR3VisualMorphology.csv"))

"""description: 

cat -- galaxy global properties, Contains (catid, [radius, declination] coord, r-band magnitudes, log_mass, color(g-i), ellip, pa, survey and quality?)
morph -- galaxy morphology, Contains (catid, type [0 ~ ellipitcal, 1 ~ lenticular, 2+ ~ spirals], early/late types)
cluster -- galaxy clusters, Contains (catid, cluster ID, membership flags etc)
kinematics -- galaxy kinematics properties, Contains (catid, velcity dispersion, velocity uncertainry, position)

"""
# Dropping duplicated data is required to run the 'validate' parameter
clusters = clusters.drop_duplicates(subset='catid')
kinematics = kinematics.drop_duplicates(subset='catid')
morph = morph.drop_duplicates(subset='catid')

# merges the files into a singular table named merged_galaxy
# TODO add and fix merge 
# Fixed from 'one to one' to 'many_to_one', and the suffixes are fixed, as Pandas requires one suffix for the left and right tables
merged_galaxy = (
    cat.merge(kinematics, on = 'catid', how = 'inner', validate = 'many_to_one', suffixes=('_cat','_kin'))
        .merge(clusters, on = 'catid', how = 'left', validate = 'many_to_one', suffixes=('_kin','_clust'))
        .merge(morph, on = 'catid', how = 'left', validate = 'many_to_one', suffixes=('_clust','_morph'))
)

data = merged_galaxy[['m_r_kin', 'sigma_re', 'z_spec_kin']]

print(data)

df_3 = data[data["sigma_re"] > 0].copy()

c = 299792.45                    # km/s
H0 = 70.0                        # km/s/Mpc
z = df_3["z_spec_kin"].astype(float).values
d = (c/H0) * z                   # finds distance
DM = 5 * np.log10(d * 1e6) - 5   # finds the distance modulus

m_r = df_3["m_r_kin"].astype(float).values   # apparent magnitude
M_r = m_r - DM                               # absolute magnitude

# L = 10 ^ (-0.4 * magnitude - Sun magnitude)
L_0 = 3.84 * 10 ** 26

M_0 = 4.83
L = L_0 * 10 ** (-0.4*(M_r - M_0))           # L0 * 10 ^ (-0.4 * (absolute magnitude - Sun))


# plotting the axis data correctly
y_pts = np.log10(L)
x_pts = np.log10(df_3["sigma_re"])

# removal of further NaNs and infinity numbers which came through
mask = np.isfinite(x_pts) & np.isfinite(y_pts)
x_pts = x_pts[mask]
y_pts = y_pts[mask]

# scatter plot of the final function
plt.figure(figsize=(8,6))
plt.scatter(x_pts, y_pts, s=32, color="royalblue", marker="*")

# labels/titles
plt.ylabel(r'$\log_{10},Luminosity\, (L_{sun})$')
plt.xlabel(r'$\log_{10},\sigma_{{re}}\, (km/s)$')
plt.title('Faber–Jackson plot of SAMI early-type galaxies')
plt.legend()

## display graph 
plt.show()
