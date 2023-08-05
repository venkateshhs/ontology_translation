import pandas as pd
import math

df_paths = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\new_paths.csv')

df_grouped_urls = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\grouped_urls.csv',
                              encoding='ISO-8859-1')

df_grouped_urls['Parent_Url'] = df_grouped_urls['Parent_Url'].str.lower()

extracted_tools_dict = {}


def get_extracted_tools(node):
    if node in extracted_tools_dict:
        return extracted_tools_dict[node]

    matching_rows = df_grouped_urls[df_grouped_urls['Parent_Url'] == node]
    if not matching_rows.empty:
        extracted_tools = matching_rows['Extracted_Tools'].tolist()
        # Store the extracted tools in the dictionary
        extracted_tools_dict[node] = extracted_tools
        return extracted_tools
    return []


df_output = pd.DataFrame(columns=['New_Path', 'First Domain', 'Second Domain', 'Third Domain', 'Extracted Tools'])

for index, row in df_paths.iterrows():
    path = row['New_Path'].lower().split('->')

    extracted_tools = [get_extracted_tools(node) for node in path]

    if any(extracted_tools):
        print(index)
        first_domain = path[0] if len(path) >= 1 else ''
        second_domain = path[1] if len(path) >= 2 else ''
        third_domain = path[2] if len(path) >= 3 else ''

        flattened_tools = [tool for sublist in extracted_tools for tool in sublist]

        if flattened_tools:

            row_data = {
                'Path': row['New_Path'],
                'First Domain': first_domain,
                'Second Domain': second_domain,
                'Third Domain': third_domain,
                'Extracted Tools': ', '.join(flattened_tools)
            }
            df_output = pd.concat([df_output, pd.DataFrame(row_data, index=[0])], ignore_index=True)

if not df_output.empty:
    output_dir = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison'
    rows_per_file = 250000
    num_files = math.ceil(len(df_output) / rows_per_file)

    for i in range(num_files):
        start_index = i * rows_per_file
        end_index = (i + 1) * rows_per_file
        file_path = f'{output_dir}\\extracted_tools_{i+1}.csv'
        df_output.iloc[start_index:end_index].to_csv(file_path, index=False)
        print(f"Extracted tools saved to: {file_path}")

else:
    print("No paths with extracted tools found.")
