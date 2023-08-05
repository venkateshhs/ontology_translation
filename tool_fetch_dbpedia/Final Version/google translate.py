import csv
import re

from deep_translator import GoogleTranslator


def get_dbpedia_title(url):
    title_match = re.search(r'/([^/]+)$', url)
    if title_match:
        title = title_match.group(1)
        title = title.replace('_', ' ')
        return title
    return None


def translate_text(text):
    title_to_translate = get_dbpedia_title(text)
    try:
        translation = GoogleTranslator(source='en', target='de').translate(title_to_translate)
        return translation
    except Exception:
        print("Exception occured")
        return text


input_file_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_tools_with_german_uri.csv'
output_file_path = r"C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_tools_with_translations_alt_labels_FINAL.csv"

with open(input_file_path, mode="r", encoding="utf-8") as input_file, \
        open(output_file_path, mode="w", newline="", encoding="utf-8") as output_file:
    csv_reader = csv.DictReader(input_file)
    fieldnames = csv_reader.fieldnames + ["German Url title", "Translated Parent_Url", "Translated Tool_Url"]
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    translated_titles = {}
    translated_urls = {}

    for row in csv_reader:
        german_url = row["German Parent URL"]
        german_title = get_dbpedia_title(german_url) if german_url else None
        row["German Url title"] = german_title if german_title else ""

        parent_url = row["Parent_Url"]

        if parent_url and parent_url not in translated_urls:
            translated_parent_url = translate_text(parent_url)
            translated_urls[parent_url] = translated_parent_url
        else:
            translated_parent_url = translated_urls.get(parent_url, "")
        row["Translated Parent_Url"] = translated_parent_url

        tool_url = row["Tool_Url"]
        if tool_url and tool_url not in translated_urls:
            translated_tool_url = translate_text(tool_url)
            translated_urls[tool_url] = translated_tool_url
        else:
            translated_tool_url = translated_urls.get(tool_url, "")
        row["Translated Tool_Url"] = translated_tool_url

        csv_writer.writerow(row)
        print(f"Processed row {csv_reader.line_num}")

print("Translation process completed.")
