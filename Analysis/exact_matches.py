import pandas as pd

translated_urls_file = r"C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_tools_with_translations_alt_labels_FINAL.csv"

tools_file = r"C:\Users\Vishwas\Desktop\Thesis\Code\tools_2018.csv"

df_translated_urls = pd.read_csv(translated_urls_file)

df_tools = pd.read_csv(tools_file)

df_translated_urls["Translated Parent_Url"] = df_translated_urls["Translated Parent_Url"].str.lower()
df_translated_urls["Translated Tool_Url"] = df_translated_urls["Translated Tool_Url"].str.lower()
df_tools["SX_TERM"] = df_tools["SX_TERM"].str.lower()
df_tools["SX_CLASS_LABEL"] = df_tools["SX_CLASS_LABEL"].str.lower()

columns = ["Matched Translated Parent_Url", "Matched Translated Tool_Url", "Matched SX_TERM", "Matched SX_CLASS_LABEL",
           "SX_CLASS_ID", "SX_CLASS_NR"]
results = []

for _, row_translated in df_translated_urls.iterrows():
    translated_tool_url = row_translated["Translated Tool_Url"]

    translated_tool_url = translated_tool_url.lower() if isinstance(translated_tool_url, str) else ""

    matches = df_tools[
        (df_tools["SX_TERM"] == translated_tool_url) |
        (df_tools["SX_CLASS_LABEL"] == translated_tool_url)
        ]

    for _, row_match in matches.iterrows():
        result = {
            "Matched Translated Tool_Url": translated_tool_url,
            "Matched SX_TERM": row_match["SX_TERM"],
            "Matched SX_CLASS_LABEL": row_match["SX_CLASS_LABEL"],
            "SX_CLASS_ID": row_match["SX_CLASS_ID"],
            "SX_CLASS_NR": row_match["SX_CLASS_NR"]
        }
        results.append(result)

df_matching_results = pd.DataFrame(results, columns=columns)

df_matching_results = df_matching_results.drop_duplicates()

output_file_path = r"C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\exact_matching_results.csv"
df_matching_results.to_csv(output_file_path, index=False)

print(df_matching_results)
