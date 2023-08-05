import requests
from bs4 import BeautifulSoup
import csv
from SPARQLWrapper import SPARQLWrapper, JSON


def get_german_uri(url):
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
            return results["results"]["bindings"][0]["resource"]["value"]
        else:
            return "No resource URI found for German label '{}'".format(url)
    else:
        return "No German label found."


with open("vectorizer_accuracies_final.csv", "r", encoding="ISO-8859-1") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    rows = [row for row in csv_reader if row["Type of Approach"] == "TF-IDF" and row["Prediction"] == "Tool"]

    print("Total rows to process:", len(rows))

    fieldnames = ["Parent URL", "Type of Approach", "Tool URL", "Accuracy", "German Parent URL", "German Tool URL",
                  "Prediction"]
    with open("german_uris.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i, row in enumerate(rows):
            parent_url = row["Parent URL"]
            tool_url = row["Tool URL"]

            try:
                german_parent_url = get_german_uri(parent_url)
            except Exception as e:
                german_parent_url = str(e)

            try:
                german_tool_url = get_german_uri(tool_url)
            except Exception as e:
                german_tool_url = str(e)

            row["German Parent URL"] = german_parent_url
            row["German Tool URL"] = german_tool_url

            try:
                writer.writerow(row)
            except Exception as e:
                print(f"Error writing row {i + 1}:", e)

            print(f"Row {i + 1} of {len(rows)}:", "Parent URL:", parent_url, "Tool URL:", tool_url,
                  "German Parent URL:", german_parent_url, "German Tool URL:", german_tool_url)
            print("\n")

print("Done")
