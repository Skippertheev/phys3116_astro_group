
# Main file for Computational assignment 2 PHYS 3116

# Setup for numpy as well as path
import pandas as pd
import numpy as np

# Retrieves each file from Data_Repo
cat = pd.read_csv("Data_Repo/InputCatGAMADR3.csv")
clusters = pd.read_csv("Data_Repo/samiDR3InputCatClusters.csv")
kinematics = pd.read_csv("Data_Repo/samiDR3StelKin.csv")
morph = pd.read_csv("Data_Repo/samiDR3VisualMorphology.csv")
