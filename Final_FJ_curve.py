# Main file for Computational assignment 2 PHYS 3116
## =====================================================================================================
# 1. IMPORT FILES AND LIBRARIES
## =====================================================================================================
# Lets the script interact with computer's files and folder
import os

# Setup for numpy as well as path
import pandas as pd
import numpy as np

# import plots
import matplotlib.pyplot as plt                                                                                                     #bookmark_1
## =====================================================================================================
# 2. LOAD AND PREPARE DATA FILES
## =====================================================================================================
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
## =====================================================================================================
# 3. DATA CLEANING AND MERGING
## =====================================================================================================
# Dropping duplicated data is required to run the 'validate' parameter                                                              
clusters = clusters.drop_duplicates(subset='catid')
kinematics = kinematics.drop_duplicates(subset='catid')
morph = morph.drop_duplicates(subset='catid')

# merges the files into a singular table named merged_galaxy
# TODO add and fix merge 
# Fixed from 'one to one' to 'many_to_one', and the suffixes are fixed, as Pandas requires one suffix for the left and right tables                 #bookmark_2
merged_galaxy = (
    cat.merge(kinematics, on = 'catid', how = 'inner', validate = 'many_to_one', suffixes=('_cat','_kin'))
        .merge(clusters, on = 'catid', how = 'left', validate = 'many_to_one', suffixes=('_kin','_clust'))
        .merge(morph, on = 'catid', how = 'left', validate = 'many_to_one', suffixes=('_clust','_morph'))
)

# Visualise merged table (standard analysis tables for large data)
# Print first 10 rows
print("\nFirst 10 rows of merged_galaxy:")
print(merged_galaxy.head(10))

# Print random 10 rows
print("\nRandom 10 rows of merged_galaxy:")
print(merged_galaxy.sample(10))

# Print table summary
print("\nTable summary:")
print(merged_galaxy.info())

# Basic statistics of numeric columns
print("\nNumeric summary:")
print(merged_galaxy.describe())


# The Faber-Jackson (FJ) curve shows the relationship between the magnitudes of galaxies and their velocity dispersions.
# Want to make sure that merged data will properly give results. Test with magnitude data

## =====================================================================================================
# 4. PRELIM CHECKS AND DATA INSPECTION
## =====================================================================================================
df = pd.DataFrame(merged_galaxy)
arr_mg = np.array(merged_galaxy)
arr1 = arr_mg[:,8]

size = np.size(arr1)

print(size)

print(arr1)

# To get a proper looking FJ curve, one of the key factors is ellipticity, the more elliptical,
# the better. As such the morphological data cannot yeild anything that indicates a galaxy is irregular,
# spiral, or bar spiral.

# The visual morphology data will tell which galaxies are elliptical. Any galaxy whose type is 0, will be elliptical
# and it is these galaxies that will best fit the FJ curve.

type0 = df[df['type'] == 0]

print(type0)

# Now that all of the 2100-odd rows of data has been reduced to 154 eliptical galaxies, we need to consider which
# galaxies are most elliptical. After some discussion it was decided that galaxies with an ellipticity between 2
# and 8 would not be too round or too flat. Thus, we will sort through these reduced galaxies again.

df2 = df.set_index('catid')
df2

reduced_1 = df2.filter(items = ['catid', 'type', 'ellip_kin'])

print(reduced_1)
## =====================================================================================================
# 5. DATA FILTERING FOR FJ RELATION
## =====================================================================================================
# preparation and filtering of the data     
df = merged_galaxy.copy()
df = df[df["type"] == 0].copy()

# only required columns are needed
col_needed = ["sigma_re", "m_r_kin", "z_spec_kin", "ellip_kin"]
df_3 = df.dropna(subset=col_needed)

# we drop eveyrthing except for out required column
df_3 = df_3.dropna(subset=col_needed)

# physical mask -- a compilation of all masked parameters.
df_3 = df_3[   
   (df_3["sigma_re"] > 30) & (df_3["sigma_re"] < 400) &    # velocity dispersion  - SDSS III velocity dispersion measurements
   (df_3["z_spec_kin"] > 0.004) & (df_3["z_spec_kin"] < 0.113) &    # redshift levels by (Scott et al. 2018) SAMI Galaxy Survey: Data Release Two   #bookmark_3
   (df_3["ellip_kin"] > 0.2) & (df_3["ellip_kin"] < 0.8)   # the ellipticity  - we add one dp each way following the 0.3 - 0.7 param used by Rawlings et al. (2020), Rules of behaviour for spin–ellipticity radial tracks in galaxies
].copy()

# these masks values are given by the The SAMI Galaxy Survey: Data Release Two (DR2)

# make a copy to only check for positive values to apply Luminosity rule.
df_3 = df_3[df_3["sigma_re"] > 0].copy()

## =====================================================================================================
# 6. COMPUTATION OF LUMINOSITY AND EQUATIONS
## =====================================================================================================
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

# [Data_Repo/Computational lab.jpeg]

## =====================================================================================================
# 7. FJ SCATTER PLOT AND LINE OF BEST FIT
## =====================================================================================================
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

# line of best fit L ∝ σ⁴
# the equation we have here is log (L) = 4 * log (sigma_re) + C, where C is some constant intercept which are unknown
# we first create a list of 100 evenly spaced points along the range of df_3["sigma_re"] / the x intercept
# we then find C - by taking the average value of C = log(L) - 4 * log (sigma_re) over all galaxies
x_grid = np.linspace(x_pts.min(), x_pts.max(), 100)
Constant = np.mean(y_pts - 4 * x_pts)
plot= 4 * x_grid + Constant
plt.plot(x_grid, plot, color="crimson", label="Expected L ∝ σ^4 " +  str("slope = 4"))

## polyfit to find out actual slope
x_plane = np.linspace(x_pts.min(), x_pts.max(), 100)
b_bit, a_bit = np.polyfit(x_pts, y_pts, 1)   # y = a + bx
y_fit = a_bit + b_bit * x_plane
plt.plot(x_plane, y_fit, color="purple", label="line of best fit; slope = " + str(b_bit) + ")")

# displays our slope
print("This is our actual slope", b_bit)

# labels/titles
plt.ylabel(r'$\log_{10},Luminosity\, (L_{sun})$')
plt.xlabel(r'$\log_{10},\sigma_{{re}}\, (km/s)$')
plt.title('Faber–Jackson plot of SAMI early-type galaxies')
plt.legend()

## additional kinematics/sigma_re uncertainties (bare minimum using provided SAMI errors)
sigma_err = df_3["sigma_re_err"].astype(float).values[mask]

# transpose error into log space and plot
xerr = (sigma_err / df_3["sigma_re"].astype(float).values[mask]) / np.log(10)  
plt.errorbar(x_pts, y_pts, xerr=xerr, yerr=None, ecolor='gray', fmt='none', capsize=2, elinewidth=0.4)

## display graph 
plt.show()