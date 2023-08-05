import requests
from bs4 import BeautifulSoup
from SPARQLWrapper import SPARQLWrapper, JSON
import csv

german_uri_cache = {}


def get_german_uri(url):
    if url in german_uri_cache:
        return german_uri_cache[url]

    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    label_element = soup.find("span", {"property": "rdfs:label", "lang": "de"})
    if label_element is not None:
        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbpedia-de: <http://de.dbpedia.org/resource/>
            SELECT ?resource WHERE {{
                ?resource rdfs:label "{}"@de .
                FILTER(REGEX(STR(?resource), "^http://de.dbpedia.org/resource/"))
            }}
        """.format(label_element.text)
        sparql = SPARQLWrapper("http://de.dbpedia.org/sparql")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results["results"]["bindings"]:
            german_uri = results["results"]["bindings"][0]["resource"]["value"]
            german_uri_cache[url] = german_uri
            return german_uri

    return None


input_file_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_extracted_tools.csv'
output_file_path = r"C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_tools_with_german_uri.csv"

with open(input_file_path, mode="r", encoding="ISO-8859-1") as input_file, \
        open(output_file_path, mode="w", newline="", encoding="utf-8") as output_file:
    # Create the CSV reader and writer objects
    csv_reader = csv.DictReader(input_file)
    fieldnames = csv_reader.fieldnames + ["German Parent URL", "German Tool URL"]
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    for row in csv_reader:
        try:
            parent_url = row["Parent_Url"]
            tool_url = row["Tool_Url"]

            parent_uri = get_german_uri(parent_url) if parent_url else None
            tool_uri = get_german_uri(tool_url) if tool_url else None

            output_row = {k: v for k, v in row.items()}
            output_row["German Parent URL"] = parent_uri if parent_uri else ""
            output_row["German Tool URL"] = tool_uri if tool_uri else ""
            csv_writer.writerow(output_row)
            print(f"Processed row {csv_reader.line_num}")
        except Exception as e:
            print(f"Error processing row {csv_reader.line_num}: {e}")
            continue

print("Processing completed.")
