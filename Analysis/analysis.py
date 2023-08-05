import pandas as pd

csv_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\paths_and_tools.csv'
df = pd.read_csv(csv_path)
buffer_size = 30000
buffer = []
file_counter = 1

columns = [f"Domain {i + 1}" for i in range(15)]
df_domains = pd.DataFrame(columns=columns)

for index, row in df.iterrows():
    path = row['Path']
    domains = [s.strip().replace("_", " ") for s in path.split("->")]

    for i, domain in enumerate(domains[:15]):
        df_domains.loc[index, f"Domain {i + 1}"] = domain

    if index % 1000 == 0:
        print(index)

    if (index + 1) % buffer_size == 0:
        output_file = fr"C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\tree\complete_heirarchy_as_dataframe_{file_counter}.csv"
        df_domains.to_csv(output_file, index=False)
        file_counter += 1
        df_domains = pd.DataFrame(columns=columns)

output_file = fr"C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\tree\complete_heirarchy_as_dataframe_{file_counter}.csv"
df_domains.to_csv(output_file, index=False)

print(df_domains)
