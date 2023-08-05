import pandas as pd


csv1_path = r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.csv'
df1 = pd.read_csv(csv1_path, encoding='ISO-8859-1')


csv2_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\CSO_links.csv'
df2 = pd.read_csv(csv2_path, encoding='ISO-8859-1')


df1['Parent'] = df1['Parent'].str.strip('<>')
df1['Child'] = df1['Child'].str.strip('<>')


filtered_urls_with_keywords = df1[df1['Parent'].str.contains('dbpedia.org|wikipedia.org') | df1['Child'].str.contains('dbpedia.org|wikipedia.org')]


filtered_urls_with_keywords.to_csv(r'C:\Users\Vishwas\Desktop\Thesis\filtered_urls_with_keywords.csv', index=False)

print("URLs that start with 'dbpedia' or 'wikipedia':")
print(filtered_urls_with_keywords)
