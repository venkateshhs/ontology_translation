import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r'C:\Users\Vishwas\Desktop\Thesis\tool_fetch_dbpedia\Second Revison\To SHow it to professor Full output\unique_tools_by_top_domain.csv'
df = pd.read_csv(file_path)

print(df.head())

print(df.describe())

print(df.dtypes)

print(df.isnull().sum())

tool_counts = df.groupby('Top Domain')['Unique Tools'].nunique().astype(int)

plt.figure(figsize=(10, 6))
sns.barplot(x=tool_counts.index, y=tool_counts.values)
plt.xlabel('Top Domain')
plt.ylabel('Number of Unique Tools')
plt.title('Number of Unique Tools per Top Domain')
plt.xticks(rotation=45)
plt.show()

total_unique_tools = df['Unique Tools'].nunique()
print("Total number of unique tools: ", total_unique_tools)

avg_unique_tools = df.groupby('Top Domain')['Unique Tools'].nunique().mean()
print("Average number of unique tools per top domain: ", avg_unique_tools)

common_tools = df['Unique Tools'].value_counts().head(10)
print("Most common unique tools:")
print(common_tools)
