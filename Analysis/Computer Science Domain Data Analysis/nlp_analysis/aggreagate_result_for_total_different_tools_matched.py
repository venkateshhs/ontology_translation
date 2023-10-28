import os
import pandas as pd

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126', '7121', '8311']
folders = ['AI', "ML"]
csv_filename = 'job_advertisement_growth_normalised.csv'

# Create an empty list to store the data
data = []

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
            years = results_df['Year'].values
            different_tools_per_year = results_df.iloc[:, 1:].gt(0).sum(axis=1).values

            # Add the data to the list
            for i in range(len(years)):
                data.append([years[i], different_tools_per_year[i], subdirectory, folder])

        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')

# Create a Pandas DataFrame from the collected data
result_df = pd.DataFrame(data, columns=['Year', 'Different tools matched', 'Job Id', 'Topic'])

# Save the DataFrame as a CSV file
result_df.to_csv(r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\total_different_tools_matched.csv', index=False)
print('Result summary saved as result_summary.csv')
