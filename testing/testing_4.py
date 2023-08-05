import requests
import wikipediaapi


def get_summary(link):
    page_title = link.split("/")[-1]

    wiki_api = wikipediaapi.Wikipedia('en')

    page = wiki_api.page(page_title)

    if page.exists():
        return page.summary

    return "No summary found for this page."


wikipedia_links = [
    "/wiki/Artificial_intelligence",
    "/wiki/Python_(programming_language)",
    "/wiki/Raspberry_Pi"
]

for link in wikipedia_links:
    if link.startswith("/wiki/"):
        url = "https://en.wikipedia.org" + link
        summary = get_summary(url)
        print("Link:", url)
        print("Summary:")
        print(summary)
        print()
