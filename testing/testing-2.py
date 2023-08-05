import pandas as pd


def handle_unicode_error(exception):
    return None


df = pd.read_csv("../tool_fetch_dbpedia/labelled_data_final.csv", on_bad_lines=handle_unicode_error,
                 encoding="ISO-8859-1", engine='python', usecols=["text", "category"])

df_tool = df[df["category"] == "Tool"]

df_tool = df_tool.dropna()

df_tool = df_tool.head(1500)

df_other = df[df["category"] == "Other"]

df_other = df_other.dropna()

df_concept = pd.read_csv("../tool_fetch_dbpedia/training_data_concept.csv", on_bad_lines=handle_unicode_error,
                         encoding="ISO-8859-1", engine='python', usecols=["text", "category"])

df_concept = df_concept[df_concept["category"] == "Concept"]

df_concept = df_concept.dropna()

df_concept = df_concept.head(1500)

df = pd.concat([df_tool, df_other, df_concept], ignore_index=True)

df.to_csv("BERT_classification_labelled_data.csv", index=False)
