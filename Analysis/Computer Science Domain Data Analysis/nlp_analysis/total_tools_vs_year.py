import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126', '7121', '8311']
folders = ['AI', 'microsoft', 'ML']
csv_filename = 'job_advertisement_growth_normalised.csv'

# Loop through the subdirectories and folders
for subdirectory in subdirectories:
    for folder in folders:
        # Create the full path to the CSV file
        csv_file_path = os.path.join(parent_directory, subdirectory, folder, csv_filename)

        # Check if the CSV file exists
        if os.path.exists(csv_file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)

            # Check if 'Total Tools' and 'Year' columns exist
            if 'Total Tools' in df.columns and 'Year' in df.columns:
                # Extract 'Total Tools' and 'Year' columns as NumPy arrays
                total_tools = np.array(df['Total Tools'])
                year = np.array(df['Year'])

                # Create a line graph
                plt.figure(figsize=(10, 6))
                plt.plot(year, total_tools, marker='o', linestyle='-')
                plt.title(f'Total Tools vs. Year in {subdirectory}/{folder}')
                plt.xlabel('Year')
                plt.ylabel('Total Tools in percentage(Normalised to total job ads per year)')
                plt.xticks(rotation=45)

                # Save the plot in the respective folder
                plot_path = os.path.join(parent_directory, subdirectory, folder, 'total_tools_vs_year_line.png')
                plt.savefig(plot_path, bbox_inches='tight')

                print(f'Line graph saved at: {plot_path}')
            else:
                print(f'CSV file in {subdirectory}/{folder} does not contain "Total Tools" and "Year" columns.')
        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')
