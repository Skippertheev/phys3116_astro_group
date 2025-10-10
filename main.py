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
