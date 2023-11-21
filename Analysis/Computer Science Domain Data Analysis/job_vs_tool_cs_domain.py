import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
import string
from nltk.corpus import stopwords
import os
# Load the spaCy NLP pipeline
nlp = spacy.load("en_core_web_sm")

# Load tool data from CSV
tool_data_path = r"C:\Users\Vishwas\Desktop\Thesis\ontology_translation\tool_fetch_dbpedia\Second Revison\dbpedia_tools_with_translations_alt_labels_FINAL.csv"
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
#split_tool_list_lower = list(tool_synonyms) + alternate_labels + parent_alternate_labels
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


# Initialize the PhraseMatcher
matcher = PhraseMatcher(nlp.vocab)

# Create lowercase patterns for each tool in the tool list
tool_patterns = [nlp(tool) for tool in split_tool_list_unique]

# Add the patterns to the matcher
for pattern in tool_patterns:
    matcher.add("ToolPatterns", None, pattern)

root_directory = r"C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\New data set"
for folder_name in ["2514"]:#
    folder_path = os.path.join(root_directory, folder_name)

    # Iterate over the years (2015 to 2022)
    for year in os.listdir(folder_path):
        if int(year)<2021:
            print(year)
            continue

        year_folder_path = os.path.join(folder_path, year)

        # Check if the folder contains a CSV file
        csv_file_path = os.path.join(year_folder_path, f"reduced_data_{year}.csv")
        if os.path.exists(csv_file_path):
            # Load job data from CSV
            job_data_df = pd.read_csv(csv_file_path)

            # Create lowercase patterns for each tool in the tool list
            tool_patterns = [nlp(tool) for tool in split_tool_list_unique]

            # Add the patterns to the matcher
            for pattern in tool_patterns:
                matcher.add("ToolPatterns", None, pattern)

            matched_results = []

            # Iterate through each job advertisement
            for job_text in job_data_df["merged_description"]:
                job_text_lower = job_text.lower()
                doc = nlp(job_text_lower)

                # Apply the matcher on the document
                matches = matcher(doc)

                # Get matched tool names using the match IDs
                matched_tools = [doc[start:end].text for match_id, start, end in matches]

                if matched_tools:
                    matched_results.append({"Job Advertisement": job_text_lower, "Matched Tools": matched_tools})

            # Create a DataFrame from the matched results
            matched_results_df = pd.DataFrame(matched_results)

            # Save the DataFrame to a CSV file in the corresponding folder
            output_csv_path = os.path.join(year_folder_path, f"{folder_name}_{year}_matched.csv")
            matched_results_df.to_csv(output_csv_path, index=False)
            print("Matched results saved to CSV:", output_csv_path)

            # Extract unique matched tools from the results DataFrame
            all_matched_tools = [tool for tools_list in matched_results_df["Matched Tools"] for tool in tools_list]
            unique_matched_tools = list(set(all_matched_tools))

            # Create a new DataFrame for the unique matched tools
            unique_matched_tools_df = pd.DataFrame({"Unique Matched Tools": unique_matched_tools})

            # Save the unique matched tools to a CSV file in the corresponding folder
            unique_matched_tools_csv_path = os.path.join(year_folder_path, f"{folder_name}_{year}_matched_unique.csv")
            unique_matched_tools_df.to_csv(unique_matched_tools_csv_path, index=False)
            print("Unique matched tools saved to CSV:", unique_matched_tools_csv_path)

