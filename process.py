# Import necessary libraries
import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from zipfile import ZipFile
import yaml

# Define a function to process the downloaded data
def process():
    """Process the downloaded data to compute monthly averages."""
    # Get the directory where the script is located
    SCRIPTDIR = os.path.dirname(__file__)
    
    # Load parameters from the fileParams.yaml file
    with open(SCRIPTDIR+'/params.yaml', 'r') as file:
        params = yaml.safe_load(file)

    # Read the CSV file containing the downloaded data
    data = pd.read_csv(params['downloaded_data.csv'])

    # Convert the 'DATE' column to datetime format
    data['DATE'] = pd.to_datetime(data['DATE'])
    # Extract the month from the 'DATE' column and create a new column
    data['Month'] = data['DATE'].dt.month
    # Calculate the mean of the specified field for each month
    monthlyValues = data.groupby('Month')[params['field_name']].mean()
    # Save the computed monthly averages to a CSV file
    monthlyValues.to_csv(SCRIPTDIR+'/monthlyComputed.csv', index=False)

# Call the process function to execute the data processing
process()