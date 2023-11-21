import pandas as pd
import os

# Define the path to your input CSV file
input_file_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\New data set\2511\dwh_stg.tk_all_by_isco_fulltext_2511.csv'

# Define the exact column names you want to select (including square brackets and semicolons)
columns_to_select = [
    '[date]', '[profession]', '[profession_group]', '[profession_class]',
    '[profession_isco_code]', 'fulltext', '[job_description]',
    '[candidate_description]'
]

# Extract the directory path from the input file path
output_dir = os.path.dirname(input_file_path)

# Set the chunk size for reading the CSV file
chunk_size = 10000

# Read the CSV file in chunks
chunks = pd.read_csv(input_file_path, sep=';', usecols=columns_to_select, chunksize=chunk_size, low_memory=False)

# Iterate over chunks
for chunk in chunks:
    # Convert the date column to datetime format
    chunk['[date]'] = pd.to_datetime(chunk['[date]'], format='%Y-%m-%d')

    # Create a new column for the 'year' to use for folder creation
    chunk['year'] = chunk['[date]'].dt.year

    # Iterate over unique years and save data in corresponding folders
    for year in chunk['year'].unique():
        # Create a folder for each year if it doesn't exist
        year_folder = os.path.join(output_dir, str(year))
        os.makedirs(year_folder, exist_ok=True)

        # Filter data for the current year
        year_data = chunk[chunk['year'] == year].copy()

        # Merge 'job_description' and 'candidate_description' columns only if both are not empty
        year_data['merged_description'] = year_data.apply(
            lambda row: row['[job_description]'] + ' ' + row['[candidate_description]']
            if pd.notna(row['[job_description]']) and pd.notna(row['[candidate_description]'])
            else row['fulltext'],
            axis=1
        )

        # Create a new DataFrame with reduced columns
        reduced_columns = [
            '[date]', '[profession]', '[profession_group]', '[profession_class]',
            '[profession_isco_code]', 'merged_description'
        ]
        reduced_year_data = year_data[reduced_columns]

        # Define the output file path for the reduced data
        reduced_output_file_path = os.path.join(year_folder, f'reduced_data_{year}.csv')

        # Check if the file already exists
        if os.path.exists(reduced_output_file_path):
            # Append data to the existing file
            existing_data = pd.read_csv(reduced_output_file_path)
            combined_data = pd.concat([existing_data, reduced_year_data], ignore_index=True)
            combined_data.to_csv(reduced_output_file_path, index=False, encoding="utf-8")
        else:
            # Save the reduced data to a new CSV file
            reduced_year_data.to_csv(reduced_output_file_path, index=False, encoding="utf-8")

        print(f'Reduced data for year {year} saved to {reduced_output_file_path}')
