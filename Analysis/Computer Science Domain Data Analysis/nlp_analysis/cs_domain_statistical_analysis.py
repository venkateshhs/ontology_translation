import os
import pandas as pd
from collections import defaultdict

# Define the directory path
directory_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\7121'

# List of tools to match
tools_to_match = [
    "IBM Watson NLU",
    "Google Cloud Natural Language",
    "Amazon Comprehend",
    "Microsoft Azure Text Analytics",
    "IBM Watson Discovery",
    "Lexalytics Semantria",
    "Aylien",
    "MonkeyLearn",
    "RapidMiner",
    "Rosoka",
    "Expert.ai",
    "Diffbot",
    "Linguamatics",
    "Bitext",
    "KNIME Text Processing",
    "MeaningCloud",
    "Provalis Research WordStat",
    "Converseon",
    "DatumBox",
    "LexisNexis",
    "GPU (Graphics Processing Unit)",
    "TPU (Tensor Processing Unit)",
    "NLTK (Natural Language Toolkit)",
    "spaCy",
    "Gensim",
    "Stanford NLP",
    "OpenNLP",
    "CoreNLP",
    "TextBlob",
    "AllenNLP",
    "BERT (Bidirectional Encoder Representations from Transformers)",
    "Textblob",
    "IBM Watson",
    "Amazon Comprehend",
    "AYLIEN",
    "Stanford CoreNLP",
    "Apache OpenNLP",
    "Google Cloud",
    "MonkeyLearn",
    "Amazon Comprehend",
    "Google Cloud NLP API",
    "Textacy",
    "PyTorch-NLP",
    "PyTorch",
    "Retext",
    "Compromise",
    "Natural",
    "Nlp.js",
    "OpenNLP",
    "StanfordNLP",
    "CogCompNLP"

]

# Create a list to store the results as dictionaries
results_data = []

# Loop through each year's folder (2015 to 2022)
for year in range(2015, 2023):
    year_folder = os.path.join(directory_path, str(year))
    csv_file_path = os.path.join(year_folder, f'7121_{year}_matched.csv')

    # Check if the CSV file exists
    if os.path.exists(csv_file_path):
        print(f"Year: {year}")
        yearly_counts = defaultdict(int)  # Dictionary to store counts for each year

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Check if 'Matched Tools' column exists
        if 'Matched Tools' in df.columns:
            # Iterate through the 'Matched Tools' column
            for index, row in df.iterrows():
                matched_tools = row['Matched Tools']
                if isinstance(matched_tools, str):
                    # Split the comma-separated values
                    tools_list = matched_tools.split(',')
                    for tool in tools_list:
                        tool = tool.strip().lower()  # Convert to lowercase
                        for t in tools_to_match:
                            if t.lower() in tool:
                                yearly_counts[t] += 1

        # Create a dictionary for the yearly counts
        yearly_counts['Year'] = year
        results_data.append(yearly_counts)
        print("\n")
    else:
        print(f"Year {year} CSV file not found.\n")

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(results_data)

# Save the results to a CSV file
results_csv_file = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\7121\nlp\job_advertisement_growth.csv'
results_df.to_csv(results_csv_file, index=False)
print(f"Results saved to {results_csv_file}")
