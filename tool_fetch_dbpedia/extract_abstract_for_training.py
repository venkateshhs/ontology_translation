import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.read_csv('dbpedia_entities.csv')
df.drop_duplicates(subset='Name', keep='first', inplace=True)


def scrape_dbpedia(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    abstract_section = soup.find('p', {'class': 'lead'})

    if abstract_section is not None:

        abstract_text = abstract_section.text.strip()
        return abstract_text
    else:

        return None


abstracts = []
for i, row in df.iterrows():

    url = row['Name']
    print(f"Extracting {url}")
    abstract = scrape_dbpedia(url)
    if abstract is not None:
        abstracts.append({'text': abstract, 'category': ''})

df_train = pd.DataFrame(abstracts)
df_train.to_csv('training_data.csv', index=False)
