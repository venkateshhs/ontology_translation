import os
import pandas as pd

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126', '7121', '8311', '2511', '2512', '2513', '2514','2519']
folders = ['ML']
csv_filename = 'job_advertisement_growth_normalised.csv'

# Create an empty DataFrame to store the pivot table
pivot_table_df = pd.DataFrame()

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
                subset_df = df[['Year', 'Total Tools']]

                # Create a pivot table
                pivot_table = pd.pivot_table(subset_df, values='Total Tools', index=None, columns='Year', aggfunc='sum', fill_value=0)

                # Add a column for subdirectory
                pivot_table['Subdirectory'] = subdirectory

                # Append the pivot table to the main DataFrame
                pivot_table_df = pd.concat([pivot_table_df, pivot_table], ignore_index=True)
            else:
                print(f'CSV file in {subdirectory}/{folder} does not contain "Total Tools" and "Year" columns.')
        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')

# Save the pivot table to a CSV file
pivot_table_csv_path = os.path.join(parent_directory, 'ML_percentage_pivot_table_result.csv')
pivot_table_df.to_csv(pivot_table_csv_path, index=False)

print(f'Pivot table saved at: {pivot_table_csv_path}')
