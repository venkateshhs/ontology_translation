import os
import pandas as pd

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126', '7121', '8311']
folders = ['AI', 'ML']
csv_filename = 'job_advertisement_growth_normalised.csv'

# Create an empty list to store DataFrames
dfs = []

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
                # Extract 'Total Tools' and 'Year' columns
                df['Job ID'] = subdirectory
                df['Topic'] = folder
                dfs.append(df[['Year', 'Total Tools', 'Job ID', 'Topic']].rename(columns={'Total Tools': 'Percentage'}))
            else:
                print(f'CSV file in {subdirectory}/{folder} does not contain "Total Tools" and "Year" columns.')
        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')

# Concatenate DataFrames
result_df = pd.concat(dfs, ignore_index=True)

# Save the result to a CSV file
result_df.to_csv(r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\year_wise_total_tools.csv', index=False)

# Print the result for reference
print(result_df)
