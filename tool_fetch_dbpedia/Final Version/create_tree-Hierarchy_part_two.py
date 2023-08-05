import csv
import pandas as pd

first_csv_path = r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv'
first_df = pd.read_csv(first_csv_path, encoding='ISO-8859-1')

output_matches_path = r'C:\Users\Vishwas\Desktop\Thesis\output_matches.csv'
output_matches_df = pd.read_csv(output_matches_path)

new_matches = output_matches_df.copy()

while True:
    print("Searching for new matches...")
    existing_matches = new_matches[['Subject', 'Relation', 'Object']].values.tolist()
    added_matches = False

    for row in new_matches.itertuples(index=False):
        subject = row[0]
        relation = row[1]
        obj = row[2]

        matches_subject = first_df[
            (first_df['subject'] == subject) & (first_df['relation'] == 'cso#superTopicOf')
        ]
        matches_object = first_df[
            (first_df['object'] == obj) & (first_df['relation'] == 'cso#superTopicOf')
        ]

        exists = [subject, relation, obj] in existing_matches

        if (len(matches_subject) > 0 or len(matches_object) > 0) and not exists:
            parent_url = row[3] if pd.notnull(row[3]) else ''  # Assign empty string for new entries
            new_triplet = [subject, relation, obj, parent_url]
            new_matches = new_matches.append(pd.DataFrame([new_triplet], columns=new_matches.columns), ignore_index=True)
            existing_matches.append([subject, relation, obj])
            added_matches = True

    if not added_matches:
        break

    print(f"Found {len(new_matches) - len(output_matches_df)} new matches. Continuing the search...")

updated_matches_csv_path = r'C:\Users\Vishwas\Desktop\Thesis\updated_matches.csv'
new_matches.to_csv(updated_matches_csv_path, index=False)

print("Updated matches stored successfully.")
