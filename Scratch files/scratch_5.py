import urllib

import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_related_entities(dbpedia_resource):
    query = f"""
SELECT ?tool ?toolLabel ?toolLink WHERE {{
  <{dbpedia_resource}> dbo:wikiPageWikiLink ?toolLink .
  ?toolLink rdf:type dbo:Software .
  ?toolLink rdfs:label ?toolLabel .
  FILTER (lang(?toolLabel) = 'en')
  BIND(REPLACE(STR(?toolLink), 'http://dbpedia.org/resource/', '') AS ?tool)
}}
"""

    query = urllib.parse.quote(query)
    url = f"http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query={query}&format=application%2Fsparql-results%2Bjson&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on"
    response = requests.get(url)
    response = requests.get(url)
    print(response.content)
    json_data = response.json()
    entities = {'Tools': [], 'Concepts': []}
    for binding in json_data["results"]["bindings"]:
        tool_name = binding["tool"]["value"]
        tool_label = binding["toolLabel"]["value"]
        link = binding["toolLink"]["value"]
        print(tool_name, tool_label, link)


dbpedia_resource = "http://dbpedia.org/resource/Computer_cluster"
get_related_entities(dbpedia_resource)
