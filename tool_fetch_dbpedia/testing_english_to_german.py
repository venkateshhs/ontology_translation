import requests
from bs4 import BeautifulSoup

url = "https://dbpedia.org/page/France"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")
label_element = soup.find("span", {"property": "rdfs:label", "lang": "de"})

if label_element is not None:
    german_label = label_element.text
    print(german_label)
else:
    print("No German label found.")
