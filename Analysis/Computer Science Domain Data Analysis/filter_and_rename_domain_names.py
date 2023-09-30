import os
import pandas as pd
from collections import defaultdict

# Define the directory path
directory_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\7126'

for year in range(2015, 2023):
    year_folder = os.path.join(directory_path, str(year))
    csv_file_path = os.path.join(year_folder, f'domain_analysis.csv')
    if os.path.exists(csv_file_path):
        print(f"Year: {year},{csv_file_path}")
        yearly_counts = defaultdict(int)  # Dictionary to store counts for each year

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        print(df)
        break
