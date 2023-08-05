import requests
import csv

person_query = '''
SELECT DISTINCT ?s ?abstract WHERE {
    ?s dbo:abstract ?abstract .
    FILTER (LANG(?abstract)='en') .
    ?s rdf:type <http://dbpedia.org/ontology/Person> .
} LIMIT 200
'''

city_query = '''
SELECT DISTINCT ?s ?abstract WHERE {
    ?s dbo:abstract ?abstract .
    FILTER (LANG(?abstract)='en') .
    ?s rdf:type <http://dbpedia.org/ontology/City> .
} LIMIT 200
'''

country_query = '''
SELECT DISTINCT ?s ?abstract WHERE {
    ?s dbo:abstract ?abstract .
    FILTER (LANG(?abstract)='en') .
    ?s rdf:type <http://dbpedia.org/ontology/Country> .
} LIMIT 200
'''

politician_query = '''
SELECT DISTINCT ?s ?abstract WHERE {
    ?s dbo:abstract ?abstract .
    FILTER (LANG(?abstract)='en') .
    ?s rdf:type <http://dbpedia.org/ontology/Politician> .
} LIMIT 200
'''


endpoint = 'http://dbpedia.org/sparql'
params = {'format': 'json'}


print('Sending SPARQL queries to DBpedia...')
person_response = requests.get(endpoint, params={'query': person_query, **params}).json()
person_rows = person_response['results']['bindings']

city_response = requests.get(endpoint, params={'query': city_query, **params}).json()
city_rows = city_response['results']['bindings']

country_response = requests.get(endpoint, params={'query': country_query, **params}).json()
country_rows = country_response['results']['bindings']

politician_response = requests.get(endpoint, params={'query': politician_query, **params}).json()
politician_rows = politician_response['results']['bindings']


rows = person_rows + city_rows + country_rows + politician_rows
print(f'Retrieved {len(rows)} rows from DBpedia.')
print('Writing results to CSV file...')
with open('dbpedia_others_abstracts.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['DBpedia Link', 'Abstract'])
    for row in rows:
        dbpedia_link = row['s']['value']
        abstract = row['abstract']['value']
        writer.writerow([dbpedia_link, abstract])
print('Done!')
