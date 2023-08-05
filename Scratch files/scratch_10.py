import pandas as pd

df_tools = pd.read_csv('dbpedia_tools_with_translations_alt_labels_FINAL.csv')
df_modified = df_tools[['Parent_Url', 'Tool_Url', 'Translated Tool_Url']].copy()
df_modified.columns = ['Parent_Url', 'Tool_Url', 'Translated_Tool_Url']
df_modified[['Parent_Url', 'Tool_Url']] = df_modified[['Parent_Url', 'Tool_Url']].apply(
    lambda x: x.str.split("http://dbpedia.org/resource/")[1].str.lower().str.replace("_", " "))

df_partial = pd.read_csv('partial_matching_results.csv')

df_merged = df_modified.merge(df_partial, left_on='Tool_Url', right_on='Matched Translated Tool_Url', how='outer')

df_hierarchy = pd.read_csv('merged_complete_heirarchy.csv', low_memory=False)

df_hierarchy = df_hierarchy.astype(str)

result_data = []

count = 1
length = df_merged.shape[0]


def retrieve_domains(row):
    domain_values = set()
    for column in df_hierarchy.columns:
        column_values = df_hierarchy[column]
        matching_rows = column_values[
            column_values.notna() & column_values.str.contains(row['Parent_Url'], regex=False, case=False)]
        if not matching_rows.empty:
            unique = matching_rows.drop_duplicates()
            domain_values.update(unique.index)
    return list(domain_values)


csv_file_counter = 1
result_csv_path = f'matching_hierarchy_result_{csv_file_counter}.csv'
csv_file_max_records = 3000

for _, row in df_merged.iterrows():
    print(count, length)

    parent_urls = row['Parent_Url']
    domain_values = retrieve_domains(row)

    if domain_values:
        domain_columns = ['Domain 1', 'Domain 2']
        for index in domain_values:
            row_data = {'URL': row['Matched Translated Tool_Url'], 'Parent_URL': parent_urls}
            row_data.update(df_hierarchy.loc[index, domain_columns].to_dict())
            result_data.append(row_data)

    count += 1

    if count % csv_file_max_records == 0:
        result_df = pd.DataFrame(result_data)
        result_df.drop_duplicates(subset=['URL', 'Parent_URL', 'Domain 1', 'Domain 2'], inplace=True)

        result_df.to_csv(result_csv_path, index=False)

        csv_file_counter += 1
        result_csv_path = f'matching_hierarchy_result_{csv_file_counter}.csv'
        result_data = []

result_df = pd.DataFrame(result_data)
result_df.drop_duplicates(subset=['URL', 'Parent_URL', 'Domain 1', 'Domain 2'], inplace=True)
result_df.to_csv(result_csv_path, index=False)
