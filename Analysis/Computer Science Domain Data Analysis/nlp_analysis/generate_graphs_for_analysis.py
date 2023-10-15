import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126']
folders = ['AI', 'microsoft', "ML"]
csv_filename = 'job_advertisement_growth_normalised.csv'

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
            matched_tools = results_df.columns[1:]

            # Calculate the total number of tools matched for each year
            total_matched_per_year = results_df.iloc[:, 1:].sum(axis=1).values

            # Calculate the number of different tools matched for each year
            different_tools_per_year = results_df.iloc[:, 1:].gt(0).sum(axis=1).values

            # Create line graphs for both statistics
            plt.figure(figsize=(12, 6))

            # Plot the number of different tools matched for each year
            plt.plot(years, different_tools_per_year, marker='o', linestyle='-', label='Different Tools Matched', color='green')

            # Plot the total number of tools matched for each year
            # plt.plot(years, total_matched_per_year, marker='o', linestyle='-', label='Total Tools Matched', color='blue')

            for i, value in enumerate(different_tools_per_year):
                plt.annotate(f'{value}', (years[i], value), textcoords="offset points", xytext=(0, 10), ha='center')

            # Add labels and legends
            plt.title(f'Total vs. Different Tools Matched for Each Year in {subdirectory}/{folder}')
            plt.xlabel('Year')
            plt.ylabel('Count')
            plt.legend()

            # Save the plot as an image in the respective folder
            plot_path = os.path.join(parent_directory, subdirectory, folder, 'job_advertisement_growth_normalised.png')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(plot_path)

            print(f'Image saved at: {plot_path}')
        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')
