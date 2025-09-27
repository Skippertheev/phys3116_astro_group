
# Main file for Computational assignment 2 PHYS 3116

# Setup for numpy as well as path
import pandas as pd
import numpy as np

# Retrieves each file from Data_Repo
cat = pd.read_csv("Data_Repo/InputCatGAMADR3.csv")
clusters = pd.read_csv("Data_Repo/samiDR3InputCatClusters.csv")
kinematics = pd.read_csv("Data_Repo/samiDR3StelKin.csv")
morph = pd.read_csv("Data_Repo/samiDR3VisualMorphology.csv")

"""description: 

cat -- galaxy global properties, Contains (catid, [radius, declination] coord, r-band magnitudes, log_mass, color(g-i), ellip, pa, survey and quality?)
morph -- galaxy morphology, Contains (catid, type [0 ~ ellipitcal, 1 ~ lenticular, 2+ ~ spirals], early/late types)
cluster -- galaxy clusters, Contains (catid, cluster ID, membership flags etc)
kinematics -- galaxy kinematics properties, Contains (catid, velcity dispersion, velocity uncertainry, position)

"""

# merges the files into a singular table named merged_galaxy
# TODO add and fix merge 
merged_galaxy = (
    cat.merge(kinematics, on = 'catid', how = 'inner', validate = 'one to one', suffixes = '_kin')
        .merge(clusters, on = 'catid', how = 'left', validate = 'one to one', suffixes = '_clust')
        .merge(morph, on = 'catid', how = 'left', validate = 'one to one', suffixes = '_morph')
)

# visualise full table by printing it
