import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

data = pd.read_csv("../tool_fetch_dbpedia/BERT_classification_labelled_data.csv", encoding="ISO-8859-1")

X_train, X_val, y_train, y_val = train_test_split(data['text'], data['category'], test_size=0.2, random_state=42)

vectorizer = CountVectorizer(stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)

alphas = [0.1, 0.5, 1.0, 1.5, 2.0]
best_alpha = None
best_accuracy = 0

for alpha in alphas:
    clf = MultinomialNB(alpha=alpha)
    clf.fit(X_train_vec, y_train)

    y_val_pred = clf.predict(X_val_vec)
    accuracy = accuracy_score(y_val, y_val_pred)
    print(f"Alpha: {alpha}, Accuracy: {accuracy}")

    if accuracy > best_accuracy:
        best_alpha = alpha
        best_accuracy = accuracy

print(f"Best alpha: {best_alpha}, Best accuracy: {best_accuracy}")

clf = MultinomialNB(alpha=best_alpha)
clf.fit(X_train_vec, y_train)

new_text = "Donald John Trump (born June 14, 1946) is an American politician, media personality, and businessman who served as the 45th president of the United States from 2017 to 2021. Trump graduated from the Wharton School of the University of Pennsylvania with a bachelor's degree in 1968. He became president of his father's real estate business in 1971 and renamed it The Trump Organization. He expanded the company's operations to building and renovating skyscrapers, hotels, casinos, and golf courses. He later started side ventures, mostly by licensing his name. From 2004 to 2015, he co-produced and hosted the reality television series The Apprentice. Trump and his businesses have been involved in more than 4,000 state and federal legal actions, including six bankruptcies."
new_text_vec = vectorizer.transform([new_text])
new_text_pred = clf.predict(new_text_vec)
print("Prediction:", new_text_pred[0])
