import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126', '7121', '8311', '2511', '2512', '2513', '2514','2519']
folders = [ 'AI']
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
            # Load the results from the CSV file
            results_df = pd.read_csv(csv_file_path)

            # Extract the years and matched tools columns
            results_df = results_df.drop(columns='Total Tools')
            results_df = results_df.drop(columns='Percentage of Tools Matched')
            years = results_df['Year'].values
            matched_tools = results_df.columns[1:]

            # Calculate the number of different tools matched for each year
            different_tools_per_year = results_df.iloc[:, 1:].gt(0).sum(axis=1).values

            # Create a dictionary for the pivot table
            pivot_data = {'Job ID': [subdirectory] * len(years), 'Year': years, 'Value': different_tools_per_year}

            # Add the data to the pivot table DataFrame
            pivot_table_df = pd.concat([pivot_table_df, pd.DataFrame(pivot_data)], ignore_index=True)

            print(f'Data added for {subdirectory}/{folder}')
        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')

# Pivot the table
# Pivot the table with aggfunc=list to keep all values for duplicate entries
# Drop duplicate entries based on 'Job ID' and 'Year'
pivot_table_df = pivot_table_df.drop_duplicates(subset=['Job ID', 'Year'])

# Pivot the table
pivot_table_df = pivot_table_df.pivot_table(index='Job ID', columns='Year', values='Value').reset_index()


# Save the pivot table to a CSV file
pivot_table_csv_path = os.path.join(parent_directory, f'{folder}_count_pivot_table_result.csv')
pivot_table_df.to_csv(pivot_table_csv_path, index=False)

print(f'Pivot table saved at: {pivot_table_csv_path}')
