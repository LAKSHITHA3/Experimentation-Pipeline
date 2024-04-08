#!/usr/bin/env python3

import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from zipfile import ZipFile
import yaml

# Define the directory where the script is located
SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))
# Path to the YAML configuration file
YAMLFILE = os.path.join(SCRIPTDIR,'params.yaml')
# Load parameters from the configuration file
with open(YAMLFILE, 'r') as file:
    params = yaml.safe_load(file)

# Extract the year from the parameters
year = params['year']
# Construct URL to fetch climatological data for the specified year
url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}/'
# Send a request to the URL and parse the response content using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# Extract rows containing data from the HTML table
rows = soup.find("table").find_all("tr")[2:-2]

# Initialize an empty list to store file names
fileName = []

# Get the total number of locations specified in the parameters
total = params.get('n_locs')

# Validate input arguments
if total is None or total <= 0:
    raise ValueError("Invalid value for 'n_locs'. It must be a positive integer.")

# Randomly select locations and extract their data
for i in range(total):
    # Generate a random index to select a row from the HTML table
    index = random.randint(0, len(rows) - 1)  # Adjust index range to avoid out-of-range error
    # Extract data from the selected row
    data = rows[index].find_all("td")
    # Append the file name to the list
    fileName.append(data[0].text)

# Create a directory to store downloaded files
output_dir = os.path.join(SCRIPTDIR, 'data')
os.makedirs(output_dir, exist_ok=True)

# Download weather data for the selected locations and save them to a directory
for name in fileName:
    newUrl = url + name
    response = requests.get(newUrl)
    file_path = os.path.join(output_dir, name)
    with open(file_path, 'wb') as file:
        file.write(response.content)

# Create a ZIP file containing all the downloaded data
with ZipFile(os.path.join(SCRIPTDIR, 'weather.zip'), 'w') as zip:
    for file in fileName:
        file_path = os.path.join(output_dir, file)
        zip.write(file_path, os.path.basename(file_path))

