import itertools

import pandas as pd


csv_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_tools_with_translations_alt_labels_FINAL.csv'
df_tools = pd.read_csv(csv_path)

df_modified = pd.DataFrame(
    columns=['Parent_Url', 'Tool_Url', 'Translated Tool_Url'])  # Add 'Translated_Tool_Url' column


for index, row in df_tools.iterrows():
    parent_url = row['Parent_Url']
    tool_url = row['Tool_Url']
    translated_tool_url = row['Translated Tool_Url'].lower()  # Get the 'Translated_Tool_Url' value

    parent_url_modified = parent_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")
    tool_url_modified = tool_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")

    df_modified.loc[index] = [parent_url_modified, tool_url_modified,
                              translated_tool_url]  # Add 'translated_tool_url' to DataFrame


url_file = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\matched_tools_with_top_domains.csv'
partial_match_file = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\partial_matching_results.csv'

url_data = pd.read_csv(url_file)
partial_match_data = pd.read_csv(partial_match_file)


partial_match_urls = partial_match_data['Matched Translated Tool_Url'].unique()


urls = url_data['URL'].unique()


missing_urls = set(partial_match_urls) - set(urls)


matches_with_parent_urls = {}
cso_file = r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv'
cso_data = pd.read_csv(cso_file, encoding="ISO-8859-1")
cso_data = cso_data.apply(lambda x: x.str.replace('_', ' ').str.lower())

for url in missing_urls:
    matching_rows = df_modified[df_modified['Tool_Url'] == url]
    if not matching_rows.empty:
        parent_urls = matching_rows['Parent_Url'].tolist()
        matches_with_parent_urls[url] = parent_urls
    else:
        matching_tool = df_modified[df_modified['Translated Tool_Url'] == url]
        parent_urls = matching_tool['Parent_Url'].tolist()
        matches_with_parent_urls[url] = parent_urls


merged_csv_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\merged_complete_heirarchy.csv'
df_merged = pd.read_csv(merged_csv_path, low_memory=False)


df_merged = df_merged.astype(str)


result_data = []



length = len(matches_with_parent_urls)


def retrieve_domains(row):
    domain_values = []
    for column in df_merged.columns:
        column_values = df_merged[column]
        matching_rows = column_values[
            column_values.notna() &
            column_values.str.contains(row['Parent_URL'], regex=False, case=False)]
        if len(matching_rows) == 0:
            same_as_match = cso_data[(cso_data['object'] == row['Parent_URL'])
                                     & (cso_data['relation'] == 'owl#sameas')]
            subject_list = same_as_match['subject'].drop_duplicates().tolist()
            for subject in subject_list:
                matching_rows = column_values[
                column_values.notna() & column_values.str.contains(subject, regex=False, case=False)]
                matching_domains = df_merged.loc[matching_rows.index,
                                                 ['Domain 1', 'Domain 2']].drop_duplicates().values
                domain_values.extend(matching_domains)
                if not matching_rows.empty:
                    print("Found")
        else:
            matching_domains = df_merged.loc[matching_rows.index,
                                             ['Domain 1', 'Domain 2']].drop_duplicates().values
            domain_values.extend(matching_domains)
    return list(set(tuple(arr) for arr in domain_values))


csv_file_counter = 100

csv_file_max_records = 1000
count = 1
for url, parent_urls in matches_with_parent_urls.items():
    print(count, length)
    for parent_url in parent_urls:
        print(parent_url)
        domain_values = retrieve_domains({'Parent_URL': parent_url})
        for data in domain_values:
            row_data = {'URL': url, 'Parent_URL': parent_url, 'Domain 1': data[0], 'Domain 2': data[1]}
            result_data.append(row_data)

    count += 1
    if len(result_data) > 1000:
        result_df = pd.DataFrame(result_data)
        result_df.drop_duplicates(subset=['URL', 'Parent_URL', 'Domain 1', 'Domain 2'], inplace=True)

        result_df.to_csv(
            f"C:\\Users\\Vishwas\\Desktop\\Thesis\\tool_fetch_dbpedia\\Second Revison\\To SHow it to professor Full output\\matching\\matching_hierarchy_result_{csv_file_counter}.csv",
            index=False)
        print("Created csv file of len: ", len(result_df))
        csv_file_counter += 1
        result_data = []


result_df = pd.DataFrame(result_data)
result_df.drop_duplicates(subset=['URL', 'Parent_URL', 'Domain 1', 'Domain 2'], inplace=True)
result_df.to_csv(
    "C:\\Users\\Vishwas\\Desktop\\Thesis\\tool_fetch_dbpedia\\Second Revison\\To SHow it to professor Full output\\matching\\matching_hierarchy_result_final_second.csv",
    index=False)
