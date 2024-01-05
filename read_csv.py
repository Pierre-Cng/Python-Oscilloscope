import pandas as pd
import time
from matplotlib import pyplot as plt 
from matplotlib.figure import Figure

def read(filename):
    try:
        while True:
            df = pd.read_csv(filename)  # Read the CSV file into a DataFrame
            last_100 = df.tail(100)  # Retrieve the last 100 rows
            print('\n'.join(last_100.apply(lambda row: ', '.join(map(str, row)), axis=1)))
            time.sleep(0.1)  # Wait for 5 seconds before checking for updates
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

# Replace 'data.csv' with the path to your CSV file
file_to_read = 'data.csv'
read(file_to_read)
