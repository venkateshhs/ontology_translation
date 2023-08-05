import requests


def get_html_content(url):
    response = requests.get(url)
    html_content = response.text
    return html_content


dbpedia_url = "http://de.dbpedia.org/page/Hypertext_Transfer_Protocol_Secure"
html_content = get_html_content(dbpedia_url)
print(html_content)
