import requests
from bs4 import BeautifulSoup


def get_links_from_dbpedia(dbpedia_url):
    response = requests.get(dbpedia_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    dbo_genre_links = soup.find_all('a', {'rev': 'dbo:wikiPageRedirects'})
    if not dbo_genre_links:
        print("No 'Synonym' links found in the page.", dbpedia_url)
    return [link.get('href') for link in dbo_genre_links]


dbpedia_link = "https://dbpedia.org/page/Artificial_intelligence"
redirect_links = get_links_from_dbpedia(dbpedia_link)


for link in redirect_links:
    print(link)
