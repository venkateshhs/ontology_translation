from bs4 import BeautifulSoup
import requests

base_url = "https://en.wikipedia.org"
start_url = f"{base_url}/wiki/Outline_of_computer_science"

categories = ["Tools", "Concepts", "Others"]
links = {category: [] for category in categories}

url = start_url
while url:
    print(f"Processing {url}...")

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find("div", {"id": "mw-content-text"})

    for category in categories:
        if category == "Others":
            links[category] += [f"{base_url}{link['href']}" for link in content.find_all("a") if link.get("href", "").startswith("/wiki") and ":" not in link.get("href", "")]
        else:
            links[category] += [f"{base_url}{link['href']}" for link in content.find_all("a", {"title": f"{category} in computer science"}) if link.get("href").startswith("/wiki")]

    next_link = soup.find("a", {"class": "next"})
    url = f"{base_url}{next_link['href']}" if next_link else None

for category in categories:
    print(f"{category} Links: {len(links[category])}")
