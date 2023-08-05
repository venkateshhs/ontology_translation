import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

with open('../Common/CSO.3.3.csv', 'r') as file:
    reader = csv.reader(file)
    urls = [row[0].strip('<>') for row in reader if 'cso.kmi.open.ac.uk' in row[0]]

links_list = []

urls = list(set(urls))

for url in urls:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        ext_res_heading = soup.find("h2", text="External Resources")
        ext_res_table = ext_res_heading.find_next_sibling("table")

        for row in ext_res_table.find_all("tr")[1:]:
            cols = row.find_all("td")
            link_type = cols[0].get_text().strip().lower()
            links = cols[1].find_all("a")
            for link in links:
                href = link.get("href").strip('<>')
                link_dict = {'Original URL': url, 'Link Type': '', 'Link Subtype': '', 'Links': ''}
                if "dbpedia.org" in href:
                    link_dict['Link Type'] = 'dbpedia'
                    link_dict['Link Subtype'] = link_type
                    link_dict['Links'] = href
                elif "wikipedia.org" in href:
                    link_dict['Link Type'] = 'wikipedia'
                    link_dict['Link Subtype'] = link_type
                    link_dict['Links'] = href
                else:
                    link_dict['Link Type'] = 'other'
                    link_dict['Link Subtype'] = link_type
                    link_dict['Links'] = href
                links_list.append(link_dict)

        print(f"Links extracted from {url}")
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")

df = pd.DataFrame(links_list)

df.to_csv('CSO_links.csv', index=False)

print("Data written to CSO_links.csv file.")
