import pandas as pd

import unicodedata
pd.set_option('max_colwidth', 10000)
df_grouped_domains = pd.read_csv(
    r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\grouped_domain_names_final.csv')

df_paths = pd.read_csv(
    r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\new_paths.csv')

df_grouped_urls = pd.read_csv(
    r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\grouped_urls_and_tool.csv',
    encoding='ISO-8859-1')
df_grouped_urls['Parent_Url'] = df_grouped_urls['Parent_Url'].str.lower()
df_grouped_urls['Extracted_Tools'] = df_grouped_urls['Extracted_Tools'].str.replace("[", "").str.replace("]", "")

top_domain_tools_dict = {}


def has_garbled_values(string):
    for char in string:
        if unicodedata.category(char) in ('Mn', 'Me') or char == '?' or char == "[" or char == "]":
            return True
    return False


def has_non_english_chars(string):
    return not all(ord(char) < 128 for char in string)


for index, row in df_grouped_domains.iterrows():
    top_domain = row['Top Domain']
    print(top_domain)
    print(f"Processing top domain: {top_domain}")

    filtered_paths = df_paths[df_paths['New_Path'].str.startswith(top_domain)]

    unique_tools = set()
    for _, path in filtered_paths.iterrows():
        nodes = path['New_Path'].split('->')

        for node in nodes:
            tools = df_grouped_urls[df_grouped_urls['Parent_Url'] == node]['Extracted_Tools'].tolist()
            tools = [tool.strip() for sublist in tools for tool in sublist.split(',')]
            tools = [tool.strip() for tool in tools if not has_garbled_values(tool) and not has_non_english_chars(tool)]
            unique_tools.update(tools)

    top_domain_tools_dict[top_domain] = ', '.join(sorted(unique_tools))

max_records_per_column = 1000

df_output_limited = pd.DataFrame(columns=['Top Domain', 'Unique Tools'])

for top_domain, unique_tools in top_domain_tools_dict.items():
    tools_list = unique_tools.split(', ')

    num_records = len(tools_list)
    num_columns = (num_records // max_records_per_column) + 1

    for i in range(num_columns):
        start_index = i * max_records_per_column
        end_index = (i + 1) * max_records_per_column
        records = tools_list[start_index:end_index]
        records_str = ', '.join(records)

        df_output_limited.loc[len(df_output_limited)] = {'Top Domain': top_domain, 'Unique Tools': records_str}

output_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\unique_tools_by_top_domain.csv'
df_output_limited.to_csv(output_path, index=False)
print(f"Unique tools by top domain (limited) saved to: {output_path}")
