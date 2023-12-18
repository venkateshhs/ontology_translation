import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126', '7121', '8311', '2511', '2512', '2513', '2514', '2519']
folders = ['ML']  # 'AI',, "ML"
csv_filename = 'job_advertisement_growth_normalised.csv'

# Create an empty DataFrame to store the pivot table
pivot_table_df = pd.DataFrame()

# Create a single line graph for all subdirectories and folders
plt.figure(figsize=(12, 6))

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

            # Calculate the total number of tools matched for each year
            total_matched_per_year = results_df.iloc[:, 1:].sum(axis=1).values

            # Calculate the number of different tools matched for each year
            different_tools_per_year = results_df.iloc[:, 1:].gt(0).sum(axis=1).values
            # Plot the number of different tools matched for each year
            plt.plot(years, different_tools_per_year, marker='o', linestyle='-', label=f'{subdirectory}/{folder}')

            # Add labels and legends
            plt.title(f'Count of Different {folder} Tools Matched for all data set')
            plt.xlabel('Year')
            plt.ylabel('Count')

            plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

            # Save the result as a pivot table
            results_df['Subdirectory'] = subdirectory
            results_df['Folder'] = folder
            pivot_table_df = pd.concat([pivot_table_df, results_df], ignore_index=True)

            print(f'Line graph added for {subdirectory}/{folder}')
        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')

# Save the combined line graph as an image
plot_path = os.path.join(parent_directory,
                         f'{folder}_total_tool_count_combined_job_advertisement_growth_normalised_for_all_tools.png')
plt.grid(False)

plt.tight_layout()
plt.savefig(plot_path)
plt.show()

# Save the pivot table to a CSV file
# pivot_table_csv_path = os.path.join(parent_directory, f'{folder}_total_toolspivot_table_result.csv')
# pivot_table_df.to_csv(pivot_table_csv_path, index=False)
#
# print(f'Combined line graph saved at: {plot_path}')
# print(f'Pivot table saved at: {pivot_table_csv_path}')
