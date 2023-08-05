import csv
import unicodedata

input_csv_file = 'C:\\Users\\Vishwas\\Desktop\\Thesis\\tool_fetch_dbpedia\\Second Revison\\dbpedia_entities_with_genre_and_key_based_querying_full_final.csv'
output_csv_file = 'C:\\Users\\Vishwas\\Desktop\\Thesis\\tool_fetch_dbpedia\\Second Revison\\dbpedia_entities_with_genre_and_key_based_querying_without_duplicates_and_special_characters.csv'


def has_garbled_values(string):
    for char in string:
        if unicodedata.category(char) in ('Mn', 'Me') or char == '?' or char == "[" or char == "]":
            return True
    return False


def has_non_english_chars(string):
    return not all(ord(char) < 128 for char in string)


data = []
invalid_labels = set()

with open(input_csv_file, 'r', encoding='ISO-8859-1') as file:
    reader = csv.DictReader(file)
    for row in reader:
        tool_labels = row['Tool Url Alternate Labels']
        parent_labels = row['Parent URL Alternate Labels']
        if tool_labels:
            labels = [label.strip().lower() for label in tool_labels.split(',')]
            parent_labels = [label.strip().lower() for label in parent_labels.split(',')]

            unique_labels = []
            invalid_row_labels = []
            for label in labels:
                label = label.replace("[", "").replace("]", "")
                if not has_garbled_values(label) and not has_non_english_chars(label):
                    unique_labels.append(label)
                else:
                    invalid_row_labels.append(label)

            row['Tool Url Alternate Labels'] = ', '.join(list(set(unique_labels)))

            if invalid_row_labels:
                print("Invalid Tool labels:", invalid_row_labels)

            parent_unique_labels = []
            invalid_parent_labels = []
            for label in parent_labels:
                label = label.replace("[", "").replace("]", "")
                if not has_garbled_values(label) and not has_non_english_chars(label):
                    parent_unique_labels.append(label)
                else:
                    invalid_parent_labels.append(label)

            row['Parent URL Alternate Labels'] = ', '.join(list(set(parent_unique_labels)))

            if invalid_parent_labels:
                print("Invalid Parent labels:", invalid_parent_labels)

        data.append(row)

fieldnames = data[0].keys()
with open(output_csv_file, 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("Modified data has been written to", output_csv_file)
