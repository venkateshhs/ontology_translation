import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from gensim.models import Word2Vec
import nltk
nltk.download('punkt')


data = pd.read_csv("BERT_classification_labelled_data.csv", encoding="ISO-8859-1")


X_train, X_val, y_train, y_val = train_test_split(data['text'], data['category'], test_size=0.2, random_state=42)


vectorizer = CountVectorizer(stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)


clf = MultinomialNB()
clf.fit(X_train_vec, y_train)


y_val_pred = clf.predict(X_val_vec)
accuracy = accuracy_score(y_val, y_val_pred)
print("Accuracy using bag-of-words:", accuracy)


vectorizer_tfidf = TfidfVectorizer(stop_words='english')
X_train_vec_tfidf = vectorizer_tfidf.fit_transform(X_train)
X_val_vec_tfidf = vectorizer_tfidf.transform(X_val)


clf_tfidf = MultinomialNB()
clf_tfidf.fit(X_train_vec_tfidf, y_train)


y_val_pred_tfidf = clf_tfidf.predict(X_val_vec_tfidf)
accuracy_tfidf = accuracy_score(y_val, y_val_pred_tfidf)
print("Accuracy using TF-IDF:", accuracy_tfidf)


corpus = [nltk.word_tokenize(text) for text in X_train]
model = Word2Vec(corpus, size=100, window=5, min_count=1, workers=4)

X_train_vec_w2v = np.array([np.mean([model[word] for word in doc], axis=0) for doc in corpus])
X_val_vec_w2v = np.array([np.mean([model[word] for word in nltk.word_tokenize(text)], axis=0) for text in X_val])

clf_w2v = MultinomialNB()
clf_w2v.fit(X_train_vec_w2v, y_train)

y_val_pred_w2v = clf_w2v.predict(X_val_vec_w2v)
accuracy_w2v = accuracy_score(y_val, y_val_pred_w2v)
print("Accuracy using word embeddings:", accuracy_w2v)

new_text = "Goggles, or safety glasses, are forms of protective eyewear that usually enclose or protect the area surrounding the eye in order to prevent particulates, water or chemicals from striking the eyes. They are used in chemistry laboratories and in woodworking. They are often used in snow sports as well, and in swimming. Goggles are often worn when using power tools such as drills or chainsaws to prevent flying particles from damaging the eyes. Many types of goggles are available"
