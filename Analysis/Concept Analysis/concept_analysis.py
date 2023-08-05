import itertools

import pandas as pd


csv_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\Concept Analysis\dbpedia_concepts.csv'
df_tools = pd.read_csv(csv_path)

df_modified = pd.DataFrame(
    columns=['Parent_Url', 'Tool_Url'])

for index, row in df_tools.iterrows():
    parent_url = row['Parent_Url']
    tool_url = row['Tool_Url']

    parent_url_modified = parent_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")
    tool_url_modified = tool_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")

    df_modified.loc[index] = [parent_url_modified, tool_url_modified]

cso_file = r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv'
cso_data = pd.read_csv(cso_file, encoding="ISO-8859-1")
cso_data = cso_data.apply(lambda x: x.str.replace('_', ' ').str.lower())


merged_csv_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\merged_complete_heirarchy.csv'
df_merged = pd.read_csv(merged_csv_path, low_memory=False)


df_merged = df_merged.astype(str)

result_data = []


def retrieve_domains(value):
    domain_values = []
    for column in df_merged.columns:
        column_values = df_merged[column]
        matching_rows = column_values[
            column_values.notna() & column_values.str.contains(value, regex=False, case=False)]
        if len(matching_rows) == 0:
            same_as_match = cso_data[(cso_data['object'] == value) & (cso_data['relation'] == 'owl#sameas')]
            subject_list = same_as_match['subject'].drop_duplicates().tolist()
            for subject in subject_list:
                matching_rows = column_values[
                    column_values.notna() & column_values.str.contains(subject, regex=False, case=False)]
                matching_domains = df_merged.loc[matching_rows.index, ['Domain 1', 'Domain 2']].drop_duplicates().values
                domain_values.extend(matching_domains)
        else:
            matching_domains = df_merged.loc[matching_rows.index, ['Domain 1', 'Domain 2']].drop_duplicates().values
            domain_values.extend(matching_domains)
    return list(set(tuple(arr) for arr in domain_values))


csv_file_counter = 100

csv_file_max_records = 1000
count = 1
selected_column = df_modified['Parent_Url']
length = len(selected_column)
duplicate_dictionary = {}
for index, value in selected_column.items():
    print(index)
    if value in duplicate_dictionary:
        domain_values = duplicate_dictionary[value]
    else:
        domain_values = retrieve_domains(value)
        duplicate_dictionary[value] = domain_values

    tool_url = df_modified.loc[index, 'Tool_Url']
    for data in domain_values:
        row_data = {'URL': tool_url, 'Parent_URL': value, 'Domain 1': data[0], 'Domain 2': data[1]}
        result_data.append(row_data)

    count += 1
    if len(result_data) > 1000:
        result_df = pd.DataFrame(result_data)
        result_df.drop_duplicates(subset=['URL', 'Parent_URL', 'Domain 1', 'Domain 2'], inplace=True)

        result_df.to_csv(
            f"C:\\Users\\Vishwas\\Desktop\\Thesis\\tool_fetch_dbpedia\\Second Revison\\Concept Analysis\\matching\\matching_hierarchy_concept_result_{csv_file_counter}.csv",
            index=False)
        print("Created csv file of len: ", len(result_df))
        csv_file_counter += 1
        result_data = []
        duplicate_dictionary = {}


# Create the final DataFrame and save it to a CSV file
result_df = pd.DataFrame(result_data)
result_df.drop_duplicates(subset=['URL', 'Parent_URL', 'Domain 1', 'Domain 2'], inplace=True)
result_df.to_csv(
    "C:\\Users\\Vishwas\\Desktop\\Thesis\\tool_fetch_dbpedia\\Second Revison\\Concept Analysis\\matching\\matching_hierarchy_concept_result_final_second.csv",
    index=False)
