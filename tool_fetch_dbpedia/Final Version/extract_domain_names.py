import pandas as pd

df_paths = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\new_paths.csv')

df_paths['Top Domain'] = df_paths['New_Path'].apply(lambda x: x.split('->')[0] if '->' in x else '')
df_paths['First Domain'] = df_paths['New_Path'].apply(lambda x: x.split('->')[1] if '->' in x else '')
df_paths['Second Domain'] = df_paths['New_Path'].apply(lambda x: x.split('->')[2] if '->' in x and len(x.split('->')) > 2 else '')
df_paths['Third Domain'] = df_paths['New_Path'].apply(lambda x: x.split('->')[3] if '->' in x and len(x.split('->')) > 3 else '')
df_paths['Fourth Domain'] = df_paths['New_Path'].apply(lambda x: x.split('->')[4] if '->' in x and len(x.split('->')) > 4 else '')

df_output = df_paths[['Top Domain', 'First Domain', 'Second Domain', 'Third Domain', 'Fourth Domain']].copy()
df_output.drop_duplicates(inplace=True)

grouped_df = df_output.groupby('Top Domain').agg(lambda x: ', '.join(x.unique()))
grouped_df.reset_index(inplace=True)

output_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\grouped_domain_names.csv'
grouped_df.to_csv(output_path, index=False)
print(f"Grouped domain names saved to: {output_path}")
