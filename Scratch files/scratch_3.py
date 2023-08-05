import pandas as pd


csv1_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\CSO_links.csv'
df1 = pd.read_csv(csv1_path, encoding='ISO-8859-1')


csv2_path = r'C:\Users\Vishwas\Desktop\Thesis\urls_which-are_not_of_type_cso.kimi.uk.csv'
df2 = pd.read_csv(csv2_path, encoding='ISO-8859-1')


not_found_urls = df2[~df2['Child'].isin(df1['Links'])]


not_found_urls.to_csv(r'C:\Users\Vishwas\Desktop\Thesis\links_which_are_not_covered.csv', index=False)

print("URLs not found in the first CSV:")
print(not_found_urls)
