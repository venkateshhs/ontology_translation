import pandas as pd

url_file = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\matched_tools_with_top_domains.csv'
partial_match_file = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\partial_matching_results.csv'
cso_file = r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv'

url_data = pd.read_csv(url_file)
partial_match_data = pd.read_csv(partial_match_file)
cso_data = pd.read_csv(cso_file, encoding='ISO-8859-1')
cso_data = cso_data.apply(lambda x: x.str.replace('_', ' ').str.lower())

partial_match_urls = partial_match_data['Matched Translated Tool_Url'].unique()


urls = url_data['URL'].unique()


missing_urls = set(partial_match_urls) - set(urls)

csv_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_tools_with_translations_alt_labels_FINAL.csv'
df_tools = pd.read_csv(csv_path)

df_modified = pd.DataFrame(
    columns=['Parent_Url', 'Tool_Url', 'Translated Tool_Url'])

for index, row in df_tools.iterrows():
    parent_url = row['Parent_Url']
    tool_url = row['Tool_Url']
    translated_tool_url = row['Translated Tool_Url'].lower()

    parent_url_modified = parent_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")
    tool_url_modified = tool_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")

    df_modified.loc[index] = [parent_url_modified, tool_url_modified,
                              translated_tool_url]

matches_with_parent_urls = {}

for url in missing_urls:
    matching_rows = df_modified[df_modified['Tool_Url'] == url]
    if not matching_rows.empty:
        parent_urls = matching_rows['Parent_Url'].tolist()
        matches_with_parent_urls[url] = parent_urls
    else:
        matching_tool = df_modified[df_modified['Translated Tool_Url'] == url]
        parent_urls = matching_tool['Parent_Url'].tolist()
        matches_with_parent_urls[url] = parent_urls


for url, parent_urls in matches_with_parent_urls.items():

    for parent_url in parent_urls:
        print(url, parent_url)
        paths = []
        top_domains = []
        first_domains = []

        stack = [(parent_url, [parent_url])]
        visited = set([parent_url])

        while stack:
            current_url, path = stack.pop()

            same_as_match = cso_data[(cso_data['object'] == current_url) & (cso_data['relation'] == 'owl#sameas')]

            if not same_as_match.empty:
                for subject in same_as_match['subject'].unique():
                    first_parent = cso_data[
                        (cso_data['object'] == subject) & (cso_data['relation'] == 'cso#supertopicof')]
                    if not first_parent.empty:
                        for first_subject in first_parent['subject'].unique():
                            updated_path = path + [first_subject]
                            stack.append((first_subject, updated_path))
                            top_domains.append(tuple(updated_path))
                            first_domains.append(first_parent['object'].values[0])

        print("URL:", url)
        print("Parent URL:", parent_url)
        print("Paths:")
        for i, path in enumerate(top_domains):
            path = list(path)
            top_domain = path[-1]
            first_domain = first_domains[i]
            print("Path", i + 1, ":", ' -> '.join(path))
            print("Top Domain:", top_domain)
            print("First Domain:", first_domain)
            print("------------------------")
