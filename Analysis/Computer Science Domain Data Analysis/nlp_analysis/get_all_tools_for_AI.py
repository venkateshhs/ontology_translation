import pandas as pd

# Load the CSV file
csv_file_path = r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv'
df = pd.read_csv(csv_file_path, encoding="ISO-8859-1")

# Filter rows where the relation is 'cso#superTopicOf'
filtered_df = df[df['relation'] == 'cso#superTopicOf']

def find_paths(topic, df, current_path=[], result_paths=None):
    if result_paths is None:
        result_paths = []
    current_path.append(topic)
    matching_rows = df[df['subject'] == topic]

    if matching_rows.empty:
        result_paths.append(current_path.copy())
    else:
        for index, row in matching_rows.iterrows():
            child = row['object']
            find_paths(child, df, current_path, result_paths)

    return result_paths

# Example: Find different paths from 'artificial_intelligence'
input_topic = 'machine_learning'
paths = find_paths(input_topic, filtered_df)

# Flatten and get unique nodes
unique_nodes = set(node for path in paths for node in path)
print(list(unique_nodes))


# Load the CSV file with tool information
tools_file_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\tool_fetch_dbpedia\Second Revison\dbpedia_tools_with_translations_alt_labels_FINAL.csv'
tools_df = pd.read_csv(tools_file_path, encoding="ISO-8859-1")

# Create a dictionary to store results for each unique node
results = {}

# List of unique nodes
unique_nodes = unique_nodes  # Replace with your list of unique nodes

for node in unique_nodes:
    matching_rows = tools_df[tools_df['Parent_Url'].str.contains(node, case=False, na=False)]
    if not matching_rows.empty:
        tool_urls = matching_rows['Tool_Url'].tolist()
        tool_alt_labels = matching_rows['Tool Url Alternate Labels'].tolist()
        for tool_url, alt_label in zip(tool_urls, tool_alt_labels):
            tool_name = tool_url.replace("http://dbpedia.org/resource/", "")
            if tool_name not in results:
                results[tool_name] = []
            results[tool_name].append(alt_label)

# Create a DataFrame from the results
result_df = pd.DataFrame(list(results.items()), columns=["Tool Name", "Alternate Tool Names"])

# Save the DataFrame to a CSV file
result_csv_file = r'C:\Users\Vishwas\Desktop\Thesis\Common\results_ML.csv'
result_df.to_csv(result_csv_file, index=False)
