import requests
import spacy
from bs4 import BeautifulSoup
import pandas as pd

nlp = spacy.load("en_core_web_sm")


def is_product(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PRODUCT":
            return True
    return False


def get_tools(dbpedia_resource):
    query = f"""
    SELECT ?tool ?toolLabel ?toolLink WHERE {{
      <{dbpedia_resource}> dbo:wikiPageWikiLink ?toolLink .
      ?toolLink rdf:type dbo:Software .
      ?toolLink rdfs:label ?toolLabel .
      FILTER (lang(?toolLabel) = 'en')
      BIND(REPLACE(STR(?toolLink), 'http://dbpedia.org/resource/', '') AS ?tool)
    }}
    """

    url = f"http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query={query}&format=application%2Fsparql-results%2Bjson&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on"
    response = requests.get(url)
    json_data = response.json()
    entities = {'Tools': [], 'Concepts': []}
    for binding in json_data["results"]["bindings"]:
        tool_name = binding["tool"]["value"]
        tool_label = binding["toolLabel"]["value"]
        link = binding["toolLink"]["value"]
        if is_product(link):
            entities['Tools'].append(link)
        else:
            entities['Concepts'].append(link)
    return entities


if __name__ == '__main__':
    cso_links_df = pd.read_csv('dbpedialinks_without_genre.csv')
    dbpedia_urls = cso_links_df['Links'].tolist()
    results = []
    length = len(dbpedia_urls)
    for index in range(0, length):
        dbpedia_resource = dbpedia_urls[index]
        entities_dict = get_tools(dbpedia_resource)
        print(f"{index}/{length}: Tools related to {dbpedia_resource}:")
        for tool in entities_dict['Tools']:
            results.append({'URL': dbpedia_resource, 'Type': 'Tool', 'Name': tool})
        for concept in entities_dict['Concepts']:
            results.append({'URL': dbpedia_resource, 'Type': 'Concept', 'Name': concept})

    results_df = pd.DataFrame(results, columns=['URL', 'Type', 'Name'])
    results_df.to_csv('dbpedia_entities_without_genre.csv', index=False)
