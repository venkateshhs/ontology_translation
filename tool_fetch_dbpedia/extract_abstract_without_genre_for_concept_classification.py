import csv
import pandas as pd

import requests
from bs4 import BeautifulSoup


def scrape_dbpedia(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    abstract_section = soup.find('p', {'class': 'lead'})

    if abstract_section is not None:

        abstract_text = abstract_section.text.strip()
        return abstract_text
    else:

        return None


unique_links = set()
with open('dbpedia_entities_without_genre.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        link = row['URL']
        if link not in unique_links:
            unique_links.add(link)
            if len(unique_links) == 1500:
                break

abstracts = []
for link in unique_links:
    print("Processing:", link)
    abstract = scrape_dbpedia(link)
    if abstract is not None and abstract != '':
        abstracts.append({'link': link, 'text': abstract, 'category': ''})
        print("Abstract extracted")
    else:
        print("No abstract found, skipping...")

df_train = pd.DataFrame(abstracts)
df_train.to_csv('training_data_concept.csv', index=False)
