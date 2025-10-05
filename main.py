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
