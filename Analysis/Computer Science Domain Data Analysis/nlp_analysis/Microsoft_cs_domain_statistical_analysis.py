import os
import pandas as pd
from collections import defaultdict

# Define the parent directory path
parent_directory = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data'

# List of subdirectories and CSV file names
subdirectories = ['431', '7126', '7121', '8311', '2511', '2512', '2513', '2514','2519']

tools_to_match = [
    "Windows 10",
    "Windows 11",
    "Windows Server",
    "Microsoft Office Suite",
    "Microsoft 365",
    "Microsoft Project",
    "Microsoft Visio",
    "Microsoft Azure",
    "Microsoft SQL Server",
    "Azure DevOps",
    "Windows Server",
    "Azure Kubernetes Service (AKS)",
    "Azure Functions",
    "Azure Logic Apps",
    "Visual Studio",
    "Visual Studio Code",
    ".NET Framework",
    ".NET Core",
    "Visual Basic",
    "C#",
    "TypeScript",
    "Azure DevOps Services",
    "Microsoft Teams",
    "Skype for Business",
    "SharePoint",
    "Yammer",
    "Exchange Server",
    "Dynamics 365",
    "Dynamics 365 Business Central",
    "Dynamics 365 Finance and Operations",
    "Power BI",
    "PowerApps",
    "Power Automate",
    "OneDrive for Business",
    "Microsoft Intune",
    "Azure Active Directory",
    "Azure Functions",
    "Azure Logic Apps",
    "Azure Cognitive Services",
    "Azure IoT Suite",
    "Microsoft Defender Antivirus",
    "Microsoft 365 Defender",
    "Azure Active Directory",
    "Azure Sentinel",
    "Azure Security Center",
    "Xbox Console",
    "Xbox Game Pass",
    "Xbox Live",
    "Microsoft Edge",
    "Bing",
    "Microsoft Surface",
    "Xbox Series X",
    "Xbox Series S",
    "Windows 8",
    "Windows 7",
    "Windows Server 2019",
    "Windows Server 2016",
    "Windows Server 2012",
    "Windows Server 2008",
    "Microsoft Word",
    "Microsoft Excel",
    "Microsoft PowerPoint",
    "Microsoft Outlook",
    "Microsoft Access",
    "Microsoft Publisher",
    "OneNote",
    "Microsoft Project Online",
    "Microsoft Project Server",
    "Microsoft Visio Online",
    "Microsoft Visio Professional",
    "Microsoft Visio Standard",
    "Microsoft Visio for the Web",
    "Microsoft Visio Plan 1",
    "Microsoft Visio Plan 2",
    "Microsoft Visio Services",
    "Microsoft Visio Viewer",
    "Microsoft Azure Virtual Machines",
    "Microsoft Azure SQL Database",
    "Microsoft Azure Kubernetes Service (AKS)",
    "Microsoft Azure Functions",
    "Microsoft Azure Logic Apps",
    "Visual Studio Community",
    "Visual Studio Professional",
    "Visual Studio Enterprise",
    ".NET 5",
    ".NET 6",
    "ASP.NET",
    "Entity Framework",
    "Azure DevOps Boards",
    "Azure DevOps Repos",
    "Azure DevOps Pipelines",
    "Azure DevOps Test Plans",
    "Azure DevOps Artifacts",
    "Azure DevOps Wiki",
    "Microsoft Teams Rooms",
    "Skype for Business Server",
    "SharePoint Online",
    "SharePoint Server",
    "SharePoint Designer",
    "Exchange Online",
    "Dynamics 365 Sales",
    "Dynamics 365 Customer Service",
    "Dynamics 365 Marketing",
    "Dynamics 365 Field Service",
    "Dynamics 365 Finance",
    "Dynamics 365 Supply Chain Management",
    "Dynamics 365 Business Central",
    "Dynamics 365 Human Resources",
    "Dynamics 365 Commerce",
    "Dynamics 365 Project Service Automation",
    "Dynamics 365 Customer Insights",
    "Power BI Pro",
    "Power BI Premium",
    "Power BI Embedded",
    "PowerApps Plan 1",
    "PowerApps Plan 2",
    "Power Automate Plan 1",
    "Power Automate Plan 2",
    "OneDrive",
    "OneDrive for Personal",
    "OneDrive for Business",
    "OneDrive for Mac",
    "OneDrive for Android",
    "OneDrive for iOS",
    "Microsoft Intune for Education",
    "Azure Active Directory B2C",
    "Azure Active Directory B2B",
    "Azure Functions Premium",
    "Azure Logic Apps Standard",
    "Azure Cognitive Services Computer Vision",
    "Azure Cognitive Services Language Understanding",
    "Azure Cognitive Services Speech",
    "Azure Cognitive Services Text Analytics",
    "Azure IoT Hub",
    "Azure IoT Central",
    "Microsoft Defender for Endpoint",
    "Microsoft Defender for Identity",
    "Microsoft Defender for Cloud",
    "Xbox Game Pass Ultimate",
    "Xbox Game Pass PC",
    "Xbox Game Pass for Console",
    "Xbox Live Gold",
    "Xbox Live Game Pass",
    "Microsoft Edge Dev",
    "Microsoft Edge Canary",
    "Microsoft Edge Insider",
    "Bing Maps",
    "Microsoft Surface Laptop",
    "Microsoft Surface Pro",
    "Microsoft Surface Book",
    "Microsoft Surface Studio",
    "Microsoft Surface Hub",
    "Microsoft Surface Go"
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
            unique_job_matched_count = 0
            # Check if 'Matched Tools' column exists
            if 'Matched Tools' in df.columns:
                # Iterate through the 'Matched Tools' column
                for index, row in df.iterrows():
                    matched_tools = row['Matched Tools']

                    if isinstance(matched_tools, str):
                        # Split the comma-separated values
                        tools_list = matched_tools.split(',')
                        tool_present = False
                        for tool in tools_list:
                            tool = tool.strip().lower()  # Convert to lowercase
                            for t in tools_to_match:
                                if t.lower() in tool:
                                    yearly_counts[t] += 1
                                    yearly_counts_for_total[t] += 1
                                    tool_present = True
                        if tool_present:
                            unique_job_matched_count +=1

                for tool, count in yearly_counts.items():
                    if tool != 'Year':
                        yearly_counts[tool] = (count / num_entries) * 100

            # Create a dictionary for the yearly counts
            total_tools_matched = sum(yearly_counts_for_total.values()) - yearly_counts['Year']
            yearly_counts['Total Tools'] = (total_tools_matched / num_entries) * 100
            yearly_counts["Percentage of Tools Matched"] = (unique_job_matched_count/num_entries) * 100
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
    results_csv_file = os.path.join(directory_path, 'microsoft', 'job_advertisement_growth_normalised.csv')
    results_df.to_csv(results_csv_file, index=False)
    print(f"Results saved to {results_csv_file}")
