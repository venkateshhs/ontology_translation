import pandas as pd
import os

# Define the path to the directory containing the CSV files
directory_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\8311'

# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Iterate through the years from 2015 to 2022
for year in range(2015, 2023):
    # Define the CSV file name for the current year
    file_name = f'%GT Count of First Domain by First Domain_{year}.csv'

    # Construct the full file path
    file_path = os.path.join(directory_path, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the CSV file into a DataFrame
        current_data = pd.read_csv(file_path)

        # Add a "Year" column with the current year
        current_data['Year'] = year

        # Concatenate the data with the merged_data DataFrame
        merged_data = pd.concat([merged_data, current_data], ignore_index=True)

# Save the merged data to a new CSV file
merged_data.to_csv(os.path.join(directory_path, '8311_Merged_Domain_Analysis.csv'), index=False)

print("Merged and saved to Merged_Data.csv")
