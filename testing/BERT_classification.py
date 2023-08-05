import pandas as pd
import numpy as np
import tensorflow as tf
from transformers import AutoTokenizer, TFDistilBertForSequenceClassification


data = pd.read_csv("../tool_fetch_dbpedia/BERT_classification_labelled_data.csv", encoding="ISO-8859-1")


model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFDistilBertForSequenceClassification.from_pretrained(model_name)


texts = data['text'].tolist()
labels = data['category'].tolist()
encoded = tokenizer(texts, padding=True, truncation=True, return_tensors='tf')


train_size = int(0.8 * len(data))
train_dataset = tf.data.Dataset.from_tensor_slices((dict(encoded), labels)).shuffle(len(data)).batch(16)
test_data = {key: encoded.data[key][train_size:] for key in encoded.data.keys()}

test_dataset = tf.data.Dataset.from_tensor_slices((test_data)).batch(16)


optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
model.compile(optimizer=optimizer, loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
model.fit(train_dataset, epochs=3, validation_data=test_dataset)


new_text = "Artificial intelligence (AI) is intelligence—perceiving, synthesizing, and infering information—demonstrated by machines, as opposed to intelligence displayed by animals and humans. Example tasks in which this is done include speech recognition, computer vision, translation between (natural) languages, as well as other mappings of inputs. The Oxford English Dictionary of Oxford University Press defines artificial intelligence as"
new_text_encoded = tokenizer(new_text, padding=True, truncation=True, return_tensors='tf')
new_text_pred = model.predict(new_text_encoded)
predicted_category = np.argmax(new_text_pred, axis=1)[0]
print("Prediction:", predicted_category)
