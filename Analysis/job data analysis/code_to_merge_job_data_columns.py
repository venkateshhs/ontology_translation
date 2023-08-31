import pandas as pd

# Path to the CSV file (with the same filename)
csv_path = r"/ontology_translation/Job_Data/2022-04/2022-04.csv"

# Columns to extract text from
columns_to_extract = ["full_text", "full_text_1", "full_text_2", "full_text_3", "full_text_4"]

# Read job advertisements from the CSV file and convert to DataFrame
df = pd.read_csv(csv_path, usecols=columns_to_extract)


# Define a function to handle merging
def merge_columns(row):
    merged_text = " ".join([str(val) for val in row if pd.notna(val)])
    return merged_text


# Apply the merge_columns function to create the merged_text column
df["merged_text"] = df.apply(merge_columns, axis=1)

# Save the merged DataFrame to a new CSV file
merged_csv_path = r"/ontology_translation/Job_Data/2022-04/merged_job_data_2022_04.csv"
df.to_csv(merged_csv_path, index=False)

# Print the DataFrame to ensure we have the correct data
print(df)
