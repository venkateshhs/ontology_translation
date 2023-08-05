import pandas as pd


url_file = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\matched_tools_with_top_domains.csv'
partial_match_file = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\partial_matching_results.csv'
cso_file = r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv'

url_data = pd.read_csv(url_file)
partial_match_data = pd.read_csv(partial_match_file)
cso_data = pd.read_csv(cso_file)


cso_data = cso_data.apply(lambda x: x.str.replace('_', ' ').str.lower())


partial_match_urls = partial_match_data['Matched Translated Tool_Url'].unique()


urls = url_data['URL'].unique()


missing_urls = set(partial_match_urls) - set(urls)
print(len(missing_urls))
