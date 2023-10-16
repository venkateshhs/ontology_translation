import os
import pandas as pd

# Define the path to the main directory
main_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of main folders (431, 7121, 7126, 8311)
main_folders = ['431', '7121', '7126', '8311']

# Create an empty list to store DataFrames for probabilities
probabilities_data_frames = []

# Iterate through each main folder
for main_folder in main_folders:
    # Create an empty list to store DataFrames for each year
    data_frames = []

    # Iterate through the years from 2015 to 2022
    for year in range(2015, 2023):
        # Define the CSV file name for the current year
        file_name = f'{main_folder}_{year}_domain_analysis.csv'

        # Construct the full file path
        file_path = os.path.join(main_directory, main_folder, str(year), file_name)

        # Check if the file exists
        if os.path.exists(file_path):
            # Read the CSV file into a DataFrame
            current_data = pd.read_csv(file_path)

            # Add a "Year" column with the current year
            current_data['Year'] = year

            # Append the DataFrame to the list
            data_frames.append(current_data)
        else:
            print(file_path, "not present")

    # Concatenate all DataFrames for this main folder
    merged_data = pd.concat(data_frames, ignore_index=True)

    # Save the merged data to a new CSV file in the main folder
    output_file_path = os.path.join(main_directory, main_folder, f'Merged_Data_for_{main_folder}_top_domain_analysis.csv')
    merged_data.to_csv(output_file_path, index=False)

    print(f"Merged data for {main_folder} and saved to {output_file_path}")

    # Calculate the probabilities of each distinct value in the 'Top Domain' column
    value_counts = merged_data['Top Domain'].value_counts()
    total_rows = len(merged_data)
    probabilities = (value_counts / total_rows )*100

    # Create a DataFrame for the current main folder's probabilities
    folder_probabilities = pd.DataFrame({'Top Domain': probabilities.index, 'Probability': probabilities.values})

    # Append the folder's probabilities to the list
    probabilities_data_frames.append(folder_probabilities)

    # Concatenate all probabilities DataFrames
    probabilities_data = pd.concat(probabilities_data_frames, ignore_index=True)
    probabilities_data["Job ID"] = main_folder
    # Save the probabilities data to a separate CSV file
    probabilities_data.to_csv(os.path.join(main_directory,main_folder, 'Top_Domain_Probabilities.csv'), index=False)

    print("Probabilities calculated and saved to Top_Domain_Probabilities.csv")
