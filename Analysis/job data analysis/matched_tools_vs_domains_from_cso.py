import pandas as pd

# Load the first CSV file
file1_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\Tool Analysis\matched_tools_with_top_domains.csv'
df1 = pd.read_csv(file1_path)

# Load the second CSV file
file2_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\2017-09\2017_04_matched_unique.csv'
df2 = pd.read_csv(file2_path)

result_data = []

# Iterate through each row in df2
for index, row in df2.iterrows():
    tool_name = row['Unique Matched Tools']

    # Find all matching rows in df1 based on both columns
    matching_rows = df1[
        (df1['URL'].str.contains(tool_name, case=False)) | (df1['Parent_URL'].str.contains(tool_name, case=False))]

    # Iterate through matching rows and add them to the result data list
    for _, match_row in matching_rows.iterrows():
        top_domain = match_row['Domain 1']
        first_domain = match_row['Domain 2']

        # Append the match to the result data list
        result_data.append({'Unique Matched Tools': tool_name, 'Top Domain': top_domain, 'First Domain': first_domain})

# Create a DataFrame from the result data
result_df = pd.DataFrame(result_data)
# Save the result to a new CSV file
# Drop duplicate rows based on all columns
result_df.drop_duplicates(inplace=True)
result_csv_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\2017-09\domain_analysis.csv'
result_df.to_csv(result_csv_path, index=False)
