import pandas as pd
import glob


csv_files = glob.glob(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\matching\matching_hierarchy_result_*.csv')


dfs = []


for file in csv_files:

    df = pd.read_csv(file)
    print(file, len(df))
    dfs.append(df)


merged_df = pd.concat(dfs)


output_file = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\matched_tools_with_top_domains.csv'
merged_df.to_csv(output_file, index=False)
print(merged_df)


