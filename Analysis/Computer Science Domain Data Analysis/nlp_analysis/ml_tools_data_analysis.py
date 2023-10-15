import os
import pandas as pd
from collections import defaultdict

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126']

tools_to_match = [
    "H2O.ai",
    "DataRobot",
    "AutoKeras",
    "TPOT (Tree-Based Pipeline Optimization Tool)",
    "Docker",
    "Kubernetes",
    "Flask",
    "Django",
    "AWS SageMaker",
    "MXNet",
    "Theano",
    "Chainer",
    "Deeplearning4j",
    "PaddlePaddle",
    "Apache Spark",
    "Hadoop",
    "Flink",
    "Databricks",
    "Beam",
    "Dialogflow (formerly API.ai)",
    "Microsoft Bot Framework",
    "Rasa",
    "IBM Watson Assistant",
    "Amazon Lex",
    "Tableau",
    "Power BI",
    "QlikView",
    "IBM Cognos",
    "Domo",
    "IBM Watson Health",
    "Google Health",
    "NVIDIA Clara",
    "PathAI",
    "Tempus",
    "QuantLib",
    "Alteryx",
    "Kensho",
    "AlphaSense",
    "Darktrace",
    "Cylance",
    "CrowdStrike",
    "Palo Alto Networks Cortex",
    "Vectra",
    "ROS (Robot Operating System)",
    "Gazebo",
    "MoveIt!",
    "RoboFlow",
    "Isaac SDK",
    "Apache Mahout",
    "Surprise",
    "LightFM",
    "Amazon Personalize",
    "Reco4j",
    "Unity ML-Agents",
    "Unreal Engine AI",
    "Godot Engine AI",
    "CryEngine AI",
    "Lumberyard",
    "ChatGPT",
    "Google Bard",
    "Chatsonic",
    "Midjourney",
    "DALL-E",
    "SlidesAI",
    "Alli AI",
    "Jasper AI",
    "Paradox",
    "Synthesia",
    "aiXcoder",
    "TabNine",
    "DeepBrain AI",
    "SecondBrain",
    "Textio",
    "Wordtune",
    "Figstack",
    "Descript",
    "INK",
    "LyricStudio",
    "Scikit Learn",
    "TensorFlow",
    "PyTorch",
    "CNTK",
    "Caffe",
    "Apache MXNet",
    "Keras",
    "OpenNN",
    "AutoML",
    "H2O",
    "Conclusion",
    "LOVO",
    "Murf.AI",
    "OpenAI API key",
    "Transformer",
    "Writesonic",
    "Copy.ai",
    "Jasper",
    "Grammarly",
    "DALL·E 2",
    "Pikazo",
    "Deep Dream Generator",
    "Deep AI",
    "Artbreeder",
    "Leap AI",
    "ImgCreator",
    "Synthesia",
    "Fliki",
    "Invideo",
    "Tabnine",
    "GitHub Copilot",
    "DeepCode",
    "Jedi",
    "AskCodi",
    "You.com",
    "Andi",
    "Play.ht",
    "Beautiful.ai",
    "Presentations.ai",
    "Wonderslide",
    "Wepik",
    "Beatoven.ai",
    "Soundraw",
    "Soundful",
    "Voicemod",
    "Chatfuel Lite",
    "Tidio",
    "BotStar",
    "Dialogflow",
    "Voice.ai",
    "Veritone Voice",
    "Overdub",
    "VIC AI",
    "Indy",
    "Docyt",
    "Gradescope",
    "Unriddle",
    "TLDR This",
    "Antivirus software",
    "Amazon Alexa",
    "Megvii",
    "Celia (virtual_assistant)",
    "Horovod (machine_learning)",
    "Horovod",
    "IPhoto",
    "TikTok",
    "SHRDLU",
    "Bruno Sartori",
    "Deeplearning4j",
    "TensorFlow",
    "Afiniti",
    "Zo_(bot)",
    "Your.MD",
    "Tay (bot)",
    "GPT-3",
    "GPT",
    "ADS-AC",
    "siri",
    "Google Search Engine",
    "Google Assistant",
    "Google Photos",
    "Google Translate",
    "Google Maps",
    "Gmail",
    "YouTube",
    "Google Cloud AI",
    "UMBEL",
    "DeepSpeed",
    "Caffe",
    "Feature_Selection_Toolbox",
    "RCASE",
    "Keras",
    "Anaconda (Python distribution)",
    "Kubeflow",
    "Scikit-learn",
    "OpenNN",
    "FastText",
    "SPSS Modeler",
    "Gboard",
    "Mlpack",
    "CatBoost",
    "Conference on Neural Information Processing Systems",
    "ELKI",
    "Yooreeka",
    "Orange (software)",
    "Apache SystemML",
    "LightGBM",
    "KXEN Inc.",
    "Flux (machine-learning_framework)",
    "PyTorch",
    "NeuroSolutions",
    "Mlpy",
    "Vowpal_Wabbit",
    "KNIME",
    "Google JAX",
    "Microsoft Cognitive Toolkit",
    "RapidMiner",
    "Theano (software)",
    "Apache Mahout",
    "SAS (software)",
    "Weka (machine_learning)",
    "Dlib",
    "OpenSMILE",
    "Scikit-multiflow",
    "PolyAnalyst",
    "MATLAB",
    "Apache_MXNet",
    "ML.NET",
    "Distributed_R",
    "XGBoost",
    "ROOT",
    "QLattice",
    "Apache Flink",
    "Torch (machine_learning)",
    "Infer.NET",
    "Deeplearning4j",
    "Neural_Designer",
    "Jubatus",
    "LIONsolver",
    "Shogun (toolbox)",
    "Apache Spark",
    "TensorFlow",
    "Oracle_Data_Mining",
    "Java_Pathfinder",
    "Uppaal_Model_Checker",
    "TAPAAL_Model_Checker",
    "NuSMV",
    "SPIN_model_checker",
    "Romeo_Model_Checker",
    "ECLAIR"
]


