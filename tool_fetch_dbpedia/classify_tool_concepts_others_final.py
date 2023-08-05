import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

data = pd.read_csv("BERT_classification_labelled_data.csv", encoding="ISO-8859-1")

urls_data = pd.read_csv("dbpedia_entities_without_genre.csv")
urls_data = urls_data[["URL", "Name"]]

X_train, X_val, y_train, y_val = train_test_split(data['text'], data['category'], test_size=0.2, random_state=42)

vectorizers = [CountVectorizer(stop_words='english'),
               TfidfVectorizer(stop_words='english'),
               TfidfVectorizer(stop_words='english',
                               ngram_range=(1, 2),
                               max_df=0.75,
                               min_df=2,
                               max_features=10000)]

vectorizer_names = ['CountVectorizer', 'TF-IDF', 'TF-IDF (ngram)']

results = []

for index, row in urls_data.iterrows():

    print(index, "Extracting:", row['Name'])
    page = requests.get(row['Name'])

    soup = BeautifulSoup(page.content, 'html.parser')

    abstract_section = soup.find('p', {'class': 'lead'})

    if abstract_section is not None:

        new_text = abstract_section.text.strip()

        accuracies = []
        for vectorizer, vectorizer_name in zip(vectorizers, vectorizer_names):
            X_train_vec = vectorizer.fit_transform(X_train)
            X_val_vec = vectorizer.transform(X_val)

            clf = MultinomialNB()
            clf.fit(X_train_vec, y_train)

            y_val_pred = clf.predict(X_val_vec)
            accuracy = accuracy_score(y_val, y_val_pred)
            accuracies.append(accuracy)

            new_text_vec = vectorizer.transform([new_text])
            new_text_pred = clf.predict(new_text_vec)

            result = {"URL": row['URL'], "Type": vectorizer_name, "Name": row['Name'],
                      "Accuracy": accuracy, "Prediction": new_text_pred[0]}
            results.append(result)

results_df = pd.DataFrame(results)
results_df.to_csv("vectorizer_accuracies.csv", index=False)

print(results_df)
