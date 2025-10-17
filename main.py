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


# drop missing rows
df = merged_galaxy.copy()
df = df[df["type"] == 0].copy()
col_needed = ["sigma_re", "m_r_kin", "z_spec_kin"]
df = df.dropna(subset = col_needed)

# todo - filter through each column
X = 100
Y = 100
Z = 100
df = df[(df["sigma_re"] > X) & (df["m_r_kin"] < Y) & (df["z_spec_kin"] > Z)]

# Now, let us create a plot of the disperision vs. magnitude to see if a FJ curve will appear for all of the galaxies
ds_red = print(type0)

df = pd.DataFrame(merged_galaxy)

df.plot(x='m_r_kin', y='vsigma_max', kind='scatter')
plt.show()

# Running this shows no linear trend, and therefore, our FJ curve must be created with our refined data

print(type0)

df = pd.DataFrame(type0)

df.plot(x='m_r_kin', y='vsigma_max', kind='scatter')
plt.show()

# Curiously, running this still gives just as random a scattering, just with less points. This indicates, that the 
# data is still unrefined or the the m_r_kin is the incorrect magnitude to use or vsigma_max is the incorrect
# dispersion to be used. This will be a point of discussion into next weeks meeting to understand why that data is
# wrong.

# Keep only elliptical galaxies
df = merged_galaxy[merged_galaxy['type'] == 0].copy()

# Filter for ellipticity between 0.2 and 0.8 (best elliptical galaxies)
df = df[(df['ellip_kin'] > 0.2) & (df['ellip_kin'] < 0.8)]

# Drop rows with missing values in key columns (cleans data to not run into problems when plotting and analysing,
# like breaking mathematical operations and skewing results) --> replaced third variable because it is not relevant
df = df.dropna(subset=['sigma_re', 'm_r_kin', 'mstar_kin'])

# Upon some reflection, one of the reasons that the practice FJ curve may not have worked is because the dispersion is
# meant to be to the power of four. A further reason for the failure is that the relationship is between dispersion^4
# and luminosity.


# The conversion between Magnitude and Luminosity is given as: L=(L_o)*10**(0.4((M_o)-M))
# For M_o = abs. magnitude of the sun (= 4.85), L_o = luminosity of the sun (3.83*10**26), M = abs. magnitude of each
# selected galaxy

def lum(x):
   return (3.83*10**26)*10**(1.932-0.4*x)

df['m_r_kin'] = df['m_r_kin'].apply(lum)

def quart(x):
   return x**4

df['sigma_re'] = df['sigma_re'].apply(quart)

df_lumin = df['m_r_kin']
df_quart = df['sigma_re']

df3 = pd.DataFrame(df_lumin)
df4 = pd.DataFrame(df_quart)

print(df3)

print(df4)

# This should now have two data frames for luminosity and for the dispersion^4.

# NOTE: After some discussion, we concluded that it the conversion may not be necesssary (as is explained below), 


# Base Faber–Jackson Relation plot using both L∝σ^4 and M∝σ^4 (same as logL=m*logσ+b). The given formula assumes a linear relationship, 
# and since M is inversly proportional to luminosity, the graph with luminosity values is flipped for a clear representation

# 'sigma_re' is how much the speeds of stars inside a galaxy differ from each other
# 'm_r_kin' is the apparent luminosity of a galaxy in the red filter
# 'mstar_kin' is stellar magnitude calculated from velocity dispersion and radius
# I think the variables are already in log form?


# Scatter plot: apparent luminosity vs velocity dispersion (the higher the velocity dispersion the lower the luminosity)
# Allowing vs code to show me multiple windows with graphs at the same time
plt.figure()
df.plot(x='m_r_kin', y='sigma_re', kind='scatter')
# Inverted for positive intercept (gcs stands for 'get current axes')
plt.gca().invert_xaxis()

# Labels
plt.title('Faber Jackson Relation (SAMI Elliptical Galaxies)')
plt.xlabel('r-band magnitude m_r_kin')
plt.ylabel('Velocity dispersion σ_re (km/s)')


# Scatter plot: magnitude vs velocity dispersion (the higher the velocity dispersion the higher the magnitude)
plt.figure()
plt.scatter(df['sigma_re'], df['m_r_kin'])
df.plot(x='mstar_kin', y='sigma_re', kind='scatter') 

# Labels
plt.title('Faber Jackson Relation (SAMI Elliptical Galaxies)')
plt.xlabel('Stellar magnitude mstar_kin')
plt.ylabel('Velocity dispersion σ_re (km/s)')

plt.show())
