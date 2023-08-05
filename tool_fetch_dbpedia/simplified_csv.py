import pandas as pd


cso_df = pd.read_csv('../Common/CSO.3.3.csv', header=None)


cso_df.columns = ['subject', 'relation', 'object']
cso_df['subject'] = cso_df['subject'].apply(lambda x: x[1:-1].split('/')[-1])
cso_df['relation'] = cso_df['relation'].apply(lambda x: x[1:-1].split('/')[-1])
cso_df['object'] = cso_df['object'].apply(lambda x: x[1:-1].split('/')[-1])


cso_df.to_csv('CSO.3.3.simplified.csv', index=False)
