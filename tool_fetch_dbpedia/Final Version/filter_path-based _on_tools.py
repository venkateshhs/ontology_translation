import pandas as pd

df_paths = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\paths_and_tools.csv')
df_grouped_urls = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\grouped_urls.csv', encoding='ISO-8859-1')

df_grouped_urls['Parent_Url'] = df_grouped_urls['Parent_Url'].str.lower()

unique_paths = set()

new_path_list = []

for index, row in df_paths.iterrows():
    path = row['Path'].lower().split('->')
    new_path = []
    found_tool = False

    for i in range(len(path)):
        node = path[i]
        matching_rows = df_grouped_urls[df_grouped_urls['Parent_Url'] == node]

        if not matching_rows.empty:
            found_tool = True
            new_path = path[:i+1]

    if found_tool and tuple(new_path) not in unique_paths:
        print(index)
        unique_paths.add(tuple(new_path))
        new_path_list.append('->'.join(new_path))

df_output = pd.DataFrame({'New_Path': new_path_list})
output_file_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\new_paths.csv'
df_output.to_csv(output_file_path, index=False)
print(f"New paths saved to: {output_file_path}")
