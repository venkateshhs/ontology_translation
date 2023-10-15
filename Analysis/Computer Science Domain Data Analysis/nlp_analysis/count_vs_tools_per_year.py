import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126']
folders = ['AI', 'microsoft']
csv_filename = 'job_advertisement_growth.csv'

# Loop through the subdirectories and folders
for subdirectory in subdirectories:
    for folder in folders:
        # Create the full path to the CSV file
        csv_file_path = os.path.join(parent_directory, subdirectory, folder, csv_filename)

        # Check if the CSV file exists
        if os.path.exists(csv_file_path):
            # Load the results from the CSV file
            results_df = pd.read_csv(csv_file_path)

            # Set the 'Year' column as the index
            results_df.set_index('Year', inplace=True)

            # Transpose the DataFrame to have matched tools as columns
            #results_df = results_df.drop(columns='Total Tools')  # Drop the 'Total Tools' column

            # Create a custom color palette
            custom_palette = sns.color_palette("husl", len(results_df.columns))

            # Create the stacked bar plot using Seaborn with the custom color palette
            plt.figure(figsize=(12, 6))
            sns.set_style("whitegrid")

            ax = results_df.plot(kind='bar', stacked=True, color=custom_palette, figsize=(12, 6))
            plt.title(f'Stacked Bar Plot of Matched Tools by Year (2015-2022) in {subdirectory}/{folder}')
            plt.xlabel('Year')
            plt.ylabel('Count')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Customize legend (optional)
            legend_labels = [plt.Line2D([0], [0], color=custom_palette[i], lw=4, label=tool)
                             for i, tool in enumerate(results_df.columns)]
            plt.legend(handles=legend_labels, title='Matched Tools', loc='upper left', bbox_to_anchor=(1, 1))

            # Save the plot as an image in the respective folder
            image_path = os.path.join(parent_directory, subdirectory, folder, 'count_vs_year.png')
            plt.tight_layout()
            plt.savefig(image_path, bbox_inches='tight')

            print(f'Stacked Bar Plot saved at: {image_path}')
        else:
            print(f'CSV file not found in {subdirectory}/{folder}.')
