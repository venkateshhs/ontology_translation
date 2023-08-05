import csv


def extract_last_part(url):
    return url.rsplit('/', 1)[-1]


first_csv_path = r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv'
first_csv_data = []
print("Reading first CSV file...")
with open(first_csv_path, 'r', encoding='ISO-8859-1') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        first_csv_data.append(row)
print("First CSV file read successfully.")

second_csv_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\dbpedia_extracted_tools.csv'
parent_urls = []
print("Reading second CSV file...")
with open(second_csv_path, 'r', encoding='ISO-8859-1') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        parent_urls.append(row['Parent_Url'])
print("Second CSV file read successfully.")

urls_parts = list(set([extract_last_part(url) for url in parent_urls]))

output_csv_path = r'C:\Users\Vishwas\Desktop\Thesis\output_matches_updated.csv'
print(f"Storing matches in {output_csv_path}...")
with open(output_csv_path, 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Parent_Url', 'Subject', 'Relation', 'Object', "same as"])

    for url_part in urls_parts:
        matches = []
        for row in first_csv_data:
            subject = row[0]
            relation = row[1]
            obj = row[2]
            if relation == "cso#superTopicOf" and (url_part in subject or url_part in obj):
                matches.append([url_part, subject, relation, obj, ""])

        if len(matches) == 0:
            same_as_matches = []
            for row in first_csv_data:
                subject = row[0]
                relation = row[1]
                obj = row[2]
                if relation == "owl#sameAs" and (url_part in subject or url_part in obj):
                    same_as_matches.append(subject)
                    same_as_matches.append(obj)

            for new_url_part in same_as_matches:
                for row in first_csv_data:
                    subject = row[0]
                    relation = row[1]
                    obj = row[2]
                    if relation == "cso#superTopicOf" and (new_url_part in subject or new_url_part in obj):
                        matches.append([url_part, subject, relation, obj, new_url_part])

        csv_writer.writerows(matches)

print("Matched rows stored successfully.")
