import urllib
import requests
from bs4 import BeautifulSoup
import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from functools import lru_cache

nlp = spacy.load("en_core_web_sm")


@lru_cache(maxsize=128)
def scrape_dbpedia(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    abstract_section = soup.find('p', {'class': 'lead'})

    if abstract_section is not None:

        abstract_text = abstract_section.text.strip()
        return abstract_text
    else:
        return ""


@lru_cache(maxsize=128)
def get_alternate_labels(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        dbo_wiki_page_redirect = soup.find_all('a', {'rev': 'dbo:wikiPageRedirects'})
        redirect_list = [link.get('href') for link in dbo_wiki_page_redirect]
        return [link.replace("http://dbpedia.org/resource/", "").replace("_", " ") for link in redirect_list]
    except Exception as e:
        print("Error fetching alternate labels:", e)
        return []


@lru_cache(maxsize=128)
def get_links_from_dbpedia(dbpedia_url):
    try:
        response = requests.get(dbpedia_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        dbo_genre_links = soup.find_all('a', {'rev': 'dbo:genre'})
        dbp_genre_links = soup.find_all('a', {'rev': 'dbp:genre'})
        resultin_list = list(
            set([link.get('href') for link in dbo_genre_links] + [link.get('href') for link in dbp_genre_links]))
        return resultin_list
    except Exception as e:
        print("Error fetching links from DBpedia:", e)
        return []


@lru_cache(maxsize=128)
def get_related_entities(dbpedia_resource):
    try:

        query_result_list = []
        for resource in ("Software", "Hardware", "Tool", "Product"):
            query = f"""
        SELECT ?tool ?toolLabel ?toolLink WHERE {{
          <{dbpedia_resource}> dbo:wikiPageWikiLink ?toolLink .
          ?toolLink rdf:type dbo:{resource} .
          ?toolLink rdfs:label ?toolLabel .
          FILTER (lang(?toolLabel) = 'en')
          BIND(REPLACE(STR(?toolLink), 'http://dbpedia.org/resource/', '') AS ?tool)
        }}
        """

            query = urllib.parse.quote(query)
            url = f"http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query={query}&format=application%2Fsparql-results%2Bjson&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on"
            response = requests.get(url)
            json_data = response.json()

            for binding in json_data["results"]["bindings"]:
                link = binding["toolLink"]["value"]
                query_result_list.append(link)
        return query_result_list
    except Exception as e:
        print("Error fetching related entities from DBpedia:", e)
        return []


def is_product(text):
    try:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PRODUCT":
                return "TOOL"
        return "CONCEPT"
    except Exception as e:
        print("Error classifying text:", e)
        return "CONCEPT"


def classify_using_ml_model(parent_url, tool_url, X_train, y_train, X_val, y_val, vectorizers,
                            vectorizer_names):
    abstract_text = scrape_dbpedia(tool_url)
    accuracies = []
    scypy_classification = is_product(abstract_text)
    classification_list = []
    parent_url_alt_labels = get_alternate_labels(parent_url)
    tool_url_alt_labels = get_alternate_labels(tool_url)
    for vectorizer, vectorizer_name in zip(vectorizers, vectorizer_names):
        X_train_vec = vectorizer.fit_transform(X_train)
        X_val_vec = vectorizer.transform(X_val)

        clf = MultinomialNB()
        clf.fit(X_train_vec, y_train)

        y_val_pred = clf.predict(X_val_vec)
        accuracy = accuracy_score(y_val, y_val_pred)
        accuracies.append(accuracy)

        new_text_vec = vectorizer.transform([abstract_text])
        new_text_pred = clf.predict(new_text_vec)

        result = {"Parent_Url": parent_url, "Tool_Url": tool_url, "Type": vectorizer_name,
                  "Accuracy": accuracy, "Prediction": new_text_pred[0],
                  "ScyPy Classification": scypy_classification,
                  "Parent URL Alternate Labels": parent_url_alt_labels,
                  "Tool Url Alternate Labels": tool_url_alt_labels}
        classification_list.append(result)
    return classification_list


def get_entities_from_dbpedia(dbpedia_url, X_train, y_train, X_val, y_val, vectorizers, vectorizer_names):
    genre_links = get_links_from_dbpedia(dbpedia_url)
    query_links = get_related_entities(dbpedia_url)

    links = list(set(genre_links + query_links))
    tool_list = []
    for link in links:
        try:
            classified_tools = classify_using_ml_model(dbpedia_url, link, X_train, y_train, X_val,
                                                       y_val,
                                                       vectorizers, vectorizer_names)
            tool_list.extend(classified_tools)
        except:
            print("Error in URL:", link, "Parent URL:", dbpedia_url)
            continue
    return tool_list


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


if __name__ == '__main__':
    cso_links_df = pd.read_csv('CSO_links.csv')
    dbpedia_links_df = cso_links_df[cso_links_df['Link Type'] == 'dbpedia']
    dbpedia_urls = dbpedia_links_df['Links'].tolist()
    dbpedia_urls = list(set(dbpedia_urls))
    data = pd.read_csv("BERT_classification_labelled_data.csv", encoding="ISO-8859-1")
    X_train, X_val, y_train, y_val = train_test_split(data['text'], data['category'], test_size=0.1, random_state=42)

    vectorizers = [CountVectorizer(stop_words='english'),
                   TfidfVectorizer(stop_words='english'),
                   TfidfVectorizer(stop_words='english',
                                   ngram_range=(1, 2),
                                   max_df=0.75,
                                   min_df=2,
                                   max_features=10000)]

    vectorizer_names = ['CountVectorizer', 'TF-IDF', 'TF-IDF (ngram)']
    results = []
    count = 1
    length = len(dbpedia_urls)
    # dbpedia_urls = ['https://dbpedia.org/page/Lossless_compression',
    #                 'http://dbpedia.org/resource/Knowledge_transfer']
    already_fetched = pd.read_csv(
        "C:\\Users\\Vishwas\\Desktop\\Thesis\\tool_fetch_dbpedia\\Second Revison\\dbpedia_entities_with_genre_and_key_based_querying_0_500.csv",
        encoding="ISO-8859-1")
    already_fetched_list = list(set(list(already_fetched["Parent_Url"])))
    print(len(already_fetched_list))
    for url in dbpedia_urls:
        if url not in already_fetched_list:
            try:
                print(count, "/", length, " Processing", url)
                entities = get_entities_from_dbpedia(url, X_train, y_train, X_val, y_val, vectorizers, vectorizer_names)
                results.append(entities)
                count += 1
            except:
                print("Error Processing:", url)
                continue

    flattened_results = flatten_list(results)

    df = pd.DataFrame(flattened_results)
    df.to_csv(
        'C:\\Users\\Vishwas\\Desktop\\Thesis\\tool_fetch_dbpedia\\Second Revison\\dbpedia_entities_with_genre_and_key_based_querying_rest.csv',
        index=False, encoding="utf-8")