for subdirectory in subdirectories:
    # Create the directory path for the subdirectory
    directory_path = os.path.join(parent_directory, subdirectory)
    csv_filename = f'{subdirectory}_{{year}}_matched.csv'  # Filename includes the subdirectory name

    # Create a list to store the results as dictionaries
    results_data = []

    # Loop through each year's folder (2015 to 2022)
    for year in range(2015, 2023):
        year_folder = os.path.join(directory_path, str(year))
        csv_file_path = os.path.join(year_folder, csv_filename.format(year=year))

        # Check if the CSV file exists
        if os.path.exists(csv_file_path):
            print(f"Year: {year}")
            yearly_counts = defaultdict(int)  # Dictionary to store counts for each year
            yearly_counts_for_total = defaultdict(int)
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)
            num_entries = len(df)
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
                                    yearly_counts_for_total[t] += 1
                for tool, count in yearly_counts.items():
                    if tool != 'Year':
                        yearly_counts[tool] = (count / num_entries) * 100

            # Create a dictionary for the yearly counts
            total_tools_matched = sum(yearly_counts_for_total.values()) - yearly_counts['Year']
            yearly_counts['Total Tools'] = (total_tools_matched / num_entries) * 100

            yearly_counts['Year'] = year

            results_data.append(yearly_counts)
            print("\n")
        else:
            print(f"Year {year} CSV file not found.\n")

    # Convert the list of dictionaries to a DataFrame
    results_df = pd.DataFrame(results_data)
    cols = results_df.columns.tolist()
    cols = ['Year'] + [col for col in cols if col != 'Year']
    results_df = results_df[cols]

    # Save the results to a CSV file in the respective subdirectory
    results_csv_file = os.path.join(directory_path, 'ML', 'job_advertisement_growth_normalised.csv')
    results_df.to_csv(results_csv_file, index=False)
    print(f"Results saved to {results_csv_file}")
