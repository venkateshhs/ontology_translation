import pandas as pd


dbpedia_entities_df = pd.read_csv('dbpedia_entities.csv')
dbpedia_urls = set(dbpedia_entities_df['URL'].unique())


cso_links_df = pd.read_csv('CSO_links.csv')
dbpedia_links_df = cso_links_df[cso_links_df['Link Type'] == 'dbpedia']
dbpedia_links = set(dbpedia_links_df['Links'].unique())


missing_links = dbpedia_links - dbpedia_urls


dbpedialinks_without_genre = pd.DataFrame(missing_links, columns=['Links'])
dbpedialinks_without_genre.to_csv("dbpedialinks_without_genre.csv")
print(f"Number of unique URLs in dbpedia_entities: {len(dbpedia_urls)}")
print(f"Number of unique URLs in CSO_links with Link Type of dbpedia: {len(dbpedia_links)}")
print(f"Number of missing URLs: {len(missing_links)}")
print("Missing URLs:")
print(missing_links)
