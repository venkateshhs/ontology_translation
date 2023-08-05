import pandas as pd

df = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv', encoding='ISO-8859-1')
df_filtered = df[df['relation'] == 'cso#superTopicOf']

top_nodes = set(df_filtered['subject']) - set(df_filtered['object'])
end_nodes = set(df_filtered['object']) - set(df_filtered['subject'])

subject_points = {}


def get_child_nodes(subject):
    child_nodes = set(df_filtered[df_filtered['subject'] == subject]['object'])
    return child_nodes


def create_paths(top_domain, current_path):
    paths = []
    child_nodes = get_child_nodes(top_domain)
    if not child_nodes:
        return [current_path]
    for node in child_nodes:
        new_path = current_path + [node]
        paths.extend(create_paths(node, new_path))
    return paths


all_paths = []
for top_domain in top_nodes:
    paths = create_paths(top_domain, [top_domain])
    all_paths.extend(paths)

df_grouped_urls = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\grouped_urls.csv',
                              encoding='ISO-8859-1')


def get_extracted_tools(node):
    matching_row = df_grouped_urls[df_grouped_urls['Parent_Url'] == node]
    if not matching_row.empty:
        return matching_row['Extracted_Tools'].values[0]
    return []


data = []
for path in all_paths:
    path_str = "->".join(path)
    path_tools = []
    for node in path:
        extracted_tools = get_extracted_tools(node)
        if extracted_tools:
            path_tools.append(f"{node} ({', '.join(extracted_tools)})")
    data.append([path_str, ", ".join(path_tools)])

df_paths = pd.DataFrame(data, columns=["Path", "Extracted Tools"])

for index, row in df_paths.iterrows():
    print("Path:", row["Path"])
    print("Extracted Tools:", row["Extracted Tools"])
    print()

df_paths.to_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\paths_and_tools.csv', index=False)
