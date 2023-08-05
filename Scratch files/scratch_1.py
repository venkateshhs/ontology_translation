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


df = pd.read_csv('C:\\Users\\Vishwas\\Desktop\\To Send to Professor\\Gold_Standard_Sample.csv')

summaries = []

for url in df['Tool URL']:
    print(url)
    summary = scrape_dbpedia(url)
    summaries.append(summary)

df['Summary'] = summaries

df.to_csv('C:\\Users\\Vishwas\\Desktop\\To Send to Professor\\summary_results.csv', encoding='utf-8', index=False)
