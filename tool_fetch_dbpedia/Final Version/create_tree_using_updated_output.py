import pandas as pd

df1 = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\output_matches_updated.csv', encoding='ISO-8859-1')

df2 = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\Common\CSO.3.3.simplified.csv', encoding='ISO-8859-1')

df2_filtered = df2[df2['relation'] == 'cso#superTopicOf']

merged_df = pd.merge(df2_filtered, df1[['Subject', 'Object', 'same as']], how='inner', left_on=['subject', 'object'], right_on=['Subject', 'Object'])

result_df = merged_df[['subject' ,'relation', 'object']].drop_duplicates()

result_df.to_csv(r'C:\Users\Vishwas\Desktop\Thesis\matched_rows.csv', index=False)
