import pandas as pd


df_tools = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_extracted_tools.csv', encoding='ISO-8859-1')

df_tools['Parent_Url'] = df_tools['Parent_Url'].str.split("http://dbpedia.org/resource/").str[1]
df_tools['Tool_Url'] = df_tools['Tool_Url'].str.split("http://dbpedia.org/resource/").str[1]


grouped_urls = df_tools.groupby('Parent_Url')['Tool_Url'].apply(list)


df_grouped_urls = pd.DataFrame({'Parent_Url': grouped_urls.index, 'Extracted_URLs': grouped_urls.values})


df_grouped_urls.to_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\grouped_urls.csv', index=False)
