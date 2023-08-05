import pandas as pd


df = pd.read_csv(r'C:\Users\Vishwas\Desktop\To Send to Professor\CSO_links_with_cso.kmi.open.ac.uk_type.csv')

unique_urls = df['Original URL'].unique()


filtered_link_types = df[df['Link Type'].isin(['dbpedia', 'wikipedia'])]


unique_link_types = filtered_link_types['Original URL'].unique()


num_dbpedia_urls = len(filtered_link_types[filtered_link_types['Link Type'] == 'dbpedia'])
num_wikipedia_urls = len(filtered_link_types[filtered_link_types['Link Type'] == 'wikipedia'])

print("Number of unique URLs:", len(unique_urls))
print("Number of unique 'dbpedia' URLs:", num_dbpedia_urls)
print("Number of unique 'wikipedia' URLs:", num_wikipedia_urls)
