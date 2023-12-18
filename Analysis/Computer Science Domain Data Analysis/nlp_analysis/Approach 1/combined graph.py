import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126', '7121', '8311', '2511', '2512', '2513', '2514','2519']
folders = ['ML']# 'AI', 'ML'
csv_filename = 'job_advertisement_growth_normalised.csv'

# Create a color map for different subcategories
color_map = {'431': 'blue', '7126': 'green', '7121': 'red', '8311': 'purple',
             '2511': 'cyan', '2512': 'magenta', '2513': 'orange', '2514': 'pink', '2519': 'yellow'}


# Create a line graph
plt.figure(figsize=(10, 6))

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
                total_tools = np.array(df['Percentage of Tools Matched'])
                year = np.array(df['Year'])

                # Plot the line with different colors for each subcategory
                plt.plot(year, total_tools, marker='o', linestyle='-', label=f'{subdirectory}/{folder}', color=color_map[subdirectory])

                print(f'Line graph added for {subdirectory}/{folder}')
            else:
                print(f'CSV file in {subdirectory}/{folder} does not contain "Total Tools" and "Year" columns.')
        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')

# Add labels and legend
plt.title('Percentage of Different Tools vs. Year for Different Job Sets')
plt.xlabel('Year')
plt.ylabel('Percentage (Normalized to total job ads per year)')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

# Save the plot
plot_path = os.path.join(parent_directory, f'{folder}_combined_total_tools_vs_year_line_for_all_tools.png')
plt.savefig(plot_path, bbox_inches='tight')

print(f'Combined line graph saved at: {plot_path}')
plt.show()
