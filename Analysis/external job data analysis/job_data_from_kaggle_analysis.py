import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
import string
from nltk.corpus import stopwords

# Load the spaCy NLP pipeline
nlp = spacy.load("en_core_web_sm")

# Load tool data from CSV
tool_data_path = r"C:\Users\Vishwas\Desktop\Thesis\ontology_translation\tool_fetch_dbpedia\Second Revison/dbpedia_tools_with_translations_alt_labels_FINAL.csv"
tool_data_df = pd.read_csv(tool_data_path, encoding="ISO-8859-1-")


# Process tool data columns
def process_column(column):
    return column.apply(
        lambda x: str(x).lower().split("http://dbpedia.org/resource/")[-1] if pd.notna(x) else "").tolist()


def process_de_column(column):
    return column.apply(
        lambda x: str(x).lower().split("http://de.dbpedia.org/resource/")[-1] if pd.notna(x) else "").tolist()


tool_synonyms = set()
tool_synonyms.update(process_column(tool_data_df["Tool_Url"]))
# tool_synonyms.update(process_column(tool_data_df["Parent_Url"]))  # added here
tool_synonyms.update(process_de_column(tool_data_df["German Tool URL"]))
# tool_synonyms.update(process_de_column(tool_data_df["German Parent URL"]))  # added here

# Process and add alternate labels
alternate_labels = tool_data_df["Tool Url Alternate Labels"].apply(
    lambda x: str(x).lower().split(", ") if pd.notna(x) else [])
alternate_labels = [label for sublist in alternate_labels for label in sublist if label.lower() != "nan"]

# added here
# parent_alternate_labels = tool_data_df["Parent URL Alternate Labels"].apply(
#     lambda x: str(x).lower().split(", ") if pd.notna(x) else [])
# parent_alternate_labels = [label for sublist in parent_alternate_labels for label in sublist if label.lower() != "nan"]

# Convert tool list to lowercase
# split_tool_list_lower = list(tool_synonyms) + alternate_labels + parent_alternate_labels
split_tool_list_lower = list(tool_synonyms) + alternate_labels

# Remove punctuation
split_tool_list_no_punct = [word for word in split_tool_list_lower if word not in string.punctuation]

# Remove stopwords
stop_words_english = set(stopwords.words("english"))
stop_words_german = set(stopwords.words("german"))
combined_stop_words = stop_words_english.union(stop_words_german)
split_tool_list_filtered = [word for word in split_tool_list_no_punct if word not in combined_stop_words]
underscore_remove_list = [word.replace('_', ' ') for word in split_tool_list_filtered]
# Remove duplicates using a set
split_tool_list_unique = list(set(underscore_remove_list))

# Load job data from CSV
job_data_path = r"C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Analysis\external job data analysis/dataset_from_kaggle.csv"
job_data_df = pd.read_csv(job_data_path)

# Initialize the PhraseMatcher
matcher = PhraseMatcher(nlp.vocab)

# Create lowercase patterns for each tool in the tool list
tool_patterns = [nlp(tool) for tool in split_tool_list_unique]

# Add the patterns to the matcher
for pattern in tool_patterns:
    matcher.add("ToolPatterns", None, pattern)

matched_results = []

# Iterate through each job advertisement
for job_text in job_data_df["JobRequirment"]:
    try:
        job_text_lower = job_text.lower()
    except:
        continue
    doc = nlp(job_text_lower)

    # Apply the matcher on the document
    matches = matcher(doc)

    # Get matched tool names using the match IDs
    matched_tools = [doc[start:end].text for match_id, start, end in matches]

    if matched_tools:
        matched_results.append({"Job Advertisement": job_text_lower, "Matched Tools": matched_tools})
        # print("Job Advertisement:", job_text_lower)
        print("Matched Tools:", matched_tools)
        print("=" * 40)
    else:
        print("No matches found in the job advertisement.")

# Create a DataFrame from the matched results
matched_results_df = pd.DataFrame(matched_results)

# # Save the DataFrame to a CSV file
output_csv_path = r"C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Analysis\external job data analysis/matched.csv"
matched_results_df.to_csv(output_csv_path, index=False)
#
print("Matched results saved to CSV:", output_csv_path)
all_matched_tools = [tool for tools_list in matched_results_df["Matched Tools"] for tool in tools_list]

# Convert the list to a set to remove duplicates
unique_matched_tools = list(set(all_matched_tools))

# Create a new DataFrame for the unique matched tools
unique_matched_tools_df = pd.DataFrame({"Unique Matched Tools": unique_matched_tools})

# Save the DataFrame to a CSV file
unique_matched_tools_csv_path = r"C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Analysis\external job data analysis/matched_unique.csv"
unique_matched_tools_df.to_csv(unique_matched_tools_csv_path, index=False)

print("Unique matched tools saved to CSV:", unique_matched_tools_csv_path)
