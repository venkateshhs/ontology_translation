import pandas as pd


csv_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\partial_matching_results.csv'
df_partial = pd.read_csv(csv_path)


matched_urls = df_partial['Matched Translated Tool_Url']

unique_tools_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\unique_tools_by_top_domain.csv'
df_unique = pd.read_csv(unique_tools_path)


domain_counts = {}


matched_urls_set = set()


for url in matched_urls:
    matched_domains = set()
    for tools in df_unique['Unique Tools']:
        tool_list = [tool.strip().strip("'").lower().replace('"', "'").replace('_', ' ') for tool in tools.split(",")]
        if url in tool_list:
            domains = df_unique.loc[df_unique['Unique Tools'] == tools, 'Top Domain']
            matched_domains.update(domains)
            matched_urls_set.add(url)
    for domain in matched_domains:
        if domain in domain_counts:
            domain_counts[domain] += 1
        else:
            domain_counts[domain] = 1


print("Number of tools matched for each domain:")
for domain, count in domain_counts.items():
    print(f"{domain}: {count}")


unmatched_urls = set(matched_urls) - matched_urls_set
print("\nURLs that didn't match with any tools:")
for url in unmatched_urls:
    print(url)
