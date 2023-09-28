import pandas as pd
import os

# Define the path to your input CSV file
input_file_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\8311\dwh_stg.tk_all_by_isco_fulltext_8311.csv'

# Define the exact column names you want to select (including square brackets and semicolons)
columns_to_select = [
    '[date]', '[profession]', '[profession_group]', '[profession_class]',
    '[profession_isco_code]', 'fulltext', '[job_description]',
    '[candidate_description]'
]

# Extract the directory path from the input file path
output_dir = os.path.dirname(input_file_path)

# Define the output file name (you can change this if needed)
output_file_name = 'selected_columns.csv'

# Create the full output file path
output_file_path = os.path.join(output_dir, output_file_name)

# Read the CSV file and select the specified columns
df = pd.read_csv(input_file_path, sep=';', usecols=columns_to_select, low_memory=False)

df['[date]'] = pd.to_datetime(df['[date]'], format='%Y-%m-%d')  # Adjust the format as needed

# Extract the year from the 'date' column and create separate CSV files for each year
output_dir = os.path.dirname(input_file_path)
for year, group_df in df.groupby(df['[date]'].dt.year):
    # Define the output file name for each year
    output_file_name = f'data_{year}.csv'
    output_file_path = os.path.join(output_dir, output_file_name)

    # Save the group (data for a specific year) to a separate CSV file
    group_df.to_csv(output_file_path, index=False, encoding="utf-8")
    print(f'Data for year {year} saved to {output_file_path}')

for year in df['[date]'].dt.year.unique():
    # Load the data for the current year
    year_data = pd.read_csv(os.path.join(output_dir, f'data_{year}.csv'))

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
        '[profession_isco_code]',  'merged_description'
    ]
    reduced_year_data = year_data[reduced_columns]

    # Define the output file name for the reduced data
    reduced_output_file_name = f'reduced_data_{year}.csv'
    reduced_output_file_path = os.path.join(output_dir, reduced_output_file_name)

    # Save the reduced data to a separate CSV file
    reduced_year_data.to_csv(reduced_output_file_path, index=False, encoding="utf-8")
    print(f'Reduced data for year {year} saved to {reduced_output_file_path}')
