# Import necessary libraries
import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from zipfile import ZipFile
import yaml

# Define a function to evaluate the consistency of the dataset
def evaluate():
    """Evaluate the consistency of the dataset using R2 score."""
    # Get the directory where the script is located
    SCRIPTDIR = os.path.dirname(__file__)

    # Read the ground truth monthly values from the monthlyValues.csv file
    monthlyValues = pd.read_csv(SCRIPTDIR+'/monthlyValues.csv')
    # Read the computed monthly averages from the monthlyComputed.csv file
    monthlyValuesComputed = pd.read_csv(SCRIPTDIR+'/monthlyComputed.csv')

    # Ensure that both datasets have the same length
    if len(monthlyValues) != len(monthlyValuesComputed):
        # If they don't have the same length, truncate the longer dataset
        if len(monthlyValues) > len(monthlyValuesComputed):
            monthlyValues = monthlyValues[:len(monthlyValuesComputed)]
        else:
            monthlyValuesComputed = monthlyValuesComputed[:len(monthlyValues)]

    # Compute the R2 score to measure consistency
    r2 = r2_score(monthlyValues, monthlyValuesComputed)
    print(f"The R2 score is {r2}")
    # Check if the R2 score meets the consistency threshold
    if r2 >= 0.9:
        print('The dataset is consistent')
    else:
        print('The dataset is not consistent')

# Call the evaluate function to execute the evaluation
evaluate()