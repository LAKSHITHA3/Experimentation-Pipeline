# Import necessary libraries
import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from zipfile import ZipFile
import yaml

# Define a function to prepare the data
def prepare():
    """Prepare the downloaded data for processing."""
    # Get the directory where the script is located
    SCRIPTDIR = os.path.dirname(__file__)

    # Extract the contents of the weather.zip file
    with ZipFile(SCRIPTDIR+'/weather.zip', 'r') as zObject: 
        zObject.extractall(path=SCRIPTDIR) 

    # Get the list of files in the directory
    files = os.listdir(SCRIPTDIR)
    # Filter the files to only include CSV files
    files = [file for file in files if file.endswith('.csv')]

    # Initialize variables to store file names and field names
    file_name = ''
    field_name = ''

    # Loop through each file
    for f in files:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(f)
        # Check if the specified fields have missing values
        if data['MonthlyDepartureFromNormalAverageTemperature'].isnull().sum() < len(data['MonthlyDepartureFromNormalAverageTemperature']) and data['DailyDepartureFromNormalAverageTemperature'].isnull().sum() < len(data['DailyDepartureFromNormalAverageTemperature']):
            # If there are no missing values, assign the file name and field name
            file_name = f 
            field_name = 'DailyDepartureFromNormalAverageTemperature'
            # Write the file name and field name to the fileParams.yaml file
            with open(SCRIPTDIR+'/fileParams.yaml', 'w') as file:
                file.write(f'file_name: {file_name}\n')
                file.write(f'field_name: {field_name}\n')

    # Read the specified field values from the CSV file
    monthlyValues = data['MonthlyDepartureFromNormalAverageTemperature']
    # Remove any rows with missing values
    monthlyValues.dropna(inplace=True)
    # Save the monthly values to a CSV file
    monthlyValues.to_csv(SCRIPTDIR+'/monthlyValues.csv', index=False)

# Call the prepare function to execute the data preparation
prepare()